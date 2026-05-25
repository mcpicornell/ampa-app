from functools import lru_cache
from typing import Literal

from apps.home.ampa.constants import DIASTOLIC, EVENING, MORNING, SYSTOLIC
from apps.home.ampa.entities import (
    AmpaResult,
    DailyResult,
    FilteredHomeBloodPressureRegistry,
)


class AmpaResultCalculator:
    def calculate(self, registry: FilteredHomeBloodPressureRegistry) -> AmpaResult:

        systolic_result = self._calculate_result(registry, SYSTOLIC)
        diastolic_result = self._calculate_result(registry, DIASTOLIC)

        return AmpaResult(
            systolic=systolic_result,
            diastolic=diastolic_result,
        )

    def _calculate_result(
        self,
        registry: FilteredHomeBloodPressureRegistry,
        key: Literal[SYSTOLIC, DIASTOLIC],
    ):
        morning = self._calculate_avg(registry, key, MORNING)
        afternoon = self._calculate_avg(registry, key, EVENING)
        return DailyResult(
            morning=morning,
            afternoon=afternoon,
        )

    def _calculate_avg(
        self,
        registry: FilteredHomeBloodPressureRegistry,
        key: Literal[SYSTOLIC, DIASTOLIC],
        period: Literal[MORNING, EVENING],
    ) -> float:
        values = [
            getattr(reading, key)
            for reading in self._iter_period(registry, period)
            if getattr(reading, key) is not None
        ]

        return sum(values) / len(values) if values else 0.0

    def _iter_period(
        self,
        registry: FilteredHomeBloodPressureRegistry,
        period: Literal[MORNING, EVENING],
    ):
        for record in registry.daily_records:
            yield from getattr(record, period).readings


@lru_cache
def get_ampa_result_calculator():
    return AmpaResultCalculator()
