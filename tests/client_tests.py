import unittest

from client import CheckResult, Result


class CheckResultTest(unittest.TestCase):

    def test_has_won_single(self):
        check_result = CheckResult()
        check_result.add_result(Result(True, 'abc1', 'fda1'))
        self.assertTrue(check_result.has_won())

    def test_has_won_mixed(self):
        check_result = CheckResult()
        check_result.add_result(Result(True, 'abc1', 'fda1'))
        check_result.add_result(Result(False, 'abc2', 'fda2'))
        self.assertTrue(check_result.has_won())

    def test_has_won_single_false(self):
        check_result = CheckResult()
        check_result.add_result(Result(False, 'abc1', 'fda1'))
        self.assertFalse(check_result.has_won())

    def test_has_won_mixed_false(self):
        check_result = CheckResult()
        check_result.add_result(Result(False, 'abc1', 'fda1'))
        check_result.add_result(Result(False, 'abc2', 'fda2'))
        self.assertFalse(check_result.has_won())
