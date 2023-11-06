from toolbox import jrxmlbuilder
from toolbox import xlsutil
from toolbox import utils

INPUT_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/input/"
TARGET_XLS_FILE = "sfm.xlsx"
PAGE = "Canevas SFM 2018"
workbook = xlsutil.load_workbook(INPUT_PATH + TARGET_XLS_FILE)


# print("\n\n")
# print("to_java_variable")
# to_java_variable = utils.to_java_variable("Année N-1 (2017) (mensuel)")
# print(to_java_variable)

# print("\n\n")
# print("expand_column")
# expand_column = jrxmlbuilder.expand_column("A:A")
# print(expand_column)

# print("\n\n")
# print("get_default_parameters")
# get_default_parameters = jrxmlbuilder.get_default_parameters(0, "maliboy")
# print(get_default_parameters)

# print("\n\n")
# print("get_grouping_value_and_width")
# get_grouping_value_and_width = jrxmlbuilder.get_grouping_value_and_width(["A", "B", "C", "D", "E"], workbook, PAGE, 65)
# print(get_grouping_value_and_width)

# print("\n\n")
# print("build_values")
# build_values = jrxmlbuilder.build_values("static", 0, "maliboy is a GOAT")
# print(build_values)

# print("\n\n")
# print("build_column_header_grouping")
# build_column_header_grouping = jrxmlbuilder.build_column_header_grouping({"row": 65, "col": "A:S"}, workbook, PAGE, 0)
# print(build_column_header_grouping)

# print("\n\n")
# print("build_column_header_basic")
# build_column_header_basic = jrxmlbuilder.build_column_header_basic({"row": 66, "col":"A:S"}, workbook, PAGE, 30)
# print(build_column_header_basic)

# print("\n\n")
# print("build_column_header")
# build_column_header = jrxmlbuilder.build_column_header([{"group": True, "row": 65, "col":"A:S", "param": {"border": 1}}, {"row": 26, "col":"A:S", "param": {"border": 1}}], workbook, PAGE)
# print(build_column_header)

print("\n\n")
print("get_field_names")
get_field_names = jrxmlbuilder.get_field_names(workbook, PAGE, 65, "A:AK")
print(get_field_names)

# print("\n\n")
# print("build_fields")
# build_fields = jrxmlbuilder.build_fields(workbook, PAGE, {"type": "fields", "name_row": 65, "width_row": 66, "col": "A:S", "fields": ["'label", "B:C", "D:E|volume,valuer", "A+B+C"]}, 0)
# print(build_fields)

# print("\n\n")
# print("expand_fields")
# expand_fields = jrxmlbuilder.expand_fields(["'label", "A:B", "C:E|volume,valeur", "A+B+C"])
# # expand_fields = jrxmlbuilder.expand_fields(["'label"])
# print(expand_fields)

print("\n\n")
print("expand_data_type")
expand_data_type = jrxmlbuilder.expand_data_type(
    [
        "'label->string",
        "B:I|volume,valeur->int",
        "L:Q|volume,valeur->int",
        "T:Y|volume,valeur->int",
        "AB:AG|volume,valeur->int",
    ],
    get_field_names,
)
print(expand_data_type)


# print(jrxmlbuilder.expand_column("BA:DE"))
