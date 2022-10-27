import cv2
from datetime import datetime
import zmq
import base64
import numpy as np
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
BLOCK_SIZE = 32
port = "5555"

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.connect ("tcp://localhost:%s" % port)
# footage_socket.connect ("tcp://raspberrypi.local:%s" % port)
now = datetime.now()
current_time = now.strftime("%H")
key = bytes('0123456789abcd' + current_time, 'utf-8')
cipher = AES.new(key, AES.MODE_ECB)
footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    try:
        frame = footage_socket.recv()
        frame = cipher.decrypt(frame)
        frame = (unpad(frame, BLOCK_SIZE))
        npimg = np.frombuffer(frame, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        # imageRGB = source
        imageRGB = cv2.cvtColor(source , cv2.COLOR_BGR2RGB)
        cv2.imshow("Stream", imageRGB)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break

    except ValueError:
        now = datetime.now()
        current_time = now.strftime("%H")
        key = bytes('0123456789abcd' + current_time, 'utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
    