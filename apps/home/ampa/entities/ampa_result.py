from dataclasses import dataclass


@dataclass
class SystolicResult:
    morning: float
    afternoon: float


@dataclass
class DiastolicResult:
    morning: float
    afternoon: float


@dataclass
class AmpaResult:
    systolic: SystolicResult
    diastolic: DiastolicResult
