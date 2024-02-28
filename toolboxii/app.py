import reportConfig
from package import utils
from package import xls
from package import jrxmlbuilder
from package import config


OUTPUT_PATH_JASPER = config.JASPER_OUTPUT_PATH
OUTPUT_PATH_JAVA = config.JAVA_OUTPUT_PATH

XLS_FILE = reportConfig.INPUT_XLS_FILE
NAME_SPACE = reportConfig.NAME_SPACE

DEFAULT_HEIGHT = 20
DEFAULT_WIDTH = 100


def main(report):
    print("starting .")

    if not utils.is_empty(report):
        print("initiatilising report parameters ..")
        parameters = {
            "name_space": NAME_SPACE,
            "package": report.get("name", "report"),
            "workbook": xls.load_workbook(XLS_FILE),
            "page": report.get("page", ""),
            "columns": jrxmlbuilder.expand_column_range(report.get("column_range", "")),
            "height": report.get("column_height", DEFAULT_HEIGHT),
            "width": report.get("column_width", DEFAULT_WIDTH),
            "output_path_jasper": OUTPUT_PATH_JASPER,
            "output_path_java": OUTPUT_PATH_JAVA,
        }

        for component in report.get("components", []):
            if component.get("type", "") == "main":
                print("building report ...")
                report_name = report.get("name", "report")
                main_report_field_class = component.get("field_class", "default")
                jrxmlbuilder.main_report(report_name, component, parameters)
                jrxmlbuilder.build_provider(NAME_SPACE, report_name, main_report_field_class, OUTPUT_PATH_JAVA)
                jrxmlbuilder.build_helper(NAME_SPACE, report_name, OUTPUT_PATH_JAVA)
                jrxmlbuilder.build_request_parameter_model(NAME_SPACE, report_name, OUTPUT_PATH_JAVA)

    print("Done")


main(reportConfig.report_definition)
