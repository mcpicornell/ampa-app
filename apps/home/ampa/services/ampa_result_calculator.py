from functools import lru_cache
from typing import Literal

from ..constants import DIASTOLIC, EVENING, MORNING, SYSTOLIC
from ..entities import (
    AfternoonResult,
    AmpaResult,
    DailyResult,
    FilteredHomeBloodPressureRegistry,
    MorningResult,
)


class AmpaResultCalculator:
    def calculate(self, registry: FilteredHomeBloodPressureRegistry) -> AmpaResult:

        systolic_result = self._calculate_result(registry, SYSTOLIC)
        diastolic_result = self._calculate_result(registry, DIASTOLIC)

        return AmpaResult(
            morning=MorningResult(
                systolic=systolic_result.morning,
                diastolic=diastolic_result.morning,
            ),
            afternoon=AfternoonResult(
                systolic=systolic_result.afternoon,
                diastolic=diastolic_result.afternoon,
            ),
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
