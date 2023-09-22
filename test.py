from toolbox import jrxmlbuilder
from toolbox import xlsutil

INPUT_PATH = "C:/Programming/scripts_queries/scripts/jasper/input/"
TARGET_XLS_FILE = "sfm.xlsx"
PAGE = "Canevas SFM 2018"
workbook = xlsutil.load_workbook(INPUT_PATH + TARGET_XLS_FILE)


print("get_default_parameters")
get_default_parameters = jrxmlbuilder.get_default_parameters(0, "maliboy")
print(get_default_parameters)

print("\n\n")
print("build_values")
build_values = jrxmlbuilder.build_values("static", 0, "maliboy is a GOAT")
print(build_values)

print("\n\n")
print("build_column_header")
build_column_header = jrxmlbuilder.build_column_header({"row": 26, "start_col": "A", "end_col": "S"}, workbook, PAGE)
print(build_column_header)
