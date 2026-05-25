from functools import lru_cache

from apps.home.ampa.entities import (
    AmpaResult,
    DiastolicResult,
    FilteredHomeBloodPressureRegistry,
    SystolicResult,
)


class AmpaResultCalculator:
    def calculate(self, registry: FilteredHomeBloodPressureRegistry) -> AmpaResult:

        systolic_result = self._calculate_systolic_result(registry)
        diastolic_result = self._calculate_diastolic_result(registry)

        return AmpaResult(
            systolic=systolic_result,
            diastolic=diastolic_result,
        )

    def _calculate_systolic_result(
        self, registry: FilteredHomeBloodPressureRegistry
    ) -> SystolicResult:
        systolic_morning = self._calculate_avg(registry, "systolic", "morning")
        systolic_afternoon = self._calculate_avg(registry, "systolic", "evening")
        return SystolicResult(
            morning=systolic_morning,
            afternoon=systolic_afternoon,
        )

    def _calculate_diastolic_result(
        self, registry: FilteredHomeBloodPressureRegistry
    ) -> DiastolicResult:
        diastolic_morning = self._calculate_avg(registry, "diastolic", "morning")
        diastolic_afternoon = self._calculate_avg(registry, "diastolic", "evening")
        return DiastolicResult(
            morning=diastolic_morning,
            afternoon=diastolic_afternoon,
        )

    def _calculate_avg(
        self, registry: FilteredHomeBloodPressureRegistry, key: str, period_name: str
    ) -> float:
        values = [
            getattr(reading, key)
            for reading in self._iter_period(registry, period_name)
            if getattr(reading, key) is not None
        ]

        return sum(values) / len(values) if values else 0.0

    def _iter_period(
        self, registry: FilteredHomeBloodPressureRegistry, period_name: str
    ):
        for day in registry.daily_records:
            period = getattr(day, period_name)
            yield from period.readings


@lru_cache
def get_ampa_result_calculator():
    return AmpaResultCalculator()
