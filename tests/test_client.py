import unittest
from datetime import date

import responses
from freezegun import freeze_time

from premium_bond_checker import Client
from premium_bond_checker.client import BondPeriod
from premium_bond_checker.exceptions import InvalidHolderNumberException
from premium_bond_checker.models import CheckResult, HistoryEntry, Result


class TestCheckResult(unittest.TestCase):
    def test_has_won_empty(self):
        check_result = CheckResult()
        self.assertFalse(check_result.has_won())

    def test_has_won_single(self):
        check_result = CheckResult()
        check_result.add_result(
            Result(True, "abc1", BondPeriod.THIS_MONTH, "You won", "£xx")
        )
        self.assertTrue(check_result.has_won())

    def test_has_won_mixed(self):
        check_result = CheckResult()
        check_result.add_result(
            Result(True, "abc1", BondPeriod.THIS_MONTH, "You won", "£xx")
        )
        check_result.add_result(
            Result(
                False,
                "abc2",
                BondPeriod.LAST_SIX_MONTHS,
                "You didn't win",
                "Good luck next month",
            )
        )
        self.assertTrue(check_result.has_won())

    def test_has_won_single_false(self):
        check_result = CheckResult()
        check_result.add_result(
            Result(
                False,
                "abc1",
                BondPeriod.THIS_MONTH,
                "You didn't win",
                "Good luck next month",
            )
        )
        self.assertFalse(check_result.has_won())

    def test_has_won_mixed_false(self):
        check_result = CheckResult()
        check_result.add_result(
            Result(
                False,
                "abc1",
                BondPeriod.THIS_MONTH,
                "You didn't win",
                "Good luck next month",
            )
        )
        check_result.add_result(
            Result(
                False,
                "abc2",
                BondPeriod.LAST_SIX_MONTHS,
                "You didn't win",
                "Good luck next month",
            )
        )
        self.assertFalse(check_result.has_won())


class ClientTest(unittest.TestCase):
    @responses.activate
    def test_check_valid(self):
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
        check_result = client.check("abcd")

        self.assertFalse(check_result.has_won())

        for bond_period in BondPeriod.all():
            self.assertEqual(
                "Sorry you didn't win",
                check_result.results[bond_period].header,
                "header should be 'Sorry you didn't win'",
            )
            self.assertEqual(
                "Good luck next month",
                check_result.results[bond_period].tagline,
                "tagline should be 'Good luck next month'",
            )

    @responses.activate
    def test_check_this_month_valid_no_win(self):
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
        self.assertEqual([], result.history)
        self.assertEqual(0, result.total_prize())
        self.assertEqual("Sorry you didn't win", result.header)
        self.assertEqual("Good luck next month", result.tagline)

    @responses.activate
    def test_check_this_month_valid_win(self):
        responses.add(
            responses.POST,
            "https://www.nsandi.com/premium-bonds-have-i-won-ajax",
            json={
                "status": "win",
                "header": "Congratulations!",
                "tagline": "You've won £225 in October 2026's draw",
                "holder_number": "abcd",
                "history": [
                    {
                        "prize": "100",
                        "bond_number": "111AA111111",
                        "date": "October 2026",
                    },
                    {
                        "date": "October 2026",
                        "bond_number": "222BB222222",
                        "prize": "100",
                    },
                    {
                        "date": "October 2026",
                        "bond_number": "333CC333333",
                        "prize": "25",
                    },
                ],
            },
            status=200,
        )

        result = Client().check_this_month("abcd")

        self.assertTrue(result.won)
        self.assertEqual("Congratulations!", result.header)
        self.assertEqual("You've won £225 in October 2026's draw", result.tagline)
        self.assertEqual(
            [
                HistoryEntry(100, "111AA111111", "October 2026"),
                HistoryEntry(100, "222BB222222", "October 2026"),
                HistoryEntry(25, "333CC333333", "October 2026"),
            ],
            result.history,
        )
        self.assertEqual(225, result.total_prize())

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

    @freeze_time("2025-01-01 00:00:00")
    def test_next_draw_same_month(self):
        self.assertEqual(date(2025, 1, 2), Client.next_draw())

    @freeze_time("2025-01-04 00:00:00")
    def test_next_draw_next_month(self):
        self.assertEqual(date(2025, 2, 3), Client.next_draw())

    @freeze_time("2025-01-01 00:00:00")
    def test_next_draw_reveal_by(self):
        self.assertEqual(date(2025, 1, 5), Client.next_draw_results_reveal_by())
