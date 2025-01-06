import board
import analogio
import time


TMP36_PIN = board.A0



def temperature(analogin):
    millivolts = analogin.value * (analogin.reference_voltage * 1000 / 65535)
    return (millivolts - 500) / 10



tmp36 = analogio.AnalogIn(TMP36_PIN)


while True:
   
    temp_C = temperature(tmp36)
 
    temp_F = (temp_C * 9/5) + 32

    print("Temperature: {}C {}F".format(temp_C, temp_F))
    time.sleep(1.0)
