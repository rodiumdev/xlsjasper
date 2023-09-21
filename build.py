from toolbox import jrxmlbuilder

target_xls_file = "sfm.xls"

report = {
    "name": "sfm",
    "xlsPage": "Canevas SFM 2018",
    "title": {},
    "pageHeader": {},
    "columnHeader": {
        "titles": {"row": 26, "start_col": "A", "end_col": "A", "type": "static"},
        "groupings": {"row": 26, "start_col": "A", "end_col": "A", "type": "static"},
        "columns": {"row": 26, "start_col": "A", "end_col": "A", "type": "static"}
    },
    "detail": {
        "properties": {},
        "components": [
            {"type": "fields", "fields": {}},
        ],
    },
    "columnFooter": {},
    "pageFooter": {},
    "summary": {},
}


print("Building Reports .....")
print("started")
jrxmlbuilder.build_report(report)
print("done")
