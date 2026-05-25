from dataclasses import dataclass


@dataclass
class DailyResult:
    morning: float
    afternoon: float


@dataclass
class AmpaResult:
    systolic: DailyResult
    diastolic: DailyResult
