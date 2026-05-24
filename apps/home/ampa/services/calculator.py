from functools import lru_cache

from apps.home.ampa.entities import (
    AmpaResult,
    DiastolicResult,
    FilteredHomeBloodPressureRegistry,
    SystolicResult,
)


class AmpaResultCalculator:
    def calculate(self, data: FilteredHomeBloodPressureRegistry) -> AmpaResult:

        systolic_result = self._calculate_systolic_result(data)
        diastolic_result = self._calculate_diastolic_result(data)

        return AmpaResult(
            systolic=SystolicResult(
                morning=systolic_result.morning,
                afternoon=systolic_result.afternoon,
            ),
            diastolic=DiastolicResult(
                morning=diastolic_result.morning,
                afternoon=diastolic_result.afternoon,
            ),
        )

    def _calculate_systolic_result(self, data):
        systolic_morning = self._calculate_avg(data, "systolic", "morning")
        systolic_afternoon = self._calculate_avg(data, "systolic", "evening")
        return SystolicResult(
            morning=systolic_morning,
            afternoon=systolic_afternoon,
        )

    def _calculate_diastolic_result(self, data):
        diastolic_morning = self._calculate_avg(data, "diastolic", "morning")
        diastolic_afternoon = self._calculate_avg(data, "diastolic", "evening")
        return DiastolicResult(
            morning=diastolic_morning,
            afternoon=diastolic_afternoon,
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
