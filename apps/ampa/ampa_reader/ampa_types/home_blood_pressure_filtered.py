from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True, slots=True)
class BloodPressureReadingFiltered:
    systolic: Optional[int] = None
    diastolic: Optional[int] = None


@dataclass(frozen=True, slots=True)
class MeasurementPeriodFiltered:
    readings: List[BloodPressureReadingFiltered]
    time: Optional[str] = None


@dataclass(frozen=True, slots=True)
class DailyBloodPressureRecordFiltered:
    day: int
    morning: MeasurementPeriodFiltered
    evening: MeasurementPeriodFiltered


@dataclass(frozen=True, slots=True)
class FilteredHomeBloodPressureRegistry:
    daily_records: List[DailyBloodPressureRecordFiltered]
    code: Optional[str] = None
    patient_name: Optional[str] = None
    date: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    physician_name: Optional[str] = None
    pharmacist_name: Optional[str] = None
