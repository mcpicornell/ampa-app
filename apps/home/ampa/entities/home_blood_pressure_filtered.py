from typing import List, Optional

from pydantic import BaseModel


class BloodPressureReadingFiltered(BaseModel):
    systolic: Optional[int] = None
    diastolic: Optional[int] = None


class MeasurementPeriodFiltered(BaseModel):
    time: Optional[str] = None
    readings: List[BloodPressureReadingFiltered]


class DailyBloodPressureRecordFiltered(BaseModel):
    day: int
    morning: MeasurementPeriodFiltered
    evening: MeasurementPeriodFiltered


class FilteredHomeBloodPressureRegistry(BaseModel):
    code: Optional[str] = None
    patient_name: Optional[str] = None
    date: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    physician_name: Optional[str] = None
    pharmacist_name: Optional[str] = None
    daily_records: List[DailyBloodPressureRecordFiltered]
