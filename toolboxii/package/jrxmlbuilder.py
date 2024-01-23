from package import utils
from package import xls


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

    table_structure = get_tbl_structure(parameters["workbook"], parameters["page"], headers, parameters["columns"])
    print(table_structure)
    if headers:
        build_header(table_structure, parameters["height"], parameters["width"])

    if fields:
        build_fields(fields)


def sub_report(component):
    pass


# Headers
def build_header(table_structure, row_height, column_width):
    for row in table_structure:
        value = ""
        width = 0
        position = 0
        position_tracker = 0
        first = True

        for column_key in row:
            if row[column_key] != "":
                if not first:
                    pass  # produce header column
                value = row[column_key] if row[column_key] != "-empty" else ""
                position += width
                width = column_width
            width += column_width
        pass  # produce header column


def produce_row():
    pass

    # for row in table_structure:
    #     value = ""
    #     position = 0
    #     width = column_width
    #     column_keys = row.keys()
    #     for index, column_key in column_keys:
    #         if row[column_key[index + 1]] == "":
    #             width += column_width
    #         if row[column_key] != "":
    #             if row[column_key] == "-empty-":
    #                 value = ""
    #             else:
    #                 value = row[column_key]


def get_tbl_structure(workbook, page, headers, columns):
    rows = expand_header_row_range(headers)
    header_column_list = []
    for row in rows:
        column_values = dict()
        for column in columns:
            column_values[column] = xls.read_cell(workbook, page, row, column)
        header_column_list.append(column_values)
    return clean_up_header_list(header_column_list)


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


# Fields
def build_fields(fields):
    pass


# others
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
