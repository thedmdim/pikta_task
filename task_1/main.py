import json, xlsxwriter, re


class ExcelOut:
    def __init__(self, filename, headers: list = None):
        self.workbook = xlsxwriter.Workbook(filename)

    @staticmethod
    def parse_json(data):
        out = dict()
        headers = [header['properties']['QuickInfo'] for header in data['headers']]
        values = [value['properties']['Text'] for value in data['values']]

        for header in headers:
            if header == 'Сумма во ВВ':
                out.update({header:[value for value in values if re.search('\d \d\d\d,\d\d', value)]})
            elif header == 'Внутренняя валюта':
                out.update({header: [value for value in values if "RUB" in value]})
            elif header == 'Код налога':
                out.update({header: [value for value in values if "CH" in value]})
            elif header == 'Счет Главной книги':
                out.update({header: [value for value in values if re.search('\d\d-\d\d\d\d\d\d', value)]})
        return out

    def add_worksheet(self, input_json):
        worksheet = self.workbook.add_worksheet()
        with open(input_json) as file:
            data = json.loads(file.read())
        formatted_data = self.parse_json(data)
        print(formatted_data)
        for col, header in enumerate(formatted_data):
            worksheet.write(0, col, header)
            for row, value in enumerate(formatted_data[header]):
                worksheet.write(row+1, col, value)

    def write(self):
        self.workbook.close()

workbook = ExcelOut('Expenses01.xlsx')
workbook.add_worksheet("test1.json")
workbook.add_worksheet("test2.json")
workbook.add_worksheet("test3.json")
workbook.write()
