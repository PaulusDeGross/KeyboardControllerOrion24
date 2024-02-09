import time

import keyboard
import serial

KEY_CODES = {
    "q": [16, 45], "w": [17, 0], "e": [18, 45],
    "a": [30, 2*45], "d": [32, 2*45],
    "y": [21, 3*45], "x": [45, 4*45], "c": [46, 3*45],
}

time.sleep(3)
teensy = serial.Serial("/dev/serial0", 9600, serial.EIGHTBITS)
mutable_bytes = bytearray(3)

while True:
    try:
        event = keyboard.read_event()
        if event.event_type == "down":
            if event.name in KEY_CODES:
                angle = KEY_CODES[event.name][1]
                mutable_bytes[0] = int(0)
                mutable_bytes[2] = angle

                if angle < 0:
                    mutable_bytes[1] = 1
                    angle = -angle
                else:
                    mutable_bytes[1] = 0

                ret_msg = teensy.readline()
                if ret_msg == b"a\r\n":
                    print("Sending data: ", mutable_bytes)
                    teensy.write(mutable_bytes)
                    time.sleep(0.1)

    except KeyboardInterrupt:
        break