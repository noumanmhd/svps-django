from ultrasonic import Ultrasonic
import time
import requests

URL = "http://127.0.0.1:8000/update-state/"

slot1 = Ultrasonic(echo=23, trigger=24, limit=4)
slot2 = Ultrasonic(echo=5, trigger=6, limit=6)
slot3 = Ultrasonic(echo=17, trigger=27, limit=2)

while True:
    s1 = slot1.detected()
    time.sleep(1)
    s2 = slot2.detected()
    time.sleep(1)
    s3 = slot3.detected()
    time.sleep(1)

    res = requests.get(URL, json={
        'A1': s1,
        'A2': s2,
        'A3': s3
        })

    print(f"Detected Solt1: {s1}")
    print(f"Detected Slot2: {s2}")
    print(f"Detected Slot3: {s3}")

