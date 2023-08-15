import datetime
import matplotlib
from .utils import ensure_tuple, filter_df_on_operating_units
from .operating_unit import OperatingUnit


class Worksheet:
    def __init__(self, workbook, sheet) -> None:
        self.workbook = workbook
        self.operating_units = []
        self.sheet = sheet
        self.next_start_row = 0

    def add_operating_unit(self, operating_unit, name=None, year=None, **options):
        if year is None:
            # Get all years for this operating unit from the dataframe
            years = sorted(
                self.workbook.analyzer.df[
                    self.workbook.analyzer.df["Operating Unit"] == str(operating_unit)
                ]["Fiscal Year"].unique()
            )
        else:
            years = ensure_tuple(year)

        for year in years:
            self.operating_units.append(
                OperatingUnit(self, operating_unit, year, name=name, **options)
            )

    def format_cell(self, row, col, format):
        self.sheet.conditional_format(row, col, row, col, {"type": "no_errors", "format": format})

    def format_row(self, row, format):
        self.sheet.conditional_format(row, 0, row, 13, {"type": "no_errors", "format": format})
        #     sheet.write_blank(row, i, sheet[row, i].value, color)

    def get_operating_units(self):
        return [ou.operating_unit for ou in self.operating_units]

    def run(self, df):
        for operating_uint in self.operating_units:
            operating_uint.run(filter_df_on_operating_units(df, (operating_uint.operating_unit,)))

        # Set the width of column 0 to 20
        self.sheet.set_column(0, 13, 20)

        self.sheet.set_column(1, 12, 11, cell_format=self.workbook.format_numbers)

        self.sheet.set_column(13, 13, 12, cell_format=self.workbook.format_numbers)

    def write_to_sheet(self, df, title_name, hidden_rows=(), row_colors={}):
        df.to_excel(
            self.workbook.writer,
            startrow=self.next_start_row + 1,
            index=False,
            sheet_name=self.sheet.name,
        )

        self.sheet.merge_range(
            self.next_start_row,
            0,
            self.next_start_row,
            13,
            title_name,
            cell_format=self.workbook.format_titles,
        ),

        # Hide rows
        for row in hidden_rows:
            self.sheet.set_row(self.next_start_row + row + 1, options={"hidden": True})

        # Color rows
        for row in row_colors:
            fmt = self.workbook.workbook.add_format(
                {"bg_color": matplotlib.colors.cnames[row_colors[row]]}
            )
            self.format_row(self.next_start_row + row + 1, fmt)

        self.next_start_row += len(df.index) + 2
