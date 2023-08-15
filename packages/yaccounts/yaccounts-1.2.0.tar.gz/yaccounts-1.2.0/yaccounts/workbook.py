import itertools
import pandas as pd

from .utils import filter_df_on_operating_units
from .worksheet import Worksheet


class Workbook:
    def __init__(self, path) -> None:
        self.analyzer = None
        self.path = path

        self.writer = pd.ExcelWriter(path, engine="xlsxwriter")
        self.workbook = self.writer.book

        self.worksheets = []

        self.format_numbers = self.workbook.add_format({"num_format": "#,##0.00"})
        self.format_titles = self.workbook.add_format(
            {"bold": True, "font_size": 16, "align": "center"}
        )

    def add_worksheet(self, name=None):
        sheet = self.workbook.add_worksheet(name)
        worksheet = Worksheet(self, sheet)
        self.worksheets.append(worksheet)
        return worksheet

    def run(self, df):
        for worksheet in self.worksheets:
            worksheet.run(filter_df_on_operating_units(df, worksheet.get_operating_units()))

        self.writer.close()

    def get_operating_units(self):
        return [ou for worksheet in self.worksheets for ou in worksheet.get_operating_units()]
