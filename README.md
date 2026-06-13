# AMPA - Home Blood Pressure Monitoring

Django system for processing and analyzing home blood pressure monitoring records (AMPA) with AI-powered data extraction.

## Description

This application processes home blood pressure self-monitoring records performed by patients at home over a 7-day period. The system uses Google Gemini AI to extract structured data from uploaded images, filters data according to established clinical protocols, and calculates systolic and diastolic blood pressure averages for morning and evening periods.

## Features

- **AI-powered data extraction**: Uses Google Gemini models to extract blood pressure data from uploaded images
- **Data registration**: Captures patient information (name, address, phone) and healthcare professionals (physician, pharmacist)
- **Structured measurements**: 7 days of records with 3 consecutive measurements per period (morning and evening)
- **Clinical filtering**: Applies standard filtering protocols:
  - Removes the first registration day (adaptation day)
  - Removes the first reading of each morning period
- **Average calculation**: Calculates systolic and diastolic blood pressure averages by period
- **Data validation**: Physiological range validation for blood pressure and pulse using Pydantic
- **User authentication**: Built-in authentication system for secure access
- **Session management**: 24-hour session expiry for uploaded registries

## Project Structure

```
ampa-app/
├── apps/
│   ├── authentication/               # User authentication system
│   ├── config.py                    # Apps configuration
│   ├── home/                        # Main application
│   │   ├── ampa/                    # AMPA core logic
│   │   │   ├── controller.py        # Main application controller
│   │   │   ├── constants.py         # AMPA constants
│   │   │   ├── ampa_types/           # Pydantic data models
│   │   │   │   ├── ampa_result.py
│   │   │   │   ├── home_blood_pressure_filtered.py
│   │   │   │   └── home_blood_pressure_registry.py
│   │   │   ├── services/           # Business logic
│   │   │   │   ├── agents/        # AI agents for data extraction
│   │   │   │   │   ├── ampa_reader_agent.py
│   │   │   │   │   └── prompts.py
│   │   │   │   ├── llms/          # LLM integration
│   │   │   │   │   ├── llm_factory.py
│   │   │   │   │   └── llm_with_fallback.py
│   │   │   │   ├── ampa_files_storage.py    # Image storage service
│   │   │   │   ├── ampa_result_calculator.py # Result calculation
│   │   │   │   ├── home_blood_pressure_filter.py # Data filtering
│   │   │   │   ├── local_json.py            # JSON debug service
│   │   │   │   └── utils.py                 # Service utilities
│   │   │   └── utils.py             # General utilities
│   │   ├── config.py                # Home app configuration
│   │   ├── management/              # Django management commands
│   │   │   └── commands/
│   │   ├── migrations/              # Database migrations
│   │   ├── views/                   # Django views
│   │   │   ├── ampa.py             # AMPA upload and result views
│   │   │   ├── index.py            # Index view
│   │   │   └── pages.py            # Page views
│   │   ├── admin.py                 # Django admin configuration
│   │   ├── models.py                # Django models
│   │   ├── tests.py                 # Test suite
│   │   └── urls.py                  # URL routing
│   ├── static/                     # Static assets
│   └── templates/                  # HTML templates
├── core/                           # Django configuration
│   ├── settings.py                 # Django settings
│   ├── urls.py                    # Main URL configuration
│   ├── asgi.py                    # ASGI configuration
│   └── wsgi.py                    # WSGI configuration
├── json_tests/                     # JSON debug files (local only)
├── media/                          # User uploaded media
├── nginx/                          # Nginx configuration
├── CHANGELOG.md                    # Project changelog
├── Dockerfile                      # Container image
├── Procfile                        # Heroku/Procfile configuration
├── docker-compose.yml              # Docker configuration
├── podman-compose.yml             # Podman configuration
├── gunicorn-cfg.py                # Gunicorn configuration
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Python runtime version
├── manage.py                      # Django management script
├── .env                           # Environment variables (local)
├── .env.local                     # Local environment variables
└── .example.env                   # Example environment variables
```

## Data Models

### BloodPressureReading
Individual blood pressure reading (Pydantic model):
- `systolic`: Systolic pressure (30-250 mmHg)
- `diastolic`: Diastolic pressure (30-250 mmHg)
- `pulse`: Heart rate (10-250 bpm)

### MeasurementPeriod
Measurement period with up to 3 consecutive readings:
- `time`: Measurement time
- `readings`: List of up to 3 readings

### DailyBloodPressureRecord
Daily record:
- `day`: Day number (1-7)
- `morning`: Morning measurements
- `evening`: Evening/night measurements

### HomeBloodPressureRegistry
Complete patient registry:
- `code`: Form code
- `patient_name`: Patient name
- `date`: Registration date
- `address`: Patient address
- `phone_number`: Patient phone
- `physician_name`: Physician name
- `pharmacist_name`: Pharmacist name
- `daily_records`: 7 days of daily records

### AmpaResult
Processing result (dataclass):
- `morning`: MorningResult with systolic and diastolic averages
- `afternoon`: AfternoonResult with systolic and diastolic averages

## Processing Flow

1. **File upload**: User uploads an image of the AMPA form
2. **AI extraction**: `AmpaReaderAgent` uses Google Gemini AI to extract structured data from the image
3. **Data validation**: Extracted data is validated using Pydantic models
4. **Filtering**: `HomeBloodPressureFilter` is applied:
   - Day 1 is removed (adaptation period)
   - First reading of each morning is removed
5. **Calculation**: `AmpaResultCalculator` is applied:
   - Systolic and diastolic averages are calculated
   - Results are separated by period (morning/evening)
6. **Result**: An `AmpaResult` with calculated averages is returned and displayed

## Installation

### Prerequisites
- Python 3.13+ (local development)
- Python 3.9 (production deployment)
- Google API Key for Gemini AI models

### Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .example.env .env
# Edit .env and add your GEMINI_API_KEY

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Login or register an account
3. Upload an image of the AMPA blood pressure monitoring form
4. View the calculated results with morning and evening averages

### Controller usage example:

```python
from apps.home.ampa import (
    AmpaFileControllerDependencies,
    get_ampa_file_controller,
    get_ampa_images_storage,
    get_ampa_reader_agent,
    get_ampa_result_calculator,
    get_gemini_policy,
    get_home_blood_pressure_filter,
    get_local_json_service,
)
from zoneinfo import ZoneInfo

controller = get_ampa_file_controller(
    AmpaFileControllerDependencies(
        storage_service=get_ampa_images_storage(),
        local_json_service=get_local_json_service("json_tests"),  # Optional: set to None for production
        filter_service=get_home_blood_pressure_filter(),
        calculator=get_ampa_result_calculator(),
        ampa_reader_agent=get_ampa_reader_agent(
            models=("gemini-2.5-flash",),
            api_key="your-google-api-key",
            llm_policy=get_gemini_policy(ZoneInfo("America/Los_Angeles")),
        ),
    )
)

# Save and process AMPA file
registry_id = controller.save_ampa_file(file)

# Calculate AMPA result
result = controller.calculate_ampa_result(registry_id)
print(f"Morning systolic: {result.morning.systolic}")
print(f"Morning diastolic: {result.morning.diastolic}")
print(f"Afternoon systolic: {result.afternoon.systolic}")
print(f"Afternoon diastolic: {result.afternoon.diastolic}")
```

## Technologies

- **Django 5.2.1**: Web framework
- **Python 3.13+**: Development environment
- **Pydantic 2.13.4**: Data validation and models
- **Google Gemini AI**: AI-powered data extraction
- **LangChain**: LLM integration framework
  - langchain-google-genai 4.2.3
  - langchain-core 1.4.0
- **SQLite**: Database (configurable via dj-database-url)
- **Gunicorn 23.0.0**: WSGI HTTP server
- **Uvicorn 0.34.0**: ASGI server
- **WhiteNoise 6.9.0**: Static file serving
- **python-decouple 3.8**: Configuration management

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
SERVER=127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
GEMINI_API_KEY=your-google-api-key
LLM_MODEL=gemini-2.5-flash
ENVIRONMENT=prod
```

### Available Gemini Models
- gemini-3.1-flash-lite
- gemini-2.5-flash-lite
- gemini-3.5-flash
- gemini-2.5-flash

## Deployment

### Docker

```bash
# Build and run with Docker
docker-compose up --build

# The application will be available at http://localhost:8008
```

## Configuration

### Environment
Set `ENVIRONMENT=local` in `.env` to enable JSON debug files. When set to `local`, processed data will be saved to the `json_tests/` directory for debugging purposes. In production (`ENVIRONMENT=prod`), JSON files are not saved.

### Session Management
Sessions expire after 24 hours (configurable via `SESSION_EXPIRANCY` in settings).

## License

See LICENSE.md file for more information.
