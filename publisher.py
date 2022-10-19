import base64
import threading
import cv2
from sklearn.neighbors import KernelDensity
import zmq
import time
import numpy as np
from datetime import datetime
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
BLOCK_SIZE = 32
port = "5555"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port) # binds to anything that wants to connect

now = datetime.now()
current_time = now.strftime("%H")
key = bytes('0123456789abcd' + current_time, 'utf-8')

cipher = AES.new(key, AES.MODE_ECB)
camera = cv2.VideoCapture(0)  # init the camera
obj = threading.Semaphore()

def video_streaming():
    global socket
    global cipher
    global obj
    while True:
        try:
            obj.acquire()
            grabbed, frame = camera.read()  # grab the current frame
            frame = cv2.resize(frame, (640, 480))  # resize the frame
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = np.array(buffer).tobytes()
            ciphertext = cipher.encrypt(pad(jpg_as_text, BLOCK_SIZE))
            socket.send(ciphertext)

        except KeyboardInterrupt:
            camera.release()
            cv2.destroyAllWindows()
            break

        finally:
            obj.release()

def key_change():
    global cipher
    global obj
    obj.acquire()
    now = datetime.now()
    current_time = now.strftime("%H")
    key = bytes('0123456789abcd' + current_time, 'utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    obj.release()
    time.sleep(3600)

t1 = threading.Thread(target = video_streaming)
t1.daemon = True # Kill thread when main program ends
t2 = threading.Thread(target = key_change)
t2.daemon = True

try:
    t2.start()
    t1.start()
finally:
    t2.join()
    t1.join()
