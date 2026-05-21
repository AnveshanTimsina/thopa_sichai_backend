1. Setup virtual environment
2. Activate virtual environment
3. Install dependencies with 
   - poetry install 
      (pyproject.toml)
4. Create postgres database (psql commands)
5. Update settings.py for database connection
6. Run python manage.py migrate
 (If any chaneges in models.py, run python manage.py makemigrations > python manage.py migrate)
7. python manage.py createsuperuser (Create admin user)
8. Run python manage.py runserver (Run the server)

- To add/update records, localhost:8000/admin
- For testing use following curl commands:


    GET:
    curl -X GET "http://localhost:8000/api/soil-moisture/" \  -H "Content-Type: application/json"

    POST: (Create)
    curl -X POST "http://localhost:8000/api/soil-moisture/create/" \
        -H "Content-Type: application/json" \
        -d '{
            "data": {
            "moisture_level": 45.5,
            "sensor_id": "sensor_001",
            "unit": "percentage"
            },
            "metadata": {
            "location": "field_1",
            "temperature": 25.3,
            "humidity": 60.0
            },
            "ip_address": "192.168.1.100"
        }'

  Update:
  curl -X PUT "http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/update/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 50.0,
      "sensor_id": "sensor_001",
      "unit": "percentage"
    },
    "metadata": {
      "location": "field_1",
      "temperature": 26.5
    },
    "ip_address": "192.168.1.100"
  }'

  Delete:
  curl -X DELETE "http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/delete/" \
  -H "Content-Type: application/json"