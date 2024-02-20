from package import utils
from package import xls
from package import template
import uuid


# ALGORITHM
# loop trough components
# if type is main process the report by
#   finding the table size using the last header index
#   producer header
#   produce fields
# move to next component
# if subreport add to main report and expand its component
# balsamiq: quantity et proforma


# Reports
def main_report(component, parameters):
    headers = component.get("headers", "")
    fields = component.get("fields", "")
    report = ""

    table_structure = get_tbl_structure(
        parameters["workbook"], parameters["page"], headers, parameters["columns"], parameters["width"]
    )

    if headers:
        report += build_header(table_structure, parameters["height"])

    if fields:
        report += build_fields(table_structure, fields, parameters["height"])

    # to be reviewed
    output = template.template_to_string("report.jrtmpl") % {
        "report": report,
        "parameters": "",
        "fields": "",
        "pageWidth": 0,
        "columnWidth": 0,
        "pageHeight": 0,
        "reportUuid": uuid.uuid4(),
    }

    utils.print_to_file(parameters["output_path"] + "jasper" + "/" + parameters["name"] + ".jrxml", output)


def sub_report(component):
    pass


# Headers
def build_header(table_structure, row_height):
    headers_xml = ""
    for y_index, row in enumerate(table_structure):
        for column in row:
            column_data = row[column]
            parameters = build_parameters(column_data, row_height, y_index)
            headers_xml += template.template_to_string("value-static.jrtmpl") % parameters
    return template.template_to_string("report-columnHeader.jrtmpl") % {
        "columnHeader": headers_xml,
        "height": row_height * len(table_structure),
    }


# Fields
def build_fields(table_structure, fields, row_height):
    last_row_index = len(table_structure) - 1
    last_row = table_structure[last_row_index]
    fields_xml = ""

    for column in last_row:
        if column in fields:
            field_representation = fields[column]
            if "=" not in field_representation:
                pass
            else:
                pass

            fields_xml += ""
        else:
            fields_xml += ""
        # static, value, calc


def make_static_field():
    pass


# others
def build_parameters(column_data, height, y_index):
    parameters = {}
    parameters["x"] = column_data["position"]
    parameters["y"] = y_index * height
    parameters["width"] = column_data["width"]
    parameters["height"] = height
    parameters["value"] = column_data["value"]

    parameters["v_align"] = "Middle"
    parameters["h_align"] = "Center"
    parameters["border"] = 1
    parameters["font"] = 11
    parameters["uuidv4"] = uuid.uuid4()

    return parameters


def expand_column_range(column_range):
    points = column_range.split(":")

    if len(points) == 2:
        start = points[0]
        end = points[1]

        if len(end) < 2:
            return utils.charecter_range(start, end)
        else:
            column_range = []
            if len(start) < 2:
                first_charecter_start = "A"
                second_charecter_start = "A"
                column_range = utils.charecter_range(start, "Z")
            else:
                first_charecter_start = start[0]
                second_charecter_start = start[1]
            end_range = utils.charecter_range(first_charecter_start, end[0])

            for first_charecter in end_range:
                for second_charecter in utils.charecter_range(second_charecter_start, "Z"):
                    res = first_charecter + second_charecter
                    if res != end:
                        column_range.append(res)
                    else:
                        break
                second_charecter_start = "A"
            column_range.append(end)
            return column_range
    return []


def get_tbl_structure(workbook, page, headers, columns, default_width):
    rows = expand_header_row_range(headers)
    header_column_list = []
    for row in rows:
        column_values = dict()
        for column in columns:
            column_values[column] = xls.read_cell(workbook, page, row, column)
        header_column_list.append(column_values)
    cleaned_row_list = clean_up_header_list(header_column_list)
    return make_proper_structure(cleaned_row_list, default_width)


def expand_header_row_range(header_range):
    points = header_range.split(":")
    if len(points) == 2:
        return list(range(int(points[0]), int(points[1]) + 1))
    return []


def clean_up_header_list(header_rows):
    if header_rows:
        last_row_index = len(header_rows) - 1
    column_to_remove = []
    for column in reversed(header_rows[last_row_index]):
        if header_rows[last_row_index][column] == "":
            column_to_remove.append(column)
        else:
            break

    for column in column_to_remove:
        for header_row in header_rows:
            header_row.pop(column)
    for header_row in header_rows:
        for col in header_row:
            if header_row[col] == "":
                header_row[col] = "-empty-"
            else:
                break
    return header_rows


def make_proper_structure(cleaned_row_list, column_width):
    structure_row_list = []

    for row in cleaned_row_list:
        structure_row = {}
        key_list = list(row.keys())
        cell_key = ""
        cell_width = 0
        cell_position = 0
        cell_value = ""
        for index, col_key in enumerate(key_list):
            if row[col_key] != "":  # ignore null value cells
                cell_value = row[col_key]
                cell_key = col_key
            cell_width += column_width

            # if next column is not empty store the value, width and position information
            if (index + 2 > len(key_list)) or row[key_list[index + 1]] != "":
                structure_row[cell_key] = {"value": cell_value, "width": cell_width, "position": cell_position}
                cell_width = 0
                cell_position += column_width
        structure_row_list.append(structure_row)
    return structure_row_list
