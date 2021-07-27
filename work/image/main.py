import cv2
import requests 
from detect import detect_image
from servo import Barrier
from gpiozero import LED, Button
from signal import pause
from time import sleep

IN_IR_PIN = 0
OUT_IR_PIN = 1

bar = Barrier(0)
bar.bclose()

in_state = False
out_state = False

URL = "http://127.0.0.1:8000/check-plate/"

def on_car_in_start():
    global in_state
    global out_state
    if not out_state:
        camera = cv2.VideoCapture(0)
        _, frame = camera.read()
        result = detect_image(frame)
        res = requests.get(URL, json={
            'plate': result
        })
        if res.status_code == 200:
            bar.bopen()
            in_state = True
    

def on_car_in_stop():
    global in_state
    global out_state
    if not in_state and out_state:
        sleep(2)
        bar.bclose()
        out_state = False

def on_car_out_start():
    global in_state
    global out_state
    if not in_state:
        bar.bopen()
        out_state = True

def on_car_out_stop():
    global in_state
    global out_state
    if not out_state and in_state:
        sleep(2)
        bar.bclose()
        in_state = False

def main():
   in_ir = Button(IN_IR_PIN)
   out_ir = Button(OUT_IR_PIN)

   in_ir.when_pressed = on_car_in_start
   in_ir.when_released = on_car_in_stop

   out_ir.when_pressed = on_car_out_start
   out_ir.when_released = on_car_out_stop

   pause()


if __name__ == "__main__":
    main()