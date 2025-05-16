import os
import RPi.GPIO as GPIO
import time

def bicara(text):
    bahasa = "id+m1"
    speed = 130
    pitch = 55
    volume = 200

    command = f'espeak-ng -v {bahasa} -s {speed} -p {pitch} -a {volume} "{text}"'
    os.system(command)

GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

print("Mengukur jarak")
bicara("Mengukur jarak")


try:
    while True:
        # Kirim pulsa trigger selama 10 mikrodetik
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        # Tunggu echo mulai
        pulse_start = time.time()
        timeout = pulse_start + 0.04  # timeout 40 ms
        while GPIO.input(ECHO) == 0 and pulse_start < timeout:
            pulse_start = time.time()
        if pulse_start >= timeout:
            continue  # ulangi loop jika timeout

        # Tunggu echo selesai
        pulse_end = time.time()
        timeout = pulse_end + 0.04
        while GPIO.input(ECHO) == 1 and pulse_end < timeout:
            pulse_end = time.time()
        if pulse_end >= timeout:
            continue  # ulangi loop jika timeout

        pulse_duration = pulse_end - pulse_start
        jarak = pulse_duration * 17150
        jarak = round(jarak, 2)

        print("Jarak", jarak, "cm")
        bicara(f"Jarak {jarak} sentimeter")
        time.sleep(2)

except KeyboardInterrupt:
    print("Pengukuran dihentikan")
    bicara("Pengukuran dihentikan")
finally:
    GPIO.cleanup()

