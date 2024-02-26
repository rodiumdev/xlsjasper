import uuid
from package import utils
from package import xls
from package import template


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
def main_report(name, component, parameters):
    headers = component.get("headers", "")
    fields = component.get("fields", {})
    subreports = component.get("subreports", [])

    report_xml = ""
    fields_xml = ""
    subreports_xml = ""
    parameters_declarations_xml = ""
    field_declarations_xml = ""

    table_structure = get_tbl_structure(
        parameters["workbook"],
        parameters["page"],
        headers,
        component.get("parent"),
        parameters["columns"],
        parameters["width"],
    )

    report_width = parameters["width"] * len(parameters["columns"])
    report_header_height = parameters["height"] * len(table_structure)
    report_detail_height = parameters["height"] * (len(subreports) + 1)

    # print(table_structure)

    if headers:
        report_xml += build_header(table_structure, parameters["height"])

    if fields:
        fields_xml += build_fields(table_structure, fields, parameters["height"])
        field_declarations_xml = declare_jasper_fields(table_structure, fields)

    for sub_report_index, subreport in enumerate(subreports):
        sub_report_name = subreport.get("name", "subreport")
        main_report(sub_report_name, subreport.get("components", {}), parameters)
        subreports_xml += sub_report(sub_report_name, report_width, parameters["height"], sub_report_index)
        parameters_declarations_xml += declare_jasper_subreport_parameters(sub_report_name)

    report_xml += build_details(fields_xml, subreports_xml, report_detail_height)

    # to be reviewed
    output = template.template_to_string("report.jrtmpl") % {
        "report": report_xml,
        "parameters": parameters_declarations_xml,
        "fields": field_declarations_xml,
        "pageWidth": report_width + 80,
        "columnWidth": report_width + 40,
        "pageHeight": report_header_height + report_detail_height + 40,
        "reportUuid": uuid.uuid4(),
    }

    utils.print_to_file(parameters["output_path"] + "jasper" + "/" + name + ".jrxml", output)


# Subreports
def sub_report(subreport_name, width, height, y_index):
    parameters = build_subreport_parameters(subreport_name, width, height, y_index)
    return template.template_to_string("subreport.jrtmpl") % parameters


def declare_jasper_subreport_parameters(subreport_name):
    return template.template_to_string("parameter-subreport.jrtmpl") % {
        "name": utils.to_variable(utils.clean_brackets(subreport_name) + " Subreport"),
        "nameSource": utils.to_variable(utils.clean_brackets(subreport_name) + " DataSource"),
    }


# Headers
def build_header(table_structure, row_height):
    headers_xml = ""
    for y_index, row in enumerate(table_structure):
        for column in row:
            column_data = row[column]
            parameters = build_field_or_header_parameters(column_data, row_height, y_index)
            headers_xml += template.template_to_string("value-static.jrtmpl") % parameters
    return template.template_to_string("report-columnHeader.jrtmpl") % {
        "columnHeader": headers_xml,
        "height": row_height * len(table_structure),
    }


# Detaisl
def build_details(fields_xml, subreport_xml, height):
    return template.template_to_string("report-detail-plus-subreport.jrtmpl") % {
        "detail": fields_xml,
        "subreport": subreport_xml,
        "height": height,
    }


# Fields
def build_fields(table_structure, fields, row_height):
    y_index = len(table_structure)
    last_row_index = y_index - 1
    last_row = table_structure[last_row_index]
    fields_xml = ""

    for column_key in last_row:
        if column_key in fields:
            field_representation = fields[column_key]
            if "=" not in field_representation:  # fixed variable name
                fields_xml += make_fixed_field(last_row[column_key], field_representation, row_height, 0)
            else:  # calculation based on other columns
                fields_xml += make_calc_field(last_row[column_key], field_representation[1:], last_row, row_height, 0)
        else:
            fields_xml += make_vairable_field(last_row[column_key], row_height, 0)
    return fields_xml


def declare_jasper_fields(table_structure, fields):
    last_row = table_structure[len(table_structure) - 1]
    field_declarations_xml = ""

    for column_key in last_row:
        if column_key in fields:
            field_representation = fields[column_key]
            if "=" not in field_representation:  # fixed variable name
                field_declarations_xml += template.template_to_string("field-string.jrtmpl") % {
                    "name": utils.to_variable(field_representation)
                }
        else:
            column_data = last_row[column_key]
            field_declarations_xml += template.template_to_string("field-int.jrtmpl") % {
                "name": utils.to_variable(
                    utils.clean_brackets(column_data["parent"]) + " " + utils.clean_brackets(column_data["value"])
                )
            }
    return field_declarations_xml


def make_fixed_field(column_data, field_representation, row_height, y_index):
    local_col_data = column_data.copy()
    local_col_data["value"] = "$F{" + utils.to_variable(field_representation) + "}"
    parameters = build_field_or_header_parameters(local_col_data, row_height, y_index)
    return template.template_to_string("value-field-complex.jrtmpl") % parameters


def make_vairable_field(column_data, row_height, y_index):
    local_col_data = column_data.copy()
    value = utils.clean_brackets(column_data["parent"]) + " " + utils.clean_brackets(column_data["value"])
    local_col_data["value"] = "$F{" + utils.to_variable(value) + "}"
    parameters = build_field_or_header_parameters(local_col_data, row_height, y_index)
    return template.template_to_string("value-field-complex.jrtmpl") % parameters


def make_calc_field(column_data, field_representation, last_row, row_height, y_index):
    local_col_data = column_data.copy()
    operand = get_operation(field_representation)
    column_keys = field_representation.split(operand) if operand != "" else [field_representation]
    evaluated_columns = []

    for column_key in column_keys:
        value = utils.to_variable(
            utils.clean_brackets(last_row[column_key]["parent"])
            + " "
            + utils.clean_brackets(last_row[column_key]["value"])
        )
        evaluated_columns.append("$F{" + value + "}")

    local_col_data["value"] = operand.join(str(x) for x in evaluated_columns)
    parameters = build_field_or_header_parameters(local_col_data, row_height, y_index)
    return template.template_to_string("value-field-complex.jrtmpl") % parameters


def get_operation(field_representation):
    if "+" in field_representation:
        return "+"
    if "-" in field_representation:
        return "-"
    if "*" in field_representation:
        return "*"
    if "/" in field_representation:
        return "/"
    return ""


# others
def build_field_or_header_parameters(column_data, height, y_index):
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


def build_subreport_parameters(name, width, height, y_index):
    parameters = {}
    parameters["x"] = 0
    parameters["y"] = (y_index + 1) * height
    parameters["width"] = width
    parameters["height"] = height
    parameters["data_source"] = utils.to_variable(name) + "DataSource"
    parameters["target_parameter"] = utils.to_variable(name) + "Subreport"
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


def get_tbl_structure(workbook, page, headers, parent, columns, default_width):
    rows = expand_header_row_range(headers)
    header_column_list = []
    for row in rows:
        column_values = dict()
        for column in columns:
            column_values[column] = xls.read_cell(workbook, page, row, column)
        header_column_list.append(column_values)
    cleaned_row_list = clean_up_header_list(header_column_list)
    return make_proper_structure(cleaned_row_list, parent, default_width)


def expand_header_row_range(header_range):
    points = header_range.split(":")
    if len(points) == 1:
        return [int(points[0])]
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


def make_proper_structure(cleaned_row_list, parent, column_width):
    structure_row_list = []

    for row_index, row in enumerate(cleaned_row_list):
        structure_row = {}
        key_list = list(row.keys())
        cell_key = ""
        cell_width = 0
        cell_position = 0
        cell_value = ""
        cell_parent_value = ""
        for index, col_key in enumerate(key_list):
            if row[col_key] != "":  # ignore null value cells
                cell_value = row[col_key] if row[col_key] != "-empty-" else ""
                cell_key = col_key
            if (
                row_index > 0
                and parent
                and cleaned_row_list[row_index - 1][col_key] != ""
                and cleaned_row_list[row_index - 1][col_key] != "-empty-"
            ):  # ignore null value cells
                cell_parent_value = cleaned_row_list[row_index - 1][col_key]
            cell_width += column_width

            # if next column is not empty store the value, width and position information
            if (index + 2 > len(key_list)) or row[key_list[index + 1]] != "":
                structure_row[cell_key] = {
                    "value": cell_value,
                    "width": cell_width,
                    "position": cell_position,
                    "parent": cell_parent_value,
                }
                cell_position += cell_width
                cell_width = 0
        structure_row_list.append(structure_row)
    return structure_row_list
