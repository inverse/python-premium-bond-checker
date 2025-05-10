from dataclasses import dataclass
from typing import Dict


@dataclass
class Result:
    won: bool
    holder_number: str
    bond_period: str
    header: str
    tagline: str


class CheckResult:
    def __init__(self):
        self.results: Dict[str, Result] = {}

    def add_result(self, result: Result):
        self.results[result.bond_period] = result

    def has_won(self) -> bool:
        return any([result.won for result in list(self.results.values())])
