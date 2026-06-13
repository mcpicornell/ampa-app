from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DailyResult:
    morning: float
    afternoon: float


@dataclass(frozen=True, slots=True)
class BaseResult:
    systolic: float
    diastolic: float


@dataclass(frozen=True, slots=True)
class MorningResult(BaseResult):
    pass


@dataclass(frozen=True, slots=True)
class AfternoonResult(BaseResult):
    pass


@dataclass(frozen=True, slots=True)
class AmpaResult:
    morning: MorningResult
    afternoon: AfternoonResult
