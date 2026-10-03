from dataclasses import dataclass, field


@dataclass
class HistoryEntry:
    prize: int
    bond_number: str
    date: str


@dataclass
class Result:
    won: bool
    holder_number: str
    bond_period: str
    header: str
    tagline: str
    history: list[HistoryEntry] = field(default_factory=list)

    def total_prize(self) -> int:
        return sum(entry.prize for entry in self.history)


class CheckResult:
    def __init__(self):
        self.results: dict[str, Result] = {}

    def add_result(self, result: Result):
        self.results[result.bond_period] = result

    def has_won(self) -> bool:
        return any(result.won for result in self.results.values())
