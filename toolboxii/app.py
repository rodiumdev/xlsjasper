from package import utils
from package import xls
from package import jrxmlbuilder

# fields: a string of special fields which requires specific treatment "A'|D=B+C|E,F,G=H+I*J|M-Z=B+a"

rg_fields = {"A": "label", "F": "=E", "J": "=I", "N": "=M", "R": "=Q", "S": "=Q"}
rg_fields_fn = {
    "A": "label",
    "F": "=C+D+E",
    "J": "=G+H+I",
    "N": "=K+L+M",
    "R": "=O+P+Q",
    "S": "=C+D+E+G+H+I+K+L+M+O+P+Q",
}

cmplx_fields = {
    "A": "label",
    "J": "=H",
    "K": "=J",
    "R": "=P",
    "S": "=Q",
    "Z": "=X",
    "AA": "=Y",
    "AH": "=AF",
    "AI": "=AG",
    "AJ": "=AF",
    "AK": "=AG",
}
cmplx_fields_fn = {
    "A": "label",
    "J": "=D+F+H",
    "K": "=E+G+I",
    "R": "=L+N+P",
    "S": "=M+O+Q",
    "Z": "=T+V+X",
    "AA": "=U+W+Y",
    "AH": "=AB+AD+AF",
    "AI": "=AC+AE+AG",
    "AJ": "=D+F+H+L+N+P+T+V+X+AB+AD+AF",
    "AK": "=E+G+I+M+O+Q+U+W+Y+AC+AE+AG",
}

report_definition = {
    "name": "sfm",
    "page": "Canevas SFM 2018",
    "colum_height": 20,
    "column_width": 200,
    "column_range": "A:AK",
    "components": [
        {
            "type": "main",
            "headers": "25:26",
            "fields": rg_fields,
            "parent": False,
            "subreports": [
                {
                    "name": "sfm_table_one_part_two",
                    "components": {"type": "main", "headers": "30", "fields": rg_fields_fn, "parent": False},
                },
                {
                    "name": "sfm_table_two_part_one",
                    "components": {"type": "main", "headers": "39:40", "fields": rg_fields, "parent": False},
                },
                {
                    "name": "sfm_table_three_part_one",
                    "components": {"type": "main", "headers": "49:50", "fields": rg_fields, "parent": False},
                },
                {
                    "name": "sfm_table_four_part_one",
                    "components": {"type": "main", "headers": "64:66", "fields": cmplx_fields_fn, "parent": True},
                },
                {
                    "name": "sfm_table_five_part_one",
                    "components": {"type": "main", "headers": "110:113", "fields": cmplx_fields_fn, "parent": True},
                },
                {
                    "name": "sfm_table_five_part_two",
                    "components": {"type": "main", "headers": "124:125", "fields": cmplx_fields_fn, "parent": True},
                },
                {
                    "name": "sfm_table_six_part_one",
                    "components": {"type": "main", "headers": "140:143", "fields": cmplx_fields_fn, "parent": True},
                },
                {
                    "name": "sfm_table_six_part_two",
                    "components": {"type": "main", "headers": "149:150", "fields": cmplx_fields_fn, "parent": True},
                },
                {
                    "name": "sfm_table_seven_part_one",
                    "components": {"type": "main", "headers": "161:162", "fields": rg_fields, "parent": False},
                },
            ],
        }
    ],
}

DEFAULT_HEIGHT = 20
DEFAULT_WIDTH = 100
XLS_FILE = "sfm.xlsx"
OUTPUT_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/output2/"


def main(report):
    print("starting ...")

    if not utils.is_empty(report):
        parameters = {
            "workbook": xls.load_workbook(XLS_FILE),
            "page": report.get("page", ""),
            "columns": jrxmlbuilder.expand_column_range(report.get("column_range", "")),
            "height": report.get("column_height", DEFAULT_HEIGHT),
            "width": report.get("column_width", DEFAULT_WIDTH),
            "output_path": OUTPUT_PATH,
        }

        for component in report.get("components", []):
            if component.get("type", "") == "main":
                jrxmlbuilder.main_report(report.get("name", "report"), component, parameters)

    print("...\n...\n...\nDone.")


main(report_definition)
