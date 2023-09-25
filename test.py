from toolbox import jrxmlbuilder
from toolbox import xlsutil

INPUT_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/input/"
TARGET_XLS_FILE = "sfm.xlsx"
PAGE = "Canevas SFM 2018"
workbook = xlsutil.load_workbook(INPUT_PATH + TARGET_XLS_FILE)


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
# build_column_header_grouping = jrxmlbuilder.build_column_header_grouping({"row": 65, "start_col": "A", "end_col": "S"}, workbook, PAGE, 0)
# print(build_column_header_grouping)

# print("\n\n")
# print("build_column_header_basic")
# build_column_header_basic = jrxmlbuilder.build_column_header_basic({"row": 66, "start_col": "A", "end_col": "S"}, workbook, PAGE, 30)
# print(build_column_header_basic)

print("\n\n")
print("build_column_header")
build_column_header = jrxmlbuilder.build_column_header([{"group": True, "row": 65, "start_col": "A", "end_col": "S", "param": {"border": 1}}, {"row": 26, "start_col": "A", "end_col": "S", "param": {"border": 1}}], workbook, PAGE)
print(build_column_header)
