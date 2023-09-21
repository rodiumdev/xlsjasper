from toolbox import xmlutil
from toolbox import xlsutil
from toolbox import utils


def build_values(type, value):
    template = "value-" + type + ".jrtmpl"
    return xmlutil.template_to_string % {}


def build_column():
    pass


def build_table():
    pass


def build_subreport():
    pass


def build_parameters():
    pass


def build_report(report_structure):
    # properties
    output_path = "C:/Programming/scripts_queries/scripts/jasper/output/"

    report = ""
    report_template = xmlutil.template_to_string("report.jrtmpl")

    # initialise subtemplate
    title_template = page_header_template = column_header_template = details_template = ""
    column_footer_template = page_footer_template = summary_template = ""

    if "title" in report_structure and not utils.is_empty(report_structure.get("title")):
        title_template = xmlutil.template_to_string("report-title.jrtmpl")
        report += title_template

    if "pageHeader" in report_structure and not utils.is_empty(report_structure.get("pageHeader")):
        pass

    if "columnHeader" in report_structure and not utils.is_empty(report_structure.get("columnHeader")):
        col_header_template = xmlutil.template_to_string(
            "report-columnHeader.jrtmpl")
        col_header = report_structure.get("columnHeader")

        # build title headings
        if "titles" in col_header and not utils.is_empty(col_header.get("titles")):
            col_header_title = col_header.get("titles")
            col_header_title_col_range = xlsutil.generate_column_range(
                col_header_title.get("start_col"), col_header_title.get("end_col"))
            for col_header_title_col in col_header_title_col_range:
                pass

        report += column_header_template

    # if "detail" in report_structure and not utils.is_empty(report_structure.get("detail")):
    #     details_template = xmlutil.template_to_string("report-detail.jrtmpl")
    #     report += details_template

    # if "columnFooter" in report_structure and not utils.is_empty(report_structure.get("columnFooter")):
    #     pass

    # if "pageFooter" in report_structure and not utils.is_empty(report_structure.get("pageFooter")):
    #     pass

    # if "summary" in report_structure and not utils.is_empty(report_structure.get("summary")):
    #     pass

    output = report_template % {"report": report}

    utils.print_to_file(
        output_path + report_structure.get("name", "report") + ".jrxml", output)
