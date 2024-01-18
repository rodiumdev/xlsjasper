from toolbox import jrxmlbuilder

TARGET_XLS_FILE = "sfm.xlsx"

fields_single = ["'label", "B:E", "E", "G:I", "I", "K:M", "M", "O:Q", "Q", "Q"]

fields_single_sum = [
    "'label",
    "B:E",
    "C+D+E",
    "G:I",
    "G+H+I",
    "K:M",
    "K+L+M",
    "O:Q",
    "O+P+Q",
    "C+D+E+G+H+I+K+L+M+O+P+Q",
]

data_type_single = ["'label->string", "B:E->int", "G:I->int", "K:M->int", "O:Q->int"]


fields_double_sum = [
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
]


data_type_double = [
    "'label->string",
    "B:I|volume,valeur->int",
    "L:Q|volume,valeur->int",
    "T:Y|volume,valeur->int",
    "AB:AG|volume,valeur->int",
]


report = {
    "name": "sfm",
    "package": "bceao.eme.edition",
    "page": "Canevas SFM 2018",
    "width": 1920,
    "height": 140,
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
                "name": "sfm",
                "package": "bceao.eme.edition",
                "name_row": 65,
                "width_row": 66,
                "col": "A:AK",
                "fields": fields,
                "dataType": data_type,
            },
            {
                "type": "subreport",
                "structure": {
                    "name": "sfm_one",
                    "page": "Canevas SFM 2018",
                    "width": 1920,
                    "height": 140,
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
                                "package": "bceao.eme.edition",
                                "name": "sfm_one",
                                "name_row": 65,
                                "width_row": 66,
                                "col": "A:AK",
                                "fields": fields,
                                "dataType": data_type,
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
