# Thopa Sichai — Soil Moisture IoT Platform

An end-to-end IoT demo platform developed for KU Hackfest 2025 and later improved on, that showcases a secure, production-oriented integration between ESP32 edge devices (MicroPython) and a Django REST Framework backend.

**Key highlights:**

- Device registry for multi-node deployments (auto-registration for new nodes)
- Token-based API authentication for IoT devices (`Token` header)
- Robust telemetry ingestion with JSON fields and strong validation
- Per-device actuation control (server-driven motor state)
- Defensive MicroPython client code with network and hardware failsafes

## Overview

`Thopa Sichai` collects soil moisture telemetry from distributed ESP32 devices and provides a web API for querying and controlling water pumps per device. The backend implements a `Device` registry which allows the server to manage many sensors independently.

## Architecture

- ESP32 devices run a MicroPython script (`esp32/esp32_to_django_backend.py`) that:
  - Reads ADC values, computes moisture percentage
  - Posts telemetry to `/api/soil-moisture/receive/` with `Authorization: Token <...>`
  - Polls `/api/soil-moisture/latest/?device_id=<id>` to receive motor instructions
- Django REST Framework serves the API and persists telemetry in `SoilMoisture` model records. Each reading can be tied to a `Device` model instance.

## Features

- Token authentication for IoT devices using `rest_framework.authtoken`
- Device auto-registration when telemetry includes `metadata.device_id`
- Flexible telemetry storage with `JSONField` for arbitrary sensor payloads
- Pagination, input validation, and structured API responses
- Motor decision service (`determine_motor_state`) and per-device `MotorState`

## Security and Hardening

- API access for telemetry ingestion and actuation endpoints requires DRF token authentication. Generate a token for each device and embed it in the device header: `Authorization: Token <key>`.
- Avoid placing tokens or secrets in code for production. Use environment variables or a secret manager.
- Default `DEBUG=False` for production and ensure `ALLOWED_HOSTS` and HTTPS are configured.
- Rate limiting via DRF throttle classes is enabled in `core/settings.py`.

## Setup (Local Development)

Prerequisites:

- Python 3.11+
- PostgreSQL (recommended) or default DB configured in `core/settings.py`
- Poetry (optional)

Quick start (poetry):

```bash
poetry install
poetry shell
cp .env.example .env  # adapt environment variables as needed
python manage.py migrate
python manage.py createsuperuser
mkdir -p logs
python manage.py runserver
```

Create a device token (one per physical node):

```bash
python manage.py shell
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
user = User.objects.create_user(username='esp32_device')
token = Token.objects.create(user=user)
print(token.key)
```

Use the printed key in your MicroPython device as `IOT_API_TOKEN`.

## ESP32: MicroPython usage

- Primary responsibilities:
  - Connect to Wi-Fi
  - Read ADC (calibrated) and compute moisture percentage
  - POST telemetry to `/api/soil-moisture/receive/` with `Authorization: Token <key>` and `metadata.device_id`
  - GET `/api/soil-moisture/latest/?device_id=<id>` to receive motor instructions

Example header from the device:

```
Authorization: Token <your_token_here>
```

Important: In production, set `IOT_API_TOKEN` on the device from a secure provisioning process; do not store in source control.

## Testing

Run the test suite:

```bash
python manage.py test
```

Unit tests cover the ingestion flow, device auto-registration, and motor logic.

## Project structure

See the repository for a full breakdown. Key directories:

- `core/` — Django project settings and top-level routing
- `iot/` — Application containing models, serializers, views, services, and tests
- `esp32/` — MicroPython client code used on physical ESP32 devices
- `docs/` — Additional documentation and CURL examples
