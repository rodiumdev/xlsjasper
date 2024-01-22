import openpyxl
from unidecode import unidecode

INPUT_PATH = "C:/Programming/scripts_queries/scripts/xlsjasper/input/"


def generate_column_range(start_column, end_column):
    return list(map(chr, range(ord(start_column), ord(end_column) + 1)))


def load_workbook(file_name):
    return openpyxl.load_workbook(INPUT_PATH + file_name, data_only=True)


def read_cell(workbook, page, row, col):
    workbook_page = workbook.active = workbook[page]
    cell = workbook_page[col + str(row)]

    if cell.value is None:
        return ""
    else:
        return unidecode(cell.value)  # .encode('UTF-8')
