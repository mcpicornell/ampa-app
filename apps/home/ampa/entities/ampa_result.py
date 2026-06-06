from dataclasses import dataclass


@dataclass
class DailyResult:
    morning: float
    afternoon: float


@dataclass
class BaseResult:
    systolic: float
    diastolic: float


@dataclass
class MorningResult(BaseResult):
    pass


@dataclass
class AfternoonResult(BaseResult):
    pass


@dataclass
class AmpaResult:
    morning: MorningResult
    afternoon: AfternoonResult
