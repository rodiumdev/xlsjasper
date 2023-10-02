from toolbox import jrxmlbuilder

TARGET_XLS_FILE = "sfm.xlsx"

report = {
    "name": "sfm",
    "page": "Canevas SFM 2018",
    "title": {},
    "column-header": [
        {"group": True, "row": 64, "col": "A:A"},
        {"group": True, "row": 65, "col": "A:AK"},
        {"row": 66, "col": "A:AK"},
    ],
    "detail": {
        "param": {},
        "components": [
            {
                "type": "fields",
                "name_row": 65,
                "width_row": 66,
                "col": "A:AK",
                "fields": [
                    "'label",
                    "B:I|volume,valeur",
                    "D+F+H|volume,valeur",
                    "L:Q|volume,valeur",
                    "L+N+P|volume,valeur",
                    "T:Y|volume,valeur",
                    "T+V+X|volume,valeur",
                    "AB:AG|volume,valeur",
                    "AB+AD+AF|volume,valeur",
                    "D+F+H+L+N+P+T+V+X+AB+AD+AF|volume,valeur",
                ],
                "dataType": [
                    "'label->string",
                    "B:I|volume,valeur->int",
                    "L:Q|volume,valeur->int",
                    "T:Y|volume,valeur->int",
                    "AB:AG|volume,valeur->int",
                ],
            },
            {
                "type": "subreport",
                "structure": {
                    "name": "sfm-subreport",
                    "page": "Canevas SFM 2018",
                    "column-header": [
                        {"group": True, "row": 64, "col": "A:A"},
                        {"group": True, "row": 65, "col": "A:AK"},
                        {"row": 66, "col": "A:AK"},
                    ],
                    "detail": {
                        "param": {},
                        "components": [
                            {
                                "type": "fields",
                                "name_row": 65,
                                "width_row": 66,
                                "col": "A:AK",
                                "fields": [
                                    "'label",
                                    "B:I|volume,valeur",
                                    "D+F+H|volume,valeur",
                                    "L:Q|volume,valeur",
                                    "L+N+P|volume,valeur",
                                    "T:Y|volume,valeur",
                                    "T+V+X|volume,valeur",
                                    "AB:AG|volume,valeur",
                                    "AB+AD+AF|volume,valeur",
                                    "D+F+H+L+N+P+T+V+X+AB+AD+AF|volume,valeur",
                                ],
                            }
                        ],
                    },
                },
            },
        ],
    },
}


print("Building Reports .....")
print("started")
jrxmlbuilder.build(TARGET_XLS_FILE, report)
print("done")
