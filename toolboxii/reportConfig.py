# fields: a string of special fields which requires specific treatment "A'|D=B+C|E,F,G=H+I*J|M-Z=B+a"

NAME_SPACE = "bceao.application.bean.business.report"
INPUT_XLS_FILE = "sfm.xlsx"

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
            "parent": False,
            "fields": rg_fields,
            "field_class": "basic",
            "subreports": [
                {
                    "name": "sfm_table_one_part_two",
                    "components": {
                        "type": "main",
                        "headers": "30",
                        "parent": False,
                        "fields": rg_fields_fn,
                        "field_class": "basic",
                    },
                },
                {
                    "name": "sfm_table_two_part_one",
                    "components": {
                        "type": "main",
                        "headers": "39:40",
                        "parent": False,
                        "fields": rg_fields,
                        "field_class": "basic",
                    },
                },
                {
                    "name": "sfm_table_three_part_one",
                    "components": {
                        "type": "main",
                        "headers": "49:50",
                        "parent": False,
                        "fields": rg_fields,
                        "field_class": "basic",
                    },
                },
                {
                    "name": "sfm_table_four_part_one",
                    "components": {
                        "type": "main",
                        "headers": "64:66",
                        "parent": True,
                        "fields": cmplx_fields_fn,
                        "field_class": "advanced",
                    },
                },
                {
                    "name": "sfm_table_five_part_one",
                    "components": {
                        "type": "main",
                        "headers": "110:113",
                        "parent": True,
                        "fields": cmplx_fields_fn,
                        "field_class": "advanced",
                    },
                },
                {
                    "name": "sfm_table_five_part_two",
                    "components": {
                        "type": "main",
                        "headers": "124:125",
                        "parent": True,
                        "fields": cmplx_fields_fn,
                        "field_class": "advanced",
                    },
                },
                {
                    "name": "sfm_table_six_part_one",
                    "components": {
                        "type": "main",
                        "headers": "140:143",
                        "parent": True,
                        "fields": cmplx_fields_fn,
                        "field_class": "advanced",
                    },
                },
                {
                    "name": "sfm_table_six_part_two",
                    "components": {
                        "type": "main",
                        "headers": "149:150",
                        "parent": True,
                        "fields": cmplx_fields_fn,
                        "field_class": "advanced",
                    },
                },
                {
                    "name": "sfm_table_seven_part_one",
                    "components": {
                        "type": "main",
                        "headers": "161:162",
                        "parent": False,
                        "fields": rg_fields,
                        "field_class": "basic",
                    },
                },
            ],
        }
    ],
}
