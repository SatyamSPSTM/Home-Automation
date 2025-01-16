from machine import Pin
import time
import urequests
import network

motor_p=Pin(19,Pin.OUT)

ssid = "Ankit"
password = "88888861"

g_firebase_url = "https://dht11-training-default-rtdb.asia-southeast1.firebasedatabase.app/Gardening.json"

def connect_to_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    if not station.isconnected():
        print("Connecting to Wi-Fi...")
        station.connect(ssid, password)
        while not station.isconnected():
            pass
    print("Connected to Wi-Fi")

def Gardening_Data():
    try:
        response = urequests.get(firebase_url)
        data = response.json()
        response.close()  
        return data
    except Exception as e:
        print("Error retrieving Gardening Data:", e)
        return None

def update_motor_status(s):
    try:
        data = {"status": s}
        json_data = urequests.json.dumps(data)
        response = urequests.put(url, data=json_data)
        if response.status_code == 200:
          print("Motor status updated successfully!")
        else:
            print(f"Error updating status: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
def current_time():
    current_time = time.localtime()  
    hour = current_time.tm_hour
    minute = current_time.tm_min
    return hour,minute

def ftime(data):
    try:
        hours, minutes = map(int, time_string.split(":"))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return time.time(hours, minutes, 0)  
        else:
            return False
    except ValueError:
        return False


# Main loop
def main():
    connect_to_wifi()
    while True:
        data=Gardening_Data()
        run_time,duration,Motor_status=data['run_time'],int(data['Duration']),data['Motor_status']
        hour,minute=current_time()
        fhour,fminute=ftime(run_time)
        if fhour==hour and fminute==minute:
            motor_p.on()
            update_motor_status(True)
            sleep(duration*60)
            update_motor_status(False)
        else:
            print("Data retrieval from Firebase failed.")
        
        
        

if __name__ == "__main__":
    main()

