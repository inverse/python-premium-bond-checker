import unittest

import responses
from premium_bond_checker.client import CheckResult, Client, Result
from premium_bond_checker.exceptions import InvalidHolderNumberException


class TestCheckResult(unittest.TestCase):
    def test_has_won_single(self):
        check_result = CheckResult()
        check_result.add_result(Result(True, "abc1", "fda1"))
        self.assertTrue(check_result.has_won())

    def test_has_won_mixed(self):
        check_result = CheckResult()
        check_result.add_result(Result(True, "abc1", "fda1"))
        check_result.add_result(Result(False, "abc2", "fda2"))
        self.assertTrue(check_result.has_won())

    def test_has_won_single_false(self):
        check_result = CheckResult()
        check_result.add_result(Result(False, "abc1", "fda1"))
        self.assertFalse(check_result.has_won())

    def test_has_won_mixed_false(self):
        check_result = CheckResult()
        check_result.add_result(Result(False, "abc1", "fda1"))
        check_result.add_result(Result(False, "abc2", "fda2"))
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
