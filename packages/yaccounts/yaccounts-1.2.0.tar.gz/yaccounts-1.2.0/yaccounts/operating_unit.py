import calendar
from collections import defaultdict
import enum
import re
import numpy as np

import pandas as pd

from .config import *


class OperatingUnitType(enum.Enum):
    PROJECT = 0
    FUND_11 = 1
    ACTUALS = 2


class OperatingUnit:
    def __init__(
        self,
        worksheet,
        operating_unit,
        year,
        name=None,
        fund_type=None,
        student_aid=None,
        hide_student_wages=False,
        hide_details=True,
    ) -> None:
        self.worksheet = worksheet
        self.operating_unit = str(operating_unit)
        self.name = name
        self.year = year
        self.student_aid = student_aid
        self.hide_student_wages = hide_student_wages
        self.hide_details = hide_details

        if fund_type is None:
            if self.operating_unit.startswith("R"):
                self.type = OperatingUnitType.PROJECT
            elif self.operating_unit.startswith("11"):
                self.type = OperatingUnitType.FUND_11
            else:
                self.type = OperatingUnitType.ACTUALS

        # Create a new dataframe with months of the year as column headers
        self.df_gen = pd.DataFrame(
            columns=("Type", *[calendar.month_abbr[i] for i in range(1, 13)])
        )

        self.row_colors = {}
        self.hidden_rows = []
        self.no_sum_rows = []

        self.df = None

        if self.type == OperatingUnitType.PROJECT:
            self.previous_expenditures = self.analyzer.get_previous_expenditures(
                self.operating_unit, self.year - 1
            )

    def run(self, df):
        self.df = df
        if self.year:
            # Filter df on 'Fiscal Year' column
            self.df = self.df[self.df["Fiscal Year"] == self.year]

        if self.type in (OperatingUnitType.PROJECT, OperatingUnitType.FUND_11):
            self.verify_no_income()
        else:
            self.filter_out_budgeted_data()

        print(
            f"Running Operating Unit:{self.operating_unit} {('(' + str(self.year) + ')') if self.year else ''}",
        )

        # Add student wage data
        self.add_row("Student Wages", CODES_STUDENT_WAGES, color=COLOR_STUDENT_WAGES)
        self.create_student_wages()
        self.add_row("Student Tuition", CODES_STUDENT_TUITION, color=COLOR_STUDENT_TUITION)
        self.add_row("Faculty Spr/Sum", CODES_FACULTY_SPRING_SUMMER, color=COLOR_FACULTY)
        self.add_row("Travel", CODES_TRAVEL, color=COLOR_TRAVEL)
        self.add_detailed_rows(
            CODES_TRAVEL, ("Account Descr", "PINV Business Purpose", "JRNL Line Descr", "JH Descr")
        )

        self.add_row("Supplies/Misc", CODES_SUPPLIES, color=COLOR_SUPPLIES)
        self.add_detailed_rows(
            CODES_SUPPLIES,
            (
                "Account Descr",
                "Class Descr",
                "PINV Business Purpose",
                "JRNL Line Descr",
                "PINV Supplier Name",
            ),
        )

        self.add_row("Capital Equipment", CODES_CAPITAL, color=COLOR_CAPITAL)
        self.add_detailed_rows(
            CODES_CAPITAL,
            (
                "Account Descr",
                "Class Descr",
                "PINV Business Purpose",
                "JRNL Line Descr",
                "PINV Supplier Name",
            ),
        )

        self.add_row("Overhead", CODES_OVERHEAD, color=COLOR_OVERHEAD)
        self.row_total_expenses = self.add_row(
            "Total Expeneses", all_expense_codes(), color=COLOR_TOTAL_EXPENSES
        )

        self.add_empty_row()

        if self.type == OperatingUnitType.ACTUALS:
            self.add_row("Interest", CODES_INTEREST, actuals_coeff=-1)

        income_row_name = "Transfer Income / Carryover"
        if self.type == OperatingUnitType.PROJECT:
            income_row_name = "New Budgets or Carryover"
        elif self.type == OperatingUnitType.FUND_11:
            income_row_name = "New Budgets"

        self.add_row(
            income_row_name,
            CODES_INCOME,
            budgets_coeff=1,
            actuals_coeff=-1,
        )

        self.row_total_income = self.add_row(
            "Total Income",
            CODES_INTEREST + CODES_INCOME,
            color=COLOR_TOTAL_INCOME,
            budgets_coeff=1,
            actuals_coeff=-1,
        )
        self.add_empty_row()

        # Add a sum column that sums the values in each row, starting with the 2nd column,
        # skipping rows where "Type" is empty

        # Calculate the sum for rows where 'Type' column is not empty
        columns_to_sum = self.df_gen.columns[1:]  # Get all columns starting from the second column
        self.df_gen["Sum"] = self.df_gen.loc[
            ~self.df_gen.index.isin(self.no_sum_rows), columns_to_sum
        ].sum(axis=1)

        # Save total expenses, which is found in the self.row_total_expenses, "Sum" column
        self.total_expenses = self.df_gen.iloc[self.row_total_expenses]["Sum"]

        self.add_balance_row()
        self.add_empty_row()

        title_name = self.operating_unit
        if self.name:
            title_name = f"{self.name} ({title_name})"
        if self.year:
            title_name = f"{title_name} - {self.year}"
        self.worksheet.write_to_sheet(self.df_gen, title_name, self.hidden_rows, self.row_colors)

    def add_empty_row(self):
        # Add an empty row of None values
        empty_data = {
            "Type": [""],
            **{calendar.month_abbr[month]: [np.nan] for month in range(1, 13)},
        }

        self.df_gen = pd.concat((self.df_gen, pd.DataFrame(empty_data)), ignore_index=True)
        self.no_sum_rows.append(len(self.df_gen) - 1)

    def add_row(
        self,
        row_name,
        account_codes,
        budgets_coeff=0,
        actuals_coeff=1,
        color=None,
    ):
        """Sum the values in the 'Amount' column for each month in the given account codes.
        If actual=True, then only actual values will be summed.
        Otherwise budgeted (account income) values will be summed."""

        new_row_data = {
            "Type": [row_name],
            **{
                calendar.month_abbr[month]: [
                    budgets_coeff
                    * (
                        self.df.loc[
                            (self.df["Accounting Period"] == month)
                            & (self.df["JRNL Line Ledger"] == "BUDGETS")
                        ][COL_NAME_AMOUNT].sum()
                    )
                    + actuals_coeff
                    * (
                        self.df.loc[
                            (self.df["Accounting Period"] == month)
                            & self.df["Account"].isin(account_codes)
                            & (self.df["JRNL Line Ledger"] == "ACTUALS")
                        ][COL_NAME_AMOUNT].sum()
                    )
                ]
                for month in range(1, 13)
            },
        }

        # Add this dictionary to the dataframe
        self.df_gen = pd.concat((self.df_gen, pd.DataFrame(new_row_data)), ignore_index=True)

        if color:
            self.row_colors[len(self.df_gen)] = color

        return self.df_gen.tail(1).index[0]

    def add_balance_row(self):
        if self.type == OperatingUnitType.PROJECT:
            prev_expenditures_row = len(self.df_gen)
            self.df_gen.loc[prev_expenditures_row] = {
                "Type": "Previous Expenditures",
                calendar.month_abbr[1]: self.previous_expenditures,
            }

        # Create student aid rows
        if self.student_aid:
            student_aid_row = len(self.df_gen)
            self.df_gen.loc[student_aid_row, "Type"] = "Student aid"

            non_student_aid_row = len(self.df_gen)
            self.df_gen.loc[non_student_aid_row, "Type"] = "Non-student aid"

        # Create balance row
        balance_row = len(self.df_gen)
        self.df_gen.loc[balance_row] = {"Type": "Balance (end of month)"}

        # # Iterate through columns and calcuate the balance, which is the total income minus the total expenses
        for month in range(1, 13):
            income = self.df_gen.iloc[self.row_total_income][month]
            expenses = self.df_gen.iloc[self.row_total_expenses][month]

            if month > 1:
                prev_balance = self.df_gen.iloc[balance_row, month - 1]
            elif self.type == OperatingUnitType.PROJECT:
                prev_balance = -self.df_gen.iloc[prev_expenditures_row, month]
            else:
                prev_balance = 0

            balance = income - expenses + prev_balance
            self.df_gen.iloc[len(self.df_gen) - 1, month] = balance
            if month == 12:
                self.balance = balance

            # Fill in student aid balances
            if self.student_aid:
                student_expenses = self.analyzer.get_previous_expenditures_student_aid(
                    self.operating_unit, self.year, month
                )
                student_aid_balance = self.student_aid - student_expenses
                self.df_gen.iloc[student_aid_row, month] = student_aid_balance
                self.df_gen.iloc[non_student_aid_row, month] = balance - student_aid_balance

        self.row_colors[len(self.df_gen)] = "yellow"

    def create_student_wages(self):
        # Filter to only student wages ('Account' column in STUDENT_WAGES)
        df_students = self.df[
            (self.df["Account"].isin(CODES_STUDENT_WAGES))
            & (self.df["JRNL Line Ledger"] == "ACTUALS")
        ]

        # Get unique list of value in 'JRNL Line Descr' column
        students_raw = df_students["JRNL Line Descr"].unique()
        self.students = defaultdict(list)
        for student in students_raw:
            names = re.split(", |,| ", student)
            # if not match:
            #     raise Exception(f"Could not parse student name: {student}")
            if len(names) > 1:
                student_key = f"{names[1].title()} {names[0].title()}"
            else:
                student_key = names[0]
            self.students[student_key].append(student)

        for student in self.students.copy():
            non_person = any(word in student.lower() for word in ("benefit", "overspent"))

            if non_person:
                self.students["<" + student + ">"] = self.students.pop(student)

        sorted_students = sorted(self.students.keys(), key=lambda x: (x.startswith("<"), x))
        # Create a new dictionary with the student wages by month
        student_data = {
            "Type": [f"  {s}" for s in sorted_students],
            **{
                calendar.month_abbr[month]: [
                    df_students.loc[
                        (df_students["Accounting Period"] == month)
                        & (df_students["JRNL Line Descr"].isin(self.students[student]))
                    ]["JRNL Monetary Amount -no scrn aggregation"].sum()
                    for student in sorted_students
                ]
                for month in range(1, 13)
            },
        }
        self.df_gen = pd.concat((self.df_gen, pd.DataFrame(student_data)), ignore_index=True)

        # Add new row index to hidden rows
        if self.hide_student_wages:
            self.hidden_rows.extend(
                range(len(self.df_gen) - len(student_data["Type"]) + 1, len(self.df_gen) + 1)
            )

    def add_detailed_rows(self, codes, detail_cols):
        # Filter to only travel expenses ('Account' column in TRAVEL)
        df_travel = (
            self.df[(self.df["Account"].isin(codes)) & (self.df["JRNL Line Ledger"] == "ACTUALS")]
            .rename_axis("index")
            .sort_values(by=["Accounting Period", "index"])
        )

        for index, row in df_travel.iterrows():
            data = {
                "Type": [
                    f"  Line {index+2}: {(' - '.join(str('' if pd.isnull(row[col_name]) else row[col_name] ) for col_name in detail_cols))}"
                ],
                **{
                    calendar.month_abbr[month]: (
                        row[COL_NAME_AMOUNT] if month == row["Accounting Period"] else 0
                    )
                    for month in range(1, 13)
                },
            }
            self.df_gen = pd.concat((self.df_gen, pd.DataFrame(data)), ignore_index=True)
            # self.no_sum_rows.append(len(self.df_gen) - 1)
            if self.hide_details:
                self.hidden_rows.append(len(self.df_gen))

    def verify_no_income(self):
        # Ensure df contains no CODES_INCOME
        if self.df[self.df["Account"].isin(CODES_INCOME + CODES_INTEREST)].shape[0] > 0:
            print(self.df[self.df["Account"].isin(CODES_INCOME + CODES_INTEREST)])
            raise Exception(
                f"Budgeted account {self.operating_unit} contains income. "
                "Budgeted accounts should only contain expenses."
            )

    def filter_out_budgeted_data(self):
        # Filter out budgeted data.  Only include ACTUALS or BUDGET with code in CODES_NON_BUDGETED_BUDGET_CODES
        self.df = self.df[
            (
                (self.df["JRNL Line Ledger"] == "ACTUALS")
                | (
                    (self.df["JRNL Line Ledger"] == "BUDGETS")
                    & (self.df["Account"].isin(CODES_NON_BUDGETED_BUDGET_CODES))
                )
            )
        ]

    @property
    def analyzer(self):
        return self.worksheet.workbook.analyzer
