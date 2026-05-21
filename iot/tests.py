from django.test import TestCase
from rest_framework.test import APIClient
from .models import SoilMoisture

class ESP32IntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_esp32_receive_iot(self):
        # We now send a float percentage (e.g., 43.3) to mimic the new hardware ADC conversion
        payload = {
            "data": {"moisture_level": 43.3},
            "metadata": {"location": "ku"},
            "ip_address": "192.168.1.10" 
        }
        
        response = self.client.post(
            '/api/soil-moisture/receive/', 
            payload, 
            format='json', 
            REMOTE_ADDR='192.168.1.55'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SoilMoisture.objects.count(), 1)
        
        record = SoilMoisture.objects.first()
        self.assertEqual(record.ip_address, '192.168.1.55')
        # Check that floating point data is accurately retained by JSONField
        self.assertEqual(record.data['moisture_level'], 43.3)

    def test_list_iot(self):
        SoilMoisture.objects.create(
            data={"moisture_level": 30.5},
            ip_address="127.0.0.1"
        )
        
        response = self.client.get('/api/soil-moisture/')
        self.assertEqual(response.status_code, 200)
        
        json_data = response.json()
        self.assertTrue(json_data['success'])
        self.assertEqual(json_data['data']['pagination']['total_count'], 1)

    def test_latest_iot_motor_logic(self):
        SoilMoisture.objects.create(
            data={"moisture_level": 25.0},
            ip_address="127.0.0.1"
        )
        
        response = self.client.get('/api/soil-moisture/latest/?threshold=35.0')
        self.assertEqual(response.status_code, 200)
        
        json_data = response.json()
        self.assertEqual(json_data['motor_state'], 'on')
        self.assertEqual(json_data['reading_value'], 25.0)
