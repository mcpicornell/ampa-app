from functools import lru_cache

from ..entities import (
    AmpaResult,
    DiastolicResult,
    FilteredHomeBloodPressureRegistry,
    SystolicResult,
)


class AmpaResultCalculator:
    def calculate(self, data: FilteredHomeBloodPressureRegistry) -> AmpaResult:

        systolic_morning = self._calculate_avg(data, "systolic", "morning")
        systolic_afternoon = self._calculate_avg(data, "systolic", "evening")

        diastolic_morning = self._calculate_avg(data, "diastolic", "morning")
        diastolic_afternoon = self._calculate_avg(data, "diastolic", "evening")

        return AmpaResult(
            systolic=SystolicResult(
                morning=systolic_morning,
                afternoon=systolic_afternoon,
            ),
            diastolic=DiastolicResult(
                morning=diastolic_morning,
                afternoon=diastolic_afternoon,
            ),
        )

    def _calculate_avg(self, data, key, period_name) -> float:
        values = [
            getattr(reading, key)
            for reading in self._iter_period(data, period_name)
            if getattr(reading, key) is not None
        ]

        return sum(values) / len(values) if values else 0.0

    def _iter_period(self, data, period_name):
        for day in data.daily_records:
            period = getattr(day, period_name)
            yield from period.readings


@lru_cache
def get_ampa_result_calculator():
    return AmpaResultCalculator()
