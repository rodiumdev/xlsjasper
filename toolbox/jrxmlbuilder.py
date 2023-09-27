import uuid
from toolbox import xmlutil
from toolbox import xlsutil
from toolbox import utils

INPUT_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/input/"
PIXEL_FACTOR = 11 / 1.6
DEFAULT_HEIGHT = 30


def expand_column(columns):
    column_start, column_end = columns.split(":")
    if len(column_end) < 2:
        return xlsutil.generate_column_range(column_start, column_end)
    else:
        column_range = []
        if len(column_start) < 2:
            first_charecter_start = "A"
            second_charecter_start = "A"
            column_range = xlsutil.generate_column_range(column_start, "Z")
        else:
            first_charecter_start = column_start[0]
            second_charecter_start = column_start[1]

        end_range = xlsutil.generate_column_range(first_charecter_start, column_end[0])

        for first_charecter in end_range:
            for second_charecter in xlsutil.generate_column_range(second_charecter_start, "Z"):
                res = first_charecter + second_charecter
                if res != column_end:
                    column_range.append(res)
                else:
                    break
            second_charecter_start = "A"
        column_range.append(column_end)
        return column_range


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
    template_parameters["border"] = 1

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
    xls_column_range = expand_column(column_header.get("col"))
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
    xls_column_range = expand_column(column_header.get("col"))
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

    return xmlutil.template_to_string("report-columnHeader.jrtmpl") % {
        "columnHeader": built_column_headers,
        "height": height,
    }


def get_field_names(workbook, page, row, xls_columns):
    col_range = expand_column(xls_columns)
    filed_names = {}
    active_value = ""
    for xls_column in col_range:
        value = xlsutil.read_cell(workbook, page, row, xls_column)
        if value != "":
            active_value = value
        filed_names[xls_column] = utils.to_java_variable(active_value)
    return filed_names


def get_field_width(workbook, page, row, xls_columns):
    col_range = expand_column(xls_columns)
    filed_widths = []
    for xls_column in col_range:
        value = xlsutil.read_cell(workbook, page, row, xls_column)
        filed_widths.append(int(len(value) * PIXEL_FACTOR))
    return filed_widths


def expand_fields(fields, field_names):
    expanded_fields = []
    value_field = "$F{%(value)s}"

    for field in fields:
        if "'" in field:
            value = field.replace("'", "")
            expanded_fields.append(value_field % {"value": value})

        if ":" in field and ("|" not in field):
            col_list = expand_column(field)
            for col in col_list:
                value = "%(" + col + ")s"
                value = value % field_names
                expanded_fields.append(value_field % {"value": value})

        if ":" in field and "|" in field:
            cols, modifier = field.split("|")
            col_list = expand_column(cols)
            modifier_list = modifier.split(",")
            for loop_index, col in enumerate(col_list):
                modifier_index = loop_index % (len(modifier_list))
                value = "%(" + col + ")s" + modifier_list[modifier_index].capitalize()
                value = value % field_names
                expanded_fields.append(value_field % {"value": value})

        if ":" not in field and "'" not in field:
            operands = ["+", "-", "*", "/", "%"]
            operand = ""
            for ops in operands:
                if ops in field:
                    operand = ops

            if "|" in field:
                formula, modifiers = field.split("|")
                col_list = formula.split(operand)
                modifier_list = modifiers.split(",")
                for modifier in modifier_list:
                    modified_field = []
                    for col in col_list:
                        value = "%(" + col + ")s"
                        value = value % field_names
                        modified_field.append(value_field % {"value": value + modifier.capitalize()})
                    expanded_fields.append(operand.join(modified_field))
            else:
                col_list = field.split(operand)
                modified_field = []
                for col in col_list:
                    value = "%(" + col + ")s"
                    value = value % field_names
                    modified_field.append(value_field % {"value": value})
                expanded_fields.append(operand.join(modified_field))

    return expanded_fields


def build_fields(workbook, page, component, y_position, parameters=False):
    field_name = get_field_names(workbook, page, component.get("name_row"), component.get("col"))
    width_row = component.get("width_row") if "width_row" in component else component.get("name_row")

    field_width = get_field_width(workbook, page, width_row, component.get("col"))
    expanded_fields = expand_fields(component.get("fields", []), field_name)

    built_fields = ""
    position = 0

    for loop_index, field in enumerate(expanded_fields):
        template_parameters = get_template_parameters(
            position, y_position, field_width[loop_index], parameters=parameters
        )
        built_fields += build_values("field-complex", field, template_parameters)
        position += field_width[loop_index]
    return built_fields


def build_detail(detail, workbook, page):
    built_column_details = ""
    height = DEFAULT_HEIGHT - 5

    for loop_index, component in enumerate(detail.get("components", [])):
        if component.get("type") == "fields":
            param = detail.get("param", {})
            param["height"] = height
            y_position = loop_index * height
            built_column_details += build_fields(workbook, page, component, y_position, param)
        if component.get("type") == "subreport":
            pass
        if component.get("type") == "table":
            pass

    return xmlutil.template_to_string("report-detail.jrtmpl") % {"detail": built_column_details, "height": height}


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

    if "detail" in report_structure and not utils.is_empty(report_structure.get("detail")):
        detail = report_structure.get("detail")
        report += build_detail(detail, workbook, report_structure.get("page"))

    output = xmlutil.template_to_string("report.jrtmpl") % {"report": report}
    utils.print_to_file(output_path + report_structure.get("name", "report") + ".jrxml", output)


def build(file_name, structure):
    input_path = INPUT_PATH
    workbook = xlsutil.load_workbook(input_path + file_name)
    build_report(structure, workbook)
