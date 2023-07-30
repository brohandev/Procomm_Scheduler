import os
from openpyxl import load_workbook
from prettyprinter import pprint as pp

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
INPUT_DOC = BASE_DIR + "/input.xlsx"


def retrieve_break_times():
    workbook = load_workbook(INPUT_DOC)
    sheet = workbook["REQUIREMENTS"]

    lunch_period = None
    tea_period = None

    # iterate over the columns in the sheet
    for column in sheet.iter_cols():
        column_name = column[0].value
        for i, cell in enumerate(column):
            # skip column name
            if i == 0:
                continue

            if column_name == "LUNCH PERIOD":
                lunch_period = cell.value
            elif column_name == "TEA PERIOD":
                tea_period = cell.value

    if lunch_period < 1 or lunch_period > 26:
        print("Please enter a valid value for lunch period in input.xslx (between 1 and 26 inclusive)")
        exit()
    if tea_period < 1 or tea_period > 26:
        print("Please enter a valid value for lunch period in input.xslx (between 1 and 26 inclusive)")
        exit()

    return lunch_period, tea_period


def retrieve_company_postcodes():
    workbook = load_workbook(INPUT_DOC)
    sheet = workbook["COMPANIES"]

    profitable_companies = []
    unprofitable_companies = []

    # iterate over the columns in the sheet
    for column in sheet.iter_cols():
        column_name = column[0].value
        for i, cell in enumerate(column):
            # skip column name
            if i == 0:
                continue

            if column_name == "MORE PROFITABLE COMPANIES":
                profitable_companies.append(cell.value)
            elif column_name == "LESS PROFITABLE COMPANIES":
                unprofitable_companies.append(cell.value)

    return list(filter(lambda elem: elem is not None, profitable_companies)), \
        list(filter(lambda elem: elem is not None, unprofitable_companies))


if __name__ == '__main__':
    profitable, unprofitable = retrieve_company_postcodes()
    lunch_period, tea_period = retrieve_break_times()

    pp(profitable)
    pp(unprofitable)

    pp(lunch_period)
    pp(tea_period)
