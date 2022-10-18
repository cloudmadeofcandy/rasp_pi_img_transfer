import base64
import cv2
import zmq
import numpy as np
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
BLOCK_SIZE = 32
port = "5555"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port) # binds to anything that wants to connect
key = b'0123456789abcdef'
cipher = AES.new(key, AES.MODE_ECB)
camera = cv2.VideoCapture(0)  # init the camera

while True:
    try:
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
    
