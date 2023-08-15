""" Unit test of yaccounts package"""

import pytest
import parametrize_from_file
import yaml

from yaccounts import CsvDataAnalyzer


@pytest.fixture(scope="class")
def aa():
    aa = CsvDataAnalyzer("data.csv")
    aa.run()
    yield aa


class TestBalances:
    @parametrize_from_file.parametrize("balances.yml")
    def test_balances(self, operating_unit, year, balance, aa):
        matches = aa.find(operating_unit, year)

        assert len(matches) == 1, f"Cannot find match for {operating_unit} {year}"
        assert round(matches[0].balance) == round(
            balance
        ), f"Balance for {operating_unit} - {year} does not match"
