class PremiumBondCheckerException(Exception):
    pass


class InvalidHolderNumberException(PremiumBondCheckerException):
    pass


class TimeoutException(PremiumBondCheckerException):
    pass


class ConnectionException(PremiumBondCheckerException):
    pass
