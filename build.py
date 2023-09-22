from toolbox import jrxmlbuilder

TARGET_XLS_FILE = "sfm.xlsx"

report = {
    "name": "sfm",
    "page": "Canevas SFM 2018",
    "title": {},
    "page-header": {},
    "column-header": [{"group_for": 1, "row": 65, "start_col": "A", "end_col": "S", "param": {"border": 1}}, {"row": 65, "start_col": "A", "end_col": "S", "param": {"border": 1}}],
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
jrxmlbuilder.build(TARGET_XLS_FILE, report)
print("done")
