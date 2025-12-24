# Anveshan Project - Soil Moisture API

A Django REST Framework API for managing soil moisture data with PostgreSQL database.

## Features

- 4 unauthenticated REST API endpoints for CRUD operations
- PostgreSQL database with JSONB fields for flexible data storage
- Comprehensive logging and error handling
- Input validation and structured response formatting
- UUID primary keys
- Automatic timestamp tracking

## Requirements

- Python 3.11+
- PostgreSQL database
- Poetry (for dependency management)

## Setup Instructions

### 1. Install Dependencies

```bash
# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### 2. Database Setup

Create a PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE anveshan_db;

# Exit psql
\q
```

### 3. Environment Variables

Set the following environment variables (or use defaults):

```bash
export DB_NAME=anveshan_db
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
export SECRET_KEY=your-secret-key-here
export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Run Migrations

```bash
# Activate Poetry shell
poetry shell

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Logs Directory

```bash
mkdir -p logs
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

All endpoints are unauthenticated and return JSON responses.

### 1. GET - List All Records

**Endpoint:** `GET /api/soil-moisture/`

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Records per page (default: 100, max: 1000)

**Example Request:**
```bash
curl http://localhost:8000/api/soil-moisture/?page=1&page_size=10
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "records": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "data": {"moisture_level": 45.5, "sensor_id": "sensor_001"},
        "metadata": {"location": "field_1", "temperature": 25.3},
        "ip_address": "192.168.1.100",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 10,
      "total_count": 1,
      "total_pages": 1
    }
  },
  "message": "Records retrieved successfully"
}
```

### 2. POST - Create New Record

**Endpoint:** `POST /api/soil-moisture/create/`

**Request Body:**
```json
{
  "data": {
    "moisture_level": 45.5,
    "sensor_id": "sensor_001"
  },
  "metadata": {
    "location": "field_1",
    "temperature": 25.3
  },
  "ip_address": "192.168.1.100"
}
```

**Note:** `ip_address` is optional - if not provided, it will be extracted from the request.

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/soil-moisture/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"moisture_level": 45.5, "sensor_id": "sensor_001"},
    "metadata": {"location": "field_1"},
    "ip_address": "192.168.1.100"
  }'
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "data": {"moisture_level": 45.5, "sensor_id": "sensor_001"},
    "metadata": {"location": "field_1"},
    "ip_address": "192.168.1.100",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "message": "Record created successfully"
}
```

### 3. PUT - Update Record

**Endpoint:** `PUT /api/soil-moisture/<uuid>/update/`

**Request Body:**
```json
{
  "data": {
    "moisture_level": 50.0,
    "sensor_id": "sensor_001"
  },
  "metadata": {
    "location": "field_1",
    "temperature": 26.0
  },
  "ip_address": "192.168.1.100"
}
```

**Example Request:**
```bash
curl -X PUT http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/update/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {"moisture_level": 50.0, "sensor_id": "sensor_001"},
    "metadata": {"location": "field_1"},
    "ip_address": "192.168.1.100"
  }'
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "data": {"moisture_level": 50.0, "sensor_id": "sensor_001"},
    "metadata": {"location": "field_1"},
    "ip_address": "192.168.1.100",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
  },
  "message": "Record updated successfully"
}
```

### 4. DELETE - Delete Record

**Endpoint:** `DELETE /api/soil-moisture/<uuid>/delete/`

**Example Request:**
```bash
curl -X DELETE http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/delete/
```

**Example Response:**
```json
{
  "success": true,
  "message": "Record 550e8400-e29b-41d4-a716-446655440000 deleted successfully"
}
```

## Error Responses

All endpoints return structured error responses:

```json
{
  "success": false,
  "errors": {
    "field_name": ["Error message"]
  }
}
```

## Database Schema

### SoilMoisture Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key (auto-generated) |
| data | JSONB | Main data field (required) |
| metadata | JSONB | Optional metadata field |
| ip_address | VARCHAR(45) | IP address of data source |
| created_at | TIMESTAMP | Auto-generated on creation |
| updated_at | TIMESTAMP | Auto-updated on modification |

## Logging

Logs are written to:
- Console (stdout)
- File: `logs/django.log`

Log levels:
- `INFO`: General information and successful operations
- `WARNING`: Validation errors and non-critical issues
- `ERROR`: Exceptions and critical errors

## Validation Rules

- `data`: Must be a non-empty JSON object
- `metadata`: Must be a JSON object or null
- `ip_address`: Must be a valid IPv4 or IPv6 address
- `page`: Must be a positive integer
- `page_size`: Must be between 1 and 1000

## Development

### Running Tests

```bash
poetry run pytest
```

### Creating Superuser

```bash
python manage.py createsuperuser
```

### Accessing Admin Panel

Visit `http://localhost:8000/admin/` after creating a superuser.

## Project Structure

```
anveshan_project/
├── anveshan_project/      # Main project directory
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   └── ...
├── soil_moisture/        # Soil moisture app
│   ├── models.py         # SoilMoisture model
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── urls.py           # App URL configuration
│   └── ...
├── manage.py             # Django management script
├── pyproject.toml        # Poetry dependencies
└── README.md             # This file
```

## License

This project is for development purposes.

