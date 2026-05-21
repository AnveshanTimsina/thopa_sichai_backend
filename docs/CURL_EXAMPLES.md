# CURL Examples for Soil Moisture API

All endpoints are available at `http://localhost:8000/api/`

## 1. GET - Read/List All Records

### List all records (with pagination)
```bash
curl -X GET "http://localhost:8000/api/soil-moisture/" \
  -H "Content-Type: application/json"
```

### List with pagination parameters
```bash
curl -X GET "http://localhost:8000/api/soil-moisture/?page=1&page_size=10" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "records": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
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

---

## 2. POST - Create/Add New Record

### Create record with all fields
```bash
curl -X POST "http://localhost:8000/api/soil-moisture/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 45.5,
      "sensor_id": "sensor_001",
      "unit": "percentage",
      "depth": 20,
      "timestamp": "2024-01-15T10:30:00Z"
    },
    "metadata": {
      "location": "field_1",
      "coordinates": {
        "latitude": 28.6139,
        "longitude": 77.2090
      },
      "temperature": 25.3,
      "humidity": 60.0,
      "weather_condition": "sunny"
    },
    "ip_address": "192.168.1.100"
  }'
```

### Create record with minimal data (ip_address auto-extracted)
```bash
curl -X POST "http://localhost:8000/api/soil-moisture/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 38.2,
      "sensor_id": "sensor_002"
    }
  }'
```

### Create record without metadata (metadata is optional)
```bash
curl -X POST "http://localhost:8000/api/soil-moisture/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 52.8,
      "sensor_id": "sensor_003",
      "unit": "percentage"
    },
    "ip_address": "10.0.0.50"
  }'
```

### Create record with different sensor types
```bash
curl -X POST "http://localhost:8000/api/soil-moisture/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 65.3,
      "sensor_id": "sensor_004",
      "sensor_type": "capacitive",
      "voltage": 3.3,
      "reading_quality": "good"
    },
    "metadata": {
      "location": "greenhouse_2",
      "crop_type": "tomatoes",
      "irrigation_status": "active",
      "last_watered": "2024-01-15T08:00:00Z"
    },
    "ip_address": "172.16.0.25"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "data": {
      "moisture_level": 45.5,
      "sensor_id": "sensor_001",
      "unit": "percentage"
    },
    "metadata": {
      "location": "field_1",
      "temperature": 25.3
    },
    "ip_address": "192.168.1.100",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  "message": "Record created successfully"
}
```

**Note:** Save the `id` from the response - you'll need it for UPDATE and DELETE operations.

---

## 3. PUT - Update Existing Record

Replace `<RECORD_ID>` with the actual UUID from the POST response.

### Update all fields
```bash
curl -X PUT "http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/update/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 50.0,
      "sensor_id": "sensor_001",
      "unit": "percentage",
      "depth": 25,
      "timestamp": "2024-01-15T11:00:00Z"
    },
    "metadata": {
      "location": "field_1",
      "coordinates": {
        "latitude": 28.6139,
        "longitude": 77.2090
      },
      "temperature": 26.5,
      "humidity": 58.0,
      "weather_condition": "partly_cloudy"
    },
    "ip_address": "192.168.1.100"
  }'
```

### Update with new moisture reading
```bash
curl -X PUT "http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/update/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 42.1,
      "sensor_id": "sensor_001",
      "unit": "percentage",
      "alert": "low_moisture"
    },
    "metadata": {
      "location": "field_1",
      "temperature": 28.0,
      "irrigation_needed": true
    },
    "ip_address": "192.168.1.100"
  }'
```

### Update record (example with different UUID)
```bash
curl -X PUT "http://localhost:8000/api/soil-moisture/123e4567-e89b-12d3-a456-426614174000/update/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 70.5,
      "sensor_id": "sensor_005",
      "sensor_type": "tensiometer",
      "pressure": 15.2
    },
    "metadata": {
      "location": "orchard_1",
      "crop_type": "apples",
      "soil_type": "loamy",
      "ph_level": 6.5
    },
    "ip_address": "10.0.0.75"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "data": {
      "moisture_level": 50.0,
      "sensor_id": "sensor_001",
      "unit": "percentage"
    },
    "metadata": {
      "location": "field_1",
      "temperature": 26.5
    },
    "ip_address": "192.168.1.100",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  },
  "message": "Record updated successfully"
}
```

---

## 4. DELETE - Delete Record

Replace `<RECORD_ID>` with the actual UUID from the POST response.

### Delete a record
```bash
curl -X DELETE "http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/delete/" \
  -H "Content-Type: application/json"
```

### Delete another record (example)
```bash
curl -X DELETE "http://localhost:8000/api/soil-moisture/123e4567-e89b-12d3-a456-426614174000/delete/" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Record 550e8400-e29b-41d4-a716-446655440000 deleted successfully"
}
```

**Error Response (if record not found):**
```json
{
  "success": false,
  "errors": {
    "detail": "Record not found"
  }
}
```

---

## Complete Workflow Example

Here's a complete workflow from creating to deleting a record:

### Step 1: Create a new record
```bash
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
      "temperature": 25.3
    },
    "ip_address": "192.168.1.100"
  }'
```

**Response includes ID:** `550e8400-e29b-41d4-a716-446655440000`

### Step 2: Read all records to verify
```bash
curl -X GET "http://localhost:8000/api/soil-moisture/" \
  -H "Content-Type: application/json"
```

### Step 3: Update the record
```bash
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
```

### Step 4: Delete the record
```bash
curl -X DELETE "http://localhost:8000/api/soil-moisture/550e8400-e29b-41d4-a716-446655440000/delete/" \
  -H "Content-Type: application/json"
```

---

## Error Examples

### Invalid JSON data
```bash
curl -X POST "http://localhost:8000/api/soil-moisture/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": "invalid_string",
    "ip_address": "192.168.1.100"
  }'
```

**Expected Error Response:**
```json
{
  "success": false,
  "errors": {
    "data": ["Data must be a valid JSON object."]
  }
}
```

### Invalid IP address
```bash
curl -X POST "http://localhost:8000/api/soil-moisture/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 45.5
    },
    "ip_address": "invalid_ip"
  }'
```

**Expected Error Response:**
```json
{
  "success": false,
  "errors": {
    "ip_address": ["Invalid IP address format."]
  }
}
```

### Update non-existent record
```bash
curl -X PUT "http://localhost:8000/api/soil-moisture/00000000-0000-0000-0000-000000000000/update/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "moisture_level": 50.0
    },
    "ip_address": "192.168.1.100"
  }'
```

**Expected Error Response:**
```json
{
  "success": false,
  "errors": {
    "detail": "Record not found"
  }
}
```

---

## Tips

1. **Save the UUID**: After creating a record, save the `id` from the response for update/delete operations
2. **IP Address**: If you don't provide `ip_address`, it will be automatically extracted from the request
3. **Metadata**: The `metadata` field is optional and can be `null` or omitted
4. **Data Field**: Must be a non-empty JSON object
5. **Pretty Print**: Add `| jq` or `| python -m json.tool` to format JSON responses:
   ```bash
   curl -X GET "http://localhost:8000/api/soil-moisture/" | python -m json.tool
   ```

