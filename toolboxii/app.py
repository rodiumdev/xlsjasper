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
    "K": "=E+G+J",
    "R": "=L+N+P",
    "S": "=M+O+Q",
    "Z": "=T+V+X",
    "AA": "=U+W+Y",
    "AH": "=AB+AD+AF",
    "AI": "=AC+AE+AG",
    "AJ": "=D+F+H+L+N+P+T+V+X+AB+AD+AF",
    "AK": "=E+G+J+M+O+Q+U+W+Y+AC+AE+AG",
}

report_definition = {
    "name": "sfm",
    "page": "Canevas SFM 2018",
    "colum_height": 20,
    "column_width": 200,
    "column_range": "A:AK",
    "components": [
        {"type": "main", "headers": "25:26", "fields": rg_fields},
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": cmplx_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": rg_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": rg_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": cmplx_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": cmplx_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": cmplx_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": cmplx_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": cmplx_fields}],
        },
        {
            "type": "subreport",
            "name": "subreport",
            "components": [{"type": "main", "headers": "62:64", "fields": rg_fields}],
        },
    ],
}

DEFAULT_HEIGHT = 20
DEFAULT_WIDTH = 100
XLS_FILE = "sfm.xlsx"


def main(report):
    if not utils.is_empty(report):
        parameters = {
            "name": report.get("name", "report"),
            "workbook": xls.load_workbook(XLS_FILE),
            "page": report.get("page", ""),
            "columns": jrxmlbuilder.expand_column_range(report.get("column_range", "")),
            "height": report.get("column_height", DEFAULT_HEIGHT),
            "width": report.get("column_width", DEFAULT_WIDTH),
        }

        for component in report.get("components", []):
            if component.get("type", "") == "main":
                jrxmlbuilder.main_report(component, parameters)

            if component.get("type", "") == "subreport":
                pass


main(report_definition)
