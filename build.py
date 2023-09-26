from toolbox import jrxmlbuilder

TARGET_XLS_FILE = "sfm.xlsx"

report = {
    "name": "sfm",
    "page": "Canevas SFM 2018",
    "title": {},
    "page-header": {},
    "column-header": [{"group": True, "row": 64, "col": "A:A"}, {"group": True, "row": 65, "col": "A:S"}, {"row": 66, "col": "A:S"}],
    "detail": {
        "param": {},
        "components": [
            {"type": "fields", "name_row": 65, "width_row": 66, "col": "A:S", "fields": ["'label", "B:C", "D:E|volume,valeur", "A+B+C"]},
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
