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

    if headers:
        build_header(headers, parameters["workbook"], parameters["page"], parameters["columns"])

    if fields:
        build_fields(fields)


def sub_report(component):
    pass


# Headers
def build_header(headers, workbook, page, columns):
    rows = expang_row_range(headers)
    read_headers_from_excel(workbook, page, rows, columns)


def expang_row_range(header_range):
    points = header_range.split(":")
    if len(points) == 2:
        return list(range(int(points[0]), int(points[1]) + 1))
    return []


def read_headers_from_excel(workbook, page, rows, columns):
    header_column_list = []
    for row in rows:
        column_values = dict()
        for column in columns:
            column_values[column] = xls.read_cell(workbook, page, row, column)
        header_column_list.append(column_values)
    print(header_column_list)


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
