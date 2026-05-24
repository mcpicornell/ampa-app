from apps.home.ampa.entities.home_blood_pressure_registry import (
    HomeBloodPressureRegistry,
    DailyBloodPressureRecord,
    MeasurementPeriod,
    BloodPressureReading,
)

def build_fake_registry():
    return HomeBloodPressureRegistry(
        code="AMPA-TEST-001",
        patient_name="John Doe",
        date="2026-05-23",
        address="123 Main Street",
        phone_number="600123456",
        physician_name="Dr. Smith",
        pharmacist_name="Pharmacist Jane",
        daily_records=[
            DailyBloodPressureRecord(
                day=1,
                morning=MeasurementPeriod(
                    time="08:00",
                    readings=[
                        BloodPressureReading(systolic=120, diastolic=80, pulse=70),
                        BloodPressureReading(systolic=122, diastolic=82, pulse=72),
                        BloodPressureReading(systolic=121, diastolic=81, pulse=71),
                    ],
                ),
                evening=MeasurementPeriod(
                    time="20:00",
                    readings=[
                            BloodPressureReading(systolic=118, diastolic=78, pulse=68),
                            BloodPressureReading(systolic=119, diastolic=79, pulse=69),
                            BloodPressureReading(systolic=117, diastolic=77, pulse=70),
                        ],
                    ),
                ),
                DailyBloodPressureRecord(
                    day=2,
                    morning=MeasurementPeriod(
                        time="08:10",
                        readings=[
                            BloodPressureReading(systolic=125, diastolic=85, pulse=72),
                            BloodPressureReading(systolic=124, diastolic=84, pulse=73),
                            BloodPressureReading(systolic=126, diastolic=86, pulse=74),
                        ],
                    ),
                    evening=MeasurementPeriod(
                        time="20:10",
                        readings=[
                            BloodPressureReading(systolic=119, diastolic=79, pulse=69),
                            BloodPressureReading(systolic=118, diastolic=78, pulse=68),
                            BloodPressureReading(systolic=120, diastolic=80, pulse=70),
                        ],
                    ),
                ),
                DailyBloodPressureRecord(
                    day=3,
                    morning=MeasurementPeriod(
                        time="08:05",
                        readings=[
                            BloodPressureReading(systolic=118, diastolic=77, pulse=67),
                            BloodPressureReading(systolic=119, diastolic=78, pulse=68),
                            BloodPressureReading(systolic=120, diastolic=79, pulse=69),
                        ],
                    ),
                    evening=MeasurementPeriod(
                        time="20:05",
                        readings=[
                            BloodPressureReading(systolic=117, diastolic=76, pulse=66),
                            BloodPressureReading(systolic=116, diastolic=75, pulse=65),
                            BloodPressureReading(systolic=118, diastolic=77, pulse=67),
                        ],
                    ),
                ),
                DailyBloodPressureRecord(
                    day=4,
                    morning=MeasurementPeriod(
                        time="08:00",
                        readings=[
                            BloodPressureReading(systolic=122, diastolic=81, pulse=71),
                            BloodPressureReading(systolic=123, diastolic=82, pulse=72),
                            BloodPressureReading(systolic=121, diastolic=80, pulse=70),
                        ],
                    ),
                    evening=MeasurementPeriod(
                        time="20:00",
                        readings=[
                            BloodPressureReading(systolic=119, diastolic=78, pulse=68),
                            BloodPressureReading(systolic=120, diastolic=79, pulse=69),
                            BloodPressureReading(systolic=118, diastolic=77, pulse=67),
                        ],
                    ),
                ),
                DailyBloodPressureRecord(
                    day=5,
                    morning=MeasurementPeriod(
                        time="08:00",
                        readings=[
                            BloodPressureReading(systolic=121, diastolic=80, pulse=70),
                            BloodPressureReading(systolic=120, diastolic=79, pulse=69),
                            BloodPressureReading(systolic=122, diastolic=81, pulse=71),
                        ],
                    ),
                    evening=MeasurementPeriod(
                        time="20:00",
                        readings=[
                            BloodPressureReading(systolic=118, diastolic=77, pulse=67),
                            BloodPressureReading(systolic=117, diastolic=76, pulse=66),
                            BloodPressureReading(systolic=119, diastolic=78, pulse=68),
                        ],
                    ),
                ),
                DailyBloodPressureRecord(
                    day=6,
                    morning=MeasurementPeriod(
                        time="08:00",
                        readings=[
                            BloodPressureReading(systolic=123, diastolic=82, pulse=72),
                            BloodPressureReading(systolic=124, diastolic=83, pulse=73),
                            BloodPressureReading(systolic=122, diastolic=81, pulse=71),
                        ],
                    ),
                    evening=MeasurementPeriod(
                        time="20:00",
                        readings=[
                            BloodPressureReading(systolic=120, diastolic=79, pulse=69),
                            BloodPressureReading(systolic=121, diastolic=80, pulse=70),
                            BloodPressureReading(systolic=119, diastolic=78, pulse=68),
                        ],
                    ),
                ),
                DailyBloodPressureRecord(
                    day=7,
                    morning=MeasurementPeriod(
                        time="08:00",
                        readings=[
                            BloodPressureReading(systolic=119, diastolic=78, pulse=68),
                            BloodPressureReading(systolic=120, diastolic=79, pulse=69),
                            BloodPressureReading(systolic=118, diastolic=77, pulse=67),
                        ],
                    ),
                    evening=MeasurementPeriod(
                        time="20:00",
                        readings=[
                            BloodPressureReading(systolic=117, diastolic=76, pulse=66),
                            BloodPressureReading(systolic=116, diastolic=75, pulse=65),
                            BloodPressureReading(systolic=118, diastolic=77, pulse=67),
                        ],
                    ),
                ),
            ],
        )