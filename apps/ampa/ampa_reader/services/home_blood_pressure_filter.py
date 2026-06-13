from functools import lru_cache

from ..ampa_types import (
    BloodPressureReadingFiltered,
    DailyBloodPressureRecord,
    DailyBloodPressureRecordFiltered,
    FilteredHomeBloodPressureRegistry,
    HomeBloodPressureRegistry,
    MeasurementPeriod,
    MeasurementPeriodFiltered,
)


class HomeBloodPressureFilter:
    def filter(
        self, registry: HomeBloodPressureRegistry
    ) -> FilteredHomeBloodPressureRegistry:

        filtered_daily_records = self._filter_daily_records(registry.daily_records)
        return FilteredHomeBloodPressureRegistry(
            code=registry.code,
            patient_name=registry.patient_name,
            date=registry.date,
            address=registry.address,
            phone_number=registry.phone_number,
            physician_name=registry.physician_name,
            pharmacist_name=registry.pharmacist_name,
            daily_records=filtered_daily_records,
        )

    def _filter_daily_records(
        self, daily_records: list[DailyBloodPressureRecord]
    ) -> list[DailyBloodPressureRecordFiltered]:
        filtered_records = []
        for record in daily_records:
            if self._is_day_1(record.day):
                continue
            filtered_records.append(self.filter_record(record))

        return filtered_records

    def filter_record(
        self, record: DailyBloodPressureRecord
    ) -> DailyBloodPressureRecordFiltered:
        morning_filtered = self._clean_period(record.morning, is_morning=True)
        evening_filtered = self._clean_period(record.evening, is_morning=False)

        return DailyBloodPressureRecordFiltered(
            day=record.day,
            morning=morning_filtered,
            evening=evening_filtered,
        )

    def _is_day_1(self, day: int) -> bool:
        return day == 1

    def _clean_period(
        self, period: MeasurementPeriod, is_morning: bool
    ) -> MeasurementPeriodFiltered:
        cleaned_readings = []
        for idx, reading in enumerate(period.readings):
            if self._is_first_reading(idx, is_morning):
                continue

            cleaned_readings.append(
                BloodPressureReadingFiltered(
                    systolic=reading.systolic,
                    diastolic=reading.diastolic,
                )
            )

        return MeasurementPeriodFiltered(
            time=period.time,
            readings=cleaned_readings,
        )

    def _is_first_reading(self, reading_idx: int, is_morning: bool) -> bool:
        return is_morning and reading_idx == 0


@lru_cache
def get_home_blood_pressure_filter():
    return HomeBloodPressureFilter()
