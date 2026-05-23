# AMPA - Home Blood Pressure Monitoring

Django system for processing and analyzing home blood pressure monitoring records (AMPA).

## Description

This application processes home blood pressure self-monitoring records performed by patients at home over a 7-day period. The system filters data according to established clinical protocols and calculates systolic and diastolic blood pressure averages for morning and evening periods.

## Features

- **Data registration**: Captures patient information (name, address, phone) and healthcare professionals (physician, pharmacist)
- **Structured measurements**: 7 days of records with 3 consecutive measurements per period (morning and evening)
- **Clinical filtering**: Applies standard filtering protocols:
  - Removes the first registration day (adaptation day)
  - Removes the first reading of each morning period
- **Average calculation**: Calculates systolic and diastolic blood pressure averages by period
- **Data validation**: Physiological range validation for blood pressure and pulse

## Project Structure

```
apps/home/ampa/
├── controller.py                      # Main application controller
├── entities/                          # Data models
│   ├── ampa_result.py                # AMPA calculation results
│   ├── home_blood_pressure_registry.py  # Blood pressure registry
│   └── home_blood_pressure_filtered.py   # Filtered registry
└── services/                          # Business logic
    ├── calculator.py                 # Average calculation
    ├── filter.py                     # Data filtering
    └── upload.py                     # File upload
```

## Data Models

### BloodPressureReading
Individual blood pressure reading:
- `systolic`: Systolic pressure (50-300 mmHg)
- `diastolic`: Diastolic pressure (30-200 mmHg)
- `pulse`: Heart rate (20-250 bpm)

### MeasurementPeriod
Measurement period with 3 consecutive readings:
- `time`: Measurement time
- `readings`: List of 3 readings

### DailyBloodPressureRecord
Daily record:
- `day`: Day number (1-7)
- `morning`: Morning measurements
- `evening`: Evening/night measurements

### HomeBloodPressureRegistry
Complete patient registry:
- Patient demographic information
- Healthcare professional information
- 7 days of daily records

### AmpaResult
Processing result:
- `systolic`: Systolic averages (morning/evening)
- `diastolic`: Diastolic averages (morning/evening)

## Processing Flow

1. **Data reception**: Controller receives a `HomeBloodPressureRegistry`
2. **Filtering**: `HomeBloodPressureFilter` is applied:
   - Day 1 is removed (adaptation period)
   - First reading of each morning is removed
3. **Calculation**: `AmpaResultCalculator` is applied:
   - Systolic and diastolic averages are calculated
   - Results are separated by period (morning/evening)
4. **Result**: An `AmpaResult` with calculated averages is returned

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

## Usage

### Controller usage example:

```python
from apps.home.ampa.controller import get_ampa_file_controller

controller = get_ampa_file_controller()

# Calculate AMPA result from data
result = controller.calculate_ampa_result(data_dict)
print(f"Morning systolic: {result.systolic.morning}")
print(f"Evening diastolic: {result.diastolic.afternoon}")
```

## Technologies

- **Django 3.2.6 LTS**: Web framework
- **Pydantic**: Data validation and models
- **SQLite**: Database (configurable)

## License

See LICENSE.md file for more information.
