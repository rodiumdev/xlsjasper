import uuid
from toolbox import temputil
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
            value_and_width = {}
            if bootom_row_value == "":
                value_and_width = {"value": value, "width": int(len(value) * PIXEL_FACTOR)}
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
    return temputil.template_to_string(template) % parameters


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

    return temputil.template_to_string("report-columnHeader.jrtmpl") % {
        "columnHeader": built_column_headers,
        "height": height,
    }


def expand_data_type(data_types, field_names):
    expanded_data_type = ""
    model_schema = []

    for field_and_type in data_types:
        field, data_type = field_and_type.split("->")
        if "'" in field:
            value = field.replace("'", "")
            expanded_data_type += temputil.template_to_string("field-" + data_type + ".jrtmpl") % {"name": value}
            model_schema.append([data_type, value])

        if ":" in field and ("|" not in field):
            col_list = expand_column(field)
            for col in col_list:
                value = "%(" + col + ")s"
                value = value % field_names
                expanded_data_type += temputil.template_to_string("field-" + data_type + ".jrtmpl") % {"name": value}
                model_schema.append([data_type, value])

        if ":" in field and "|" in field:
            cols, modifier = field.split("|")
            col_list = expand_column(cols)
            modifier_list = modifier.split(",")
            for loop_index, col in enumerate(col_list):
                modifier_index = loop_index % (len(modifier_list))
                value = "%(" + col + ")s" + modifier_list[modifier_index].capitalize()
                value = value % field_names
                expanded_data_type += temputil.template_to_string("field-" + data_type + ".jrtmpl") % {"name": value}
                model_schema.append([data_type, value])

    return expanded_data_type, model_schema


def declare_fields(workbook, page, component):
    field_names = get_field_names(workbook, page, component.get("name_row"), component.get("col"))
    fields, model_schema = expand_data_type(component.get("dataType", []), field_names)
    build_java_model(component.get("package"), component.get("field_name", "report"), model_schema)
    return fields


def build_java_model(package, model_name, model_schema):
    model = (
        "import lombok.Getter;\nimport lombok.Setter;\n\n@Getter\n@Setter\npublic class "
        + utils.to_java_class(model_name)
        + "Fields {\n"
    )
    date_import = ""

    for attribute in model_schema:
        if attribute[0] == "int":
            model += "private Integer " + attribute[1] + ";\n"
        if attribute[0] == "long":
            model += "private Long " + attribute[1] + ";\n"
        if attribute[0] == "date":
            date_import = "import java.util.Date;\n"
            model += "private Date " + attribute[1] + ";\n"
        if attribute[0] == "string ":
            model += "private String " + attribute[1] + ";\n"
    model = "package " + package + ".models;\n\n" + date_import + model
    model += "}"
    output_path = "C:/Programming/scripts_queries/scripts/xlsjasper/output/java/models/"
    utils.print_to_file(output_path + utils.to_java_class(model_name) + "Fields.java", model)


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
        # if value == "":
        #     filed_widths.append(180)
        # else:
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

            if operand == "":
                value = "%(" + field + ")s"
                value = value % field_names
                expanded_fields.append(value_field % {"value": value})
                continue
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


def declare_java_sbureport(structure):
    output_path = "C:/Programming/scripts_queries/scripts/xlsjasper/temp/java/"

    template_subreport = temputil.java_template_to_string("subreport.javtmpl") % {
        "package": structure.get("package"),
        "class_name": utils.to_java_class(structure.get("name", "subreport")),
        "field_class_name": utils.to_java_class(structure.get("field_name", "subreport")),
        "obj_name": utils.to_java_object(structure.get("name", "subreport")),
    }

    utils.append_to_file(output_path + "tmp.java", template_subreport)


def build_subreport(report_structure, workbook, y_position, height):
    build_report(report_structure, workbook)
    declare_java_sbureport(report_structure)
    target_parameter = utils.to_java_object(report_structure["name"])
    default_parameters = {
        "height": height,
        "target_parameter": target_parameter,
        "data_source": target_parameter + "Source",
    }
    template_parameters = get_template_parameters(0, y_position, 1920, parameters=default_parameters)
    return (
        temputil.template_to_string("subreport.jrtmpl") % template_parameters,
        temputil.template_to_string("parameter-subreport.jrtmpl")
        % {"name": default_parameters.get("target_parameter"), "nameSource": default_parameters.get("data_source")},
    )


def build_detail(detail, workbook, page):
    built_details = ""
    height = DEFAULT_HEIGHT - 5
    detail_height = len(detail.get("components", [])) * height
    declared_fields = ""
    subreport_parameters = ""

    for loop_index, component in enumerate(detail.get("components", [])):
        y_position = loop_index * height
        if component.get("type") == "fields":
            param = detail.get("param", {})
            param["height"] = height
            built_details += build_fields(workbook, page, component, y_position, param)
            declared_fields = declare_fields(workbook, page, component)
        if component.get("type") == "subreport":
            subreport_detail, subreport_parameter = build_subreport(
                component.get("structure", {}), workbook, y_position, height
            )
            subreport_parameters += subreport_parameter
            built_details += subreport_detail

        if component.get("type") == "table":
            pass

    return (
        temputil.template_to_string("report-detail.jrtmpl") % {"detail": built_details, "height": detail_height},
        declared_fields,
        subreport_parameters,
    )


def build_template_request_parameters_model(structure):
    output_path = "C:/Programming/scripts_queries/scripts/xlsjasper/output/java/models/"

    template_request_parameters_model = temputil.java_template_to_string("model-request-param.javtmpl") % {
        "package": structure.get("package"),
        "class_name": utils.to_java_class(structure.get("name", "")),
    }

    utils.print_to_file(
        output_path + utils.to_java_class(structure.get("name", "")) + "RequestParameters.java",
        template_request_parameters_model,
    )


def build_template_provider(structure):
    output_path = "C:/Programming/scripts_queries/scripts/xlsjasper/output/java/"

    template_provider = temputil.java_template_to_string("provider.javtmpl") % {
        "package": structure.get("package"),
        "class_name": utils.to_java_class(structure.get("name", "report")),
        "field_class_name": utils.to_java_class(structure.get("field_name", "report")),
        "obj_name": utils.to_java_object(structure.get("name", "report")),
        "subreports": temputil.tmp_template_to_string(),
    }

    utils.print_to_file(
        output_path + utils.to_java_class(structure.get("name", "report")) + "Provider.java", template_provider
    )


def build_report(report_structure, workbook):
    # instatiation
    output_path = "C:/Programming/scripts_queries/scripts/xlsjasper/output/"
    report = ""

    if "title" in report_structure and not utils.is_empty(report_structure.get("title")):
        pass

    if "column-header" in report_structure and not utils.is_empty(report_structure.get("column-header")):
        column_header = report_structure.get("column-header")
        report += build_column_header(column_header, workbook, report_structure.get("page"))

    if "detail" in report_structure and not utils.is_empty(report_structure.get("detail")):
        detail = report_structure.get("detail")
        detail_report, detail_fields, subreport_parameters = build_detail(
            detail, workbook, report_structure.get("page")
        )
        report += detail_report

    output = temputil.template_to_string("report.jrtmpl") % {
        "report": report,
        "parameters": subreport_parameters,
        "fields": detail_fields,
        "pageWidth": report_structure.get("width", 1920) + 40,
        "columnWidth": report_structure.get("Width", 1920),
        "pageHeight": report_structure.get("height", 200),
        "reportUuid": uuid.uuid4(),
    }
    utils.print_to_file(output_path + report_structure.get("name", "report") + ".jrxml", output)


def build(file_name, structure):
    input_path = INPUT_PATH
    workbook = xlsutil.load_workbook(input_path + file_name)

    build_report(structure, workbook)
    build_template_request_parameters_model(structure)
    build_template_provider(structure)
