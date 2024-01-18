import copy
from toolbox import jrxmlbuilder

TARGET_XLS_FILE = "sfm.xlsx"

REPORT_NAME = "sfm"
PACKAGE = "bceao.application.bean.business.report.sfm"
PAGE = "Canevas SFM 2018"

reports = [
    "sfm_table_one_part_one|s|-|25:26|A:S",
    "sfm_table_one_part_two|s|sum|30|A:S",
    "sfm_table_two_part_one|s|-|39:40|A:S",
    "sfm_table_three_part_one|s|-|49:50|A:S",
    "sfm_table_four_part_one|d|sum|64:66|A:AK",
    "sfm_table_five_part_one|d|sum|110:113|A:AK",
    "sfm_table_five_part_two|d|sum|124:125|A:AK",
    "sfm_table_six_part_one|d|sum|140:143|A:AK",
    "sfm_table_six_part_two|d|sum|149:150|A:AK",
    "sfm_table_seven_part_one|s|-|161:162|A:S",
]

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

subreport = {
    "type": "subreport",
    "structure": {
        "name": "sfm_one",
        "field_name": "field_class",
        "page": PAGE,
        "width": 2120,
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
                    "package": PACKAGE,
                    "name": "class_name",
                    "field_name": "field_class",
                    "name_row": 0,
                    "width_row": 0,
                    "col": "A:AK",
                    "fields": [],
                    "dataType": [],
                }
            ],
        },
    },
}

fields = {
    "type": "fields",
    "package": PACKAGE,
    "name": REPORT_NAME,
    "field_name": REPORT_NAME,
    "name_row": 0,
    "width_row": 0,
    "col": "A:AK",
    "fields": [],
    "dataType": [],
}

field_class = {"s": "sfm_simple", "d": "sfm_complex"}

field_column_header = []

components = []

# 0-name
# 1-type
# 2-calc
# 3-row
# 4-col
ISFIRST = True
for report in reports:
    report = report.split("|")
    target = subreport["structure"]["detail"]["components"][0]

    if ISFIRST:
        target = fields
        target["field_name"] = field_class[report[1]]

    # report name
    if not ISFIRST:
        subreport["structure"]["name"] = report[0]
        subreport["structure"]["field_name"] = field_class[report[1]]

    # headers
    row_coordinates = report[3].split(":")
    column_headers = []
    COUNT = 1
    if len(row_coordinates) < 2:
        row_range = [int(row_coordinates[0])]
    else:
        row_range = range(int(row_coordinates[0]), int(row_coordinates[1]) + 1)
    for row in row_range:
        if COUNT <= len(row_range) - 1:
            column_headers.append({"group": True, "row": row, "col": report[4]})
        else:
            column_headers.append({"row": row, "col": report[4]})
        COUNT += 1
    if ISFIRST:
        field_column_header = column_headers
    else:
        subreport["structure"]["column-header"] = column_headers

    # data name, width ,fields, type
    if not ISFIRST:
        target["name"] = report[0]
        target["field_name"] = field_class[report[1]]
    if "s" == report[1]:
        target["name_row"] = row_range[-1]
        target["width_row"] = row_range[-1]
        if "-" == report[2]:
            target["fields"] = fields_single
        else:
            target["fields"] = fields_single_sum
        target["dataType"] = data_type_single
    else:
        target["name_row"] = row_range[-2]
        target["width_row"] = row_range[-1]
        target["fields"] = fields_double_sum
        target["dataType"] = data_type_double
    target["col"] = report[4]

    if ISFIRST:
        components.append(copy.deepcopy(fields))
        # print(fields)
    else:
        components.append(copy.deepcopy(subreport))
        # print(subreport)
    ISFIRST = False


print("finished producing components")


main_report = {
    "name": REPORT_NAME,
    "package": PACKAGE,
    "field_name": "sfm_simple",
    "page": PAGE,
    "width": 2120,
    "height": 350,
    "title": {},
    "column-header": field_column_header,
    "detail": {"param": {}, "components": components},
}


print("\n\nBuilding Reports .....")
print("started")
jrxmlbuilder.build(TARGET_XLS_FILE, main_report)
print("done")
