from typing import List, Optional

from pydantic import BaseModel, Field


class BloodPressureReading(BaseModel):
    systolic: Optional[int] = Field(
        None, ge=30, le=250, description="Presión arterial sistólica (máxima) en mmHg"
    )

    diastolic: Optional[int] = Field(
        None, ge=30, le=250, description="Presión arterial diastólica (mínima) en mmHg"
    )

    pulse: Optional[int] = Field(
        None, ge=10, le=250, description="Pulso cardíaco en pulsaciones por minuto"
    )


class MeasurementPeriod(BaseModel):
    time: Optional[str] = Field(None, description="Hora registrada en el formulario")

    readings: List[BloodPressureReading] = Field(
        default_factory=list,
        min_length=3,
        max_length=3,
        description="Tres mediciones consecutivas",
    )


class DailyBloodPressureRecord(BaseModel):
    day: int = Field(..., ge=1, le=7, description="Número de día del registro")

    morning: MeasurementPeriod = Field(
        ..., description="Mediciones realizadas por la mañana"
    )

    evening: MeasurementPeriod = Field(
        ..., description="Mediciones realizadas por la tarde o noche"
    )


class HomeBloodPressureRegistry(BaseModel):
    code: Optional[str] = Field(None, description="Código del formulario")

    patient_name: Optional[str] = Field(None, description="Nombre del paciente")

    date: Optional[str] = Field(None, description="Fecha del registro")

    address: Optional[str] = Field(None, description="Dirección del paciente")

    phone_number: Optional[str] = Field(
        None, description="Número de teléfono del paciente"
    )

    physician_name: Optional[str] = Field(None, description="Nombre del médico")

    pharmacist_name: Optional[str] = Field(None, description="Nombre del farmacéutico")

    daily_records: List[DailyBloodPressureRecord] = Field(
        ...,
        min_length=7,
        max_length=7,
        description="Registros diarios de presión arterial durante 7 días",
    )
