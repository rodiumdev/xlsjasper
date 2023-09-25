from toolbox import jrxmlbuilder

TARGET_XLS_FILE = "sfm.xlsx"

report = {
    "name": "sfm",
    "page": "Canevas SFM 2018",
    "title": {},
    "page-header": {},
    "column-header": [{"group": True, "row": 64, "col": "A:A"}, {"group": True, "row": 65, "col": "A:S"}, {"row": 66, "col": "A:S"}],
    "detail": {
        "parameters": {"border:": 1},
        "components": [
            {"type": "fields", "row": 67, "fields": ["label", "B:C", "sum|E:G-volume,valeur", "A:B"]},
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
