import openpyxl
import decimal
from unidecode import unidecode


def generate_column_range(start_column, end_column):
    return list(map(chr, range(ord(start_column), ord(end_column) + 1)))


def load_workbook(xls_file_path):
    return openpyxl.load_workbook(xls_file_path, data_only=True)


def dropzeros(number):
    mynum = decimal.Decimal(number).normalize()
    return mynum.__trunc__() if not mynum % 1 else float(mynum)


def load_cell(workbook, page, row, col):
    workbook_page = workbook.active = workbook[page]
    cell = workbook_page[col + row]

    if cell.value is None:
        return "0"
    else:
        return str(dropzeros(cell.value))


def load_cell_string(workbook, page, row, col):
    workbook_page = workbook.active = workbook[page]
    cell = workbook_page[col + row]

    if cell.value is None:
        return ""
    else:
        return unidecode(cell.value)  # .encode('UTF-8')


def read_cell(workbook, page, row, col):
    workbook_page = workbook.active = workbook[page]
    cell = workbook_page[col + str(row)]

    if cell.value is None:
        return ""
    else:
        return unidecode(cell.value)  # .encode('UTF-8')


def read_cell(workbook, page, row, col):
    workbook_page = workbook.active = workbook[page]
    cell = workbook_page[col + str(row)]

    if cell.value is None:
        return ""
    else:
        return unidecode(cell.value)  # .encode('UTF-8')
