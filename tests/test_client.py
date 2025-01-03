import unittest

import responses

from premium_bond_checker.client import BondPeriod, CheckResult, Client, Result
from premium_bond_checker.exceptions import InvalidHolderNumberException


class TestCheckResult(unittest.TestCase):
    def test_has_won_empty(self):
        check_result = CheckResult()
        self.assertFalse(check_result.has_won())

    def test_has_won_single(self):
        check_result = CheckResult()
        check_result.add_result(Result(True, "abc1", BondPeriod.THIS_MONTH, "You won", "£xx"))
        self.assertTrue(check_result.has_won())

    def test_has_won_mixed(self):
        check_result = CheckResult()
        check_result.add_result(Result(True, "abc1", BondPeriod.THIS_MONTH, "You won", "£xx"))
        check_result.add_result(Result(False, "abc2", BondPeriod.LAST_SIX_MONTHS, "You didn't win", "Good luck next month"))
        self.assertTrue(check_result.has_won())

    def test_has_won_single_false(self):
        check_result = CheckResult()
        check_result.add_result(Result(False, "abc1", BondPeriod.THIS_MONTH, "You didn't win", "Good luck next month"))
        self.assertFalse(check_result.has_won())

    def test_has_won_mixed_false(self):
        check_result = CheckResult()
        check_result.add_result(Result(False, "abc1", BondPeriod.THIS_MONTH, "You didn't win", "Good luck next month"))
        check_result.add_result(Result(False, "abc2", BondPeriod.LAST_SIX_MONTHS, "You didn't win", "Good luck next month"))
        self.assertFalse(check_result.has_won())


class ClientTest(unittest.TestCase):
    @responses.activate
    def test_check_this_month_valid(self):
        responses.add(
            responses.POST,
            "https://www.nsandi.com/premium-bonds-have-i-won-ajax",
            json={
                "status": "no_win",
                "header": "Sorry you didn't win",
                "tagline": "Good luck next month",
                "holder_number": "abcd",
                "history": [{"prize": "0", "bond_number": "0", "date": ""}],
            },
            status=200,
        )

        client = Client()
        result = client.check_this_month("abcd")

        self.assertFalse(result.won)
        self.assertEqual(result.header, "Sorry you didn't win", "header should be 'Sorry you didn't win'")
        self.assertEqual(result.tagline, "Good luck next month", "tagline should be 'Good luck next month'")

    @responses.activate
    def test_check_this_month_invalid_holder_number(self):
        responses.add(
            responses.POST,
            "https://www.nsandi.com/premium-bonds-have-i-won-ajax",
            json={
                "status": "no_win",
                "header": "Invalid holder's number",
                "tagline": "You have entered an invalid holder's number. Please check and try again.",
                "holder_number": "is invalid",
                "history": [{"prize": "0", "bond_number": "0", "date": ""}],
            },
            status=200,
        )

        client = Client()

        with self.assertRaises(InvalidHolderNumberException):
            client.check_this_month("abcd")

    @responses.activate
    def test_is_holder_number_valid_false(self):
        responses.add(
            responses.POST,
            "https://www.nsandi.com/premium-bonds-have-i-won-ajax",
            json={
                "status": "no_win",
                "header": "Invalid holder's number",
                "tagline": "You have entered an invalid holder's number. Please check and try again.",
                "holder_number": "is invalid",
                "history": [{"prize": "0", "bond_number": "0", "date": ""}],
            },
            status=200,
        )

        client = Client()

        self.assertFalse(client.is_holder_number_valid("abcd"))

    @responses.activate
    def test_is_holder_number_valid_true(self):
        responses.add(
            responses.POST,
            "https://www.nsandi.com/premium-bonds-have-i-won-ajax",
            json={
                "status": "no_win",
                "header": "Sorry you didn't win",
                "tagline": "Good luck next month",
                "holder_number": "abcd",
                "history": [{"prize": "0", "bond_number": "0", "date": ""}],
            },
            status=200,
        )

        client = Client()

        self.assertTrue(client.is_holder_number_valid("abcd"))
