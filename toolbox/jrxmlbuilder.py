import uuid
from toolbox import xmlutil
from toolbox import xlsutil
from toolbox import utils

PIXEL_FACTOR = 11 / 1.7
DEFAULT_HEIGHT = 30


def get_grouping_value_and_width(xls_column_range, workbook, page, row):
    grouping_value_and_width = []
    active_group = 0
    for xls_column in xls_column_range:
        value = xlsutil.read_cell(workbook, page, row, xls_column)
        bootom_row_value = xlsutil.read_cell(workbook, page, row + 1, xls_column)
        if value == "":
            grouping_value_and_width[active_group]["width"] += int(len(bootom_row_value) * PIXEL_FACTOR)
        else:
            value_and_width = {"value": value, "width": int(len(bootom_row_value) * PIXEL_FACTOR)}
            grouping_value_and_width.append(value_and_width)
            active_group = len(grouping_value_and_width) - 1

    return grouping_value_and_width


def get_template_parameters(x_position, y_position, width, parameters=False):
    parameters = parameters if parameters else {}

    template_parameters = {}
    template_parameters["x"] = x_position
    template_parameters["y"] = y_position
    template_parameters["width"] = width
    template_parameters["height"] = DEFAULT_HEIGHT
    template_parameters["v_align"] = "Middle"
    template_parameters["h_align"] = "Center"
    template_parameters["font"] = 11
    template_parameters["uuidv4"] = uuid.uuid4()
    template_parameters["border"] = 0

    parameters = {**template_parameters, **parameters}

    return parameters


def build_values(value_type, value, parameters=False):
    parameters["value"] = value
    template = "value-" + value_type + ".jrtmpl"
    return xmlutil.template_to_string(template) % parameters


# def build_column():
#     pass


# def build_table():
#     pass


# def build_subreport():
#     pass


# def build_parameters():
#     pass


def build_column_header_grouping(column_header, workbook, page, y_position):
    xls_column_range = xlsutil.generate_column_range(column_header.get("start_col"), column_header.get("end_col"))
    groupings = get_grouping_value_and_width(xls_column_range, workbook, page, column_header.get("row"))
    custom_parameter = column_header.get("param", {})
    built_column_headers = ""
    position = 0

    for group in groupings:
        value = group.get("value", "")
        width = group.get("width", 0)
        template_parameters = get_template_parameters(position, y_position, width, custom_parameter)
        built_column_headers += build_values("static", value, template_parameters)
        position += group.get("width", 0)

    return built_column_headers


def build_column_header_basic(column_header, workbook, page, y_position):
    xls_column_range = xlsutil.generate_column_range(column_header.get("start_col"), column_header.get("end_col"))
    custom_parameter = column_header.get("param", {})
    built_column_headers = ""
    position = 0

    for xls_column in xls_column_range:
        value = xlsutil.read_cell(workbook, page, column_header.get("row"), xls_column)
        width = int(len(value) * PIXEL_FACTOR)
        template_parameters = get_template_parameters(position, y_position, width, custom_parameter)
        built_column_headers += build_values("static", value, template_parameters)
        position += int(len(value) * PIXEL_FACTOR)

    return built_column_headers


def build_column_header(column_headers, workbook, page):
    built_column_headers = ""
    height = DEFAULT_HEIGHT * len(column_headers)
    for loop_index, column_header in enumerate(column_headers):
        y_position = loop_index * DEFAULT_HEIGHT
        if column_header.get("group", False):
            built_column_headers += build_column_header_grouping(column_header, workbook, page, y_position)
        else:
            built_column_headers += build_column_header_basic(column_header, workbook, page, y_position)

    return xmlutil.template_to_string("report-columnHeader.jrtmpl") % {"columnHeader": built_column_headers, "height": height}


def build_report(report_structure, workbook):
    # file paths
    output_path = "C:/Programming/scripts_queries/scripts/xlsjasper/output/"

    # instatiation
    report = ""

    if "title" in report_structure and not utils.is_empty(report_structure.get("title")):
        pass

    if "page-header" in report_structure and not utils.is_empty(report_structure.get("page-header")):
        pass

    if "column-header" in report_structure and not utils.is_empty(report_structure.get("column-header")):
        column_header = report_structure.get("column-header")
        report += build_column_header(column_header, workbook, report_structure.get("page"))

    output = xmlutil.template_to_string("report.jrtmpl") % {"report": report}
    utils.print_to_file(output_path + report_structure.get("name", "report") + ".jrxml", output)


def build(file_name, structure):
    input_path = "C:/Programming/scripts_queries/scripts/xlsjasper/input/"
    workbook = xlsutil.load_workbook(input_path + file_name)
    build_report(structure, workbook)
