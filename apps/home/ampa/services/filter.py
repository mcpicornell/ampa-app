from functools import lru_cache

from ..entities import (
    BloodPressureReadingFiltered,
    DailyBloodPressureRecordFiltered,
    FilteredHomeBloodPressureRegistry,
    HomeBloodPressureRegistry,
    MeasurementPeriodFiltered,
)


class HomeBloodPressureFilter:
    def filter(
        self, data: HomeBloodPressureRegistry
    ) -> FilteredHomeBloodPressureRegistry:

        filtered_days = []

        for day in data.daily_records:
            if self._is_day_1(day):
                continue

            morning_filtered = self._clean_period(day.morning, is_morning=True)

            evening_filtered = self._clean_period(day.evening, is_morning=False)

            filtered_days.append(
                DailyBloodPressureRecordFiltered(
                    day=day.day,
                    morning=morning_filtered,
                    evening=evening_filtered,
                )
            )

        return FilteredHomeBloodPressureRegistry(
            code=data.code,
            patient_name=data.patient_name,
            date=data.date,
            address=data.address,
            phone_number=data.phone_number,
            physician_name=data.physician_name,
            pharmacist_name=data.pharmacist_name,
            daily_records=filtered_days,
        )

    def _clean_period(self, period, is_morning):

        cleaned_readings = []

        for idx, reading in enumerate(period.readings):
            if is_morning and idx == 0:
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

    def _is_day_1(self, day):
        return day.day == 1


@lru_cache
def get_home_blood_pressure_filter():
    return HomeBloodPressureFilter()
