from machine import Pin,ADC,PWM
import time
import urequests
import network

Kfan1=Pin(12,Pin.OUT)
Kled1=Pin(13,Pin.OUT)
Led1=Pin(14,Pin.OUT)
R1L1=Pin(15,Pin.OUT)
R1fan1=Pin(16,Pin.OUT)
gas =ADC(Pin(34))
regulator_status=PWM(Pin(19))
regulator_status.freq(50)

ssid = "Ankit"
password = "88888861"

firebase_url = "https://dht11-training-default-rtdb.asia-southeast1.firebasedatabase.app/Home_Appliances.json"
conversion_factor=100/1023

def connect_to_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Connecting to Wi-Fi...")
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print("Connected to Wi-Fi")

def Home_Data():
    try:
        response = urequests.get(firebase_url)
        data = response.json()
        response.close()  
        return data
    except Exception as e:
        print("Error retrieving Gardening Data:", e)
        return None

def update_gas_level(degree):
    try:
        data = {"gas": degree}
        json_data = urequests.json.dumps(data)
        response = urequests.put(url, data=json_data)
        if response.status_code == 200:
          print("gas level updated successfully!")
        else:
            print(f"Error updating status: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def read_gas_sensor():
  sensor_value = gas.read() 
  gas_concentration = sensor_value * conversion_factor  
  return gas_concentration

def update_servo_angle(angle):
    duty = int(angle * 1023 / 180)  
    regulator_status.duty(duty)

    print("Servo angle updated to:", angle)
    
# Main loop
def main():
    connect_to_wifi()
    while True:
        data=Home_Data()
        for i in data:
            if i=='Kfan1':
                Kfan1=data[i]
            elif i=='Kled1':
                Kled1=data[i]
            elif i=='Led1':
                Led1=data[i]
            elif i=='R1L1':
                R1L1=data[i]
            elif i=='R1fan1':
                R1fan1=data[i]
            elif i=='regulator_status':
                regulator=data[i]
                if regulator:
                    servo_angle=90
                    regulator_status_upadate(servo_angle)
                else:
                    servo_angle=0
                    regulator_status_upadate(servo_angle)
        else:
            print("Data retrieval from Firebase failed.")
        update_gas_level(gas_level())
        
        
        

if __name__ == "__main__":
    main()


