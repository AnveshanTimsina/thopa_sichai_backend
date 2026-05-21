import network
import urequests
import json
import time
import gc
from machine import ADC, Pin

# --- Network Configuration ---
SSID = "<YOUR_WIFI_SSID>"
PASSWORD = "<YOUR_WIFI_PASSWORD>"
BASE_URL = "http://192.168.1.X:8000/api/soil-moisture"
IOT_API_TOKEN = "<YOUR_GENERATED_API_TOKEN_HERE>"  # Replace with the actual token generated from Django admin for authentication

# --- Hardware & Sensor Configuration ---
SOIL_SENSOR_PIN = 32
RELAY_PIN = 5  # GPIO pin connected to 5V Relay Module

CALIBRATION_DRY = 3200 
CALIBRATION_WET = 1200 

def setup_sensor(pin_num):
    """Initializes the ADC (Analog-to-Digital Converter) pin."""
    adc = ADC(Pin(pin_num))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)
    return adc

def setup_relay(pin_num):
    """Initializes the GPIO pin for the water pump relay."""
    relay = Pin(pin_num, Pin.OUT)
    relay.value(0)  # Default pump to OFF (depends on relay type: Active High/Low)
    return relay

def get_moisture_percentage(adc, num_samples=10):
    total = 0
    for _ in range(num_samples):
        total += adc.read()
        time.sleep(0.05)
        
    avg_raw = total / num_samples
    print(f"Raw ADC Hardware Reading: {avg_raw}")
    
    if CALIBRATION_DRY == CALIBRATION_WET:
        return 0.0
        
    moisture_pct = ((CALIBRATION_DRY - avg_raw) / (CALIBRATION_DRY - CALIBRATION_WET)) * 100
    moisture_pct = max(0.0, min(100.0, moisture_pct))
    
    return round(moisture_pct, 2)

def connect_wifi(timeout_sec=30):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.connect(SSID, PASSWORD)
        
        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > timeout_sec:
                print("Failed to connect to WiFi within timeout.")
                return None
            time.sleep(1)

    ip = wlan.ifconfig()[0]
    print(f"Connected successfully with IP: {ip}")
    return ip

def send_telemetry_data(ip_address, moisture_level, location="ku"):
    """
    Constructs and sends telemetry payload to the Django backend.
    """
    payload = {
        "data": {
            "moisture_level": moisture_level,
        },
        "metadata": {
            "location": location,
        },
        "ip_address": ip_address
    }
    
    headers = {
        "Content-Type": "application/json",
        "Connection": "close",
        "Authorization": f"Token {IOT_API_TOKEN}"
    }

    try:
        gc.collect()
        url = f"{BASE_URL}/receive/"
        print(f"Sending Payload: {json.dumps(payload)}")
        response = urequests.post(
            url,
            data=json.dumps(payload),
            headers=headers
        )

        print(f"POST Status: {response.status_code}")
        
    except Exception as e:
        print(f"POST Request failed: {e}")
    finally:
        if 'response' in locals():
            response.close()
            del response
        gc.collect()

def fetch_and_actuate_motor(relay):
    """
    Fetches the analytics command from Django server and controls the physical water pump via Relay.
    """
    try:
        gc.collect()
        url = f"{BASE_URL}/latest/"
        headers = {
            "Authorization": f"Token {IOT_API_TOKEN}",
            "Connection": "close"
        }
        print("Fetching motor instructions from server...")
        response = urequests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            motor_state = data.get('motor_state')
            print(f"Server Motor Instruction: {motor_state}")
            
            # Actuate Relay hardware based on server analytics 
            if motor_state == 'on':
                relay.value(1)  # Turn PUMP ON
                print(">>> PUMP IS NOW RUNNING <<<")
            else:
                relay.value(0)  # Turn PUMP OFF
                print(">>> PUMP IS OFF <<<")
        else:
            print(f"GET Status error: {response.status_code}")
            
    except Exception as e:
        print(f"GET Request failed: {e}")
        # Failsafe: Turn OFF pump if internet request crashes to prevent flooding!
        relay.value(0)
    finally:
        if 'response' in locals():
            response.close()
            del response
        gc.collect()

def main():
    gc.collect()
    
    # Initialize the physical hardware 
    moisture_sensor = setup_sensor(SOIL_SENSOR_PIN)
    relay = setup_relay(RELAY_PIN)
    
    # Read the data dynamically calculated from ADC pin
    moisture_pct = get_moisture_percentage(moisture_sensor)
    print(f"Calculated Moisture: {moisture_pct}%")
    
    # Connect to internet and dispatch
    ip = connect_wifi()
    if ip:
        send_telemetry_data(ip, moisture_level=moisture_pct)
        
        # Pause slightly to ensure backend handles insertion before querying
        time.sleep(1)
        
        # Download decision tree rule from server and actuate physical pump!
        fetch_and_actuate_motor(relay)

if __name__ == "__main__":
    main()
