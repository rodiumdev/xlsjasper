import uuid
from toolbox import xmlutil
from toolbox import xlsutil
from toolbox import utils

PIXEL_FACTOR = 11 / 1.8


def get_default_parameters(position, value):
    parameters = {}
    parameters["x"] = position
    parameters["y"] = 0
    parameters["width"] = int(len(value) * PIXEL_FACTOR)
    parameters["height"] = 30
    parameters["v_align"] = "Middle"
    parameters["h_align"] = "Center"
    parameters["font"] = 11
    parameters["uuidv4"] = uuid.uuid4()
    parameters["border"] = 0

    return parameters


def build_values(value_type, position, value, parameters=False):
    # merge default parameters with custom parameters
    default_parameters = get_default_parameters(position, value)
    parameters = parameters if parameters else {}
    parameters = {**default_parameters, **parameters}
    parameters["value"] = value

    # build template
    template = "value-" + value_type + ".jrtmpl"
    return xmlutil.template_to_string(template) % parameters


def build_column():
    pass


def build_table():
    pass


def build_subreport():
    pass


def build_parameters():
    pass


def build_column_header(column_header, workbook, page):
    xls_column_range = xlsutil.generate_column_range(column_header.get("start_col"), column_header.get("end_col"))
    built_column_headers = ""
    position = 0
    param = column_header.get("param", {})
    print(xls_column_range)
    for xls_column in xls_column_range:
        value = xlsutil.read_cell(workbook, page, column_header.get("row"), xls_column)
        built_column_headers += build_values("static", position, value, param)
        position += int(len(value) * PIXEL_FACTOR)

    return xmlutil.template_to_string("report-columnHeader.jrtmpl") % {"columnHeader": built_column_headers}


def build_column_header_grouping(column_header, workbook, page):
    xls_column_range = xlsutil.generate_column_range(column_header.get("start_col"), column_header.get("end_col"))
    built_column_headers = ""
    position = 0
    param = column_header.get("param", {})

    grouped_columns = []

    for loop_index, xls_column in enumerate(xls_column_range):
        if xls_column == "":
            grouped_columns.append(xls_column)
        else:
            value = xlsutil.read_cell(workbook, page, column_header.get("row"), xls_column)
            built_column_headers += build_values("static", position, value, param)
            position += int(len(value) * PIXEL_FACTOR)

    return xmlutil.template_to_string("report-columnHeader.jrtmpl") % {"columnHeader": built_column_headers}


def build_column_header_single(column_header, workbook, page):
    xls_column_range = xlsutil.generate_column_range(column_header.get("start_col"), column_header.get("end_col"))
    built_column_headers = ""
    position = 0
    param = column_header.get("param", {})
    for xls_column in xls_column_range:
        value = xlsutil.read_cell(workbook, page, column_header.get("row"), xls_column)
        built_column_headers += build_values("static", position, value, param)
        position += int(len(value) * PIXEL_FACTOR)

    return xmlutil.template_to_string("report-columnHeader.jrtmpl") % {"columnHeader": built_column_headers}


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
