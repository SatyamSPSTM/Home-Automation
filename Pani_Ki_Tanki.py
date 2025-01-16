from machine import Pin,PWM,time_pulse_us
import time

# Define pins for ultrasonic sensor
trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(12, Pin.IN)

# Define pin for buzzer
buzzer_pin = PWM(Pin(26, Pin.OUT), freq=1000, duty=0)  # Change the pin number as per your ESP32 board

def measure_distance():
    # Send a 10us pulse to trigger the ultrasonic sensor
    CM_TO_INCH = 0.393701
    
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)
    
    # Measure the duration of the echo pulse
    pulse_time = time_pulse_us(echo_pin, 1, 30000)  # Timeout set to 30ms (30,000us)
    
    # Calculate distance in centimeters
    distance_cm = (pulse_time * 0.0343) / 2  # Speed of sound is approximately 343 m/s
    
    distanceInch = distance_cm * CM_TO_INCH;
    
    return distanceInch



def sound_buzzer():
    # Sound the buzzer by setting duty cycle to non-zero
    buzzer_pin.duty(500)  # Adjust duty cycle as needed for desired buzzer sound level
    time.sleep(2)  # Sound the buzzer for 2 seconds
    buzzer_pin.duty(0)  # Turn off the buzzer

while True:
    distance = measure_distance()
    print(distance)
    # Check if cistern is full (distance less than or equal to 10 cm) or empty (distance greater than 50 cm)
    if distance <= 10:
        print("Cistern is full !")
        sound_buzzer()
    elif distance > 50:
        print("Cistern is empty!")
        sound_buzzer()
    time.sleep(1)  # Wait for 1 second before taking the next measurement
 