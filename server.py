import cv2
import zmq
import base64
import numpy as np

port = "5555"

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.connect ("tcp://<your Raspberry Pi IP Address in your network>:%s" % port)

footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    try:
        """The first block of code uses the np.frombuffer to handle raw bytes.
           The second block of code uses the base64 encoding to transfer the bytes
        """

        frame = footage_socket.recv()
        npimg = np.frombuffer(frame, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        imageRGB = cv2.cvtColor(source , cv2.COLOR_BGR2RGB)
        cv2.imshow("Stream", imageRGB)
        cv2.waitKey(1)
        
        # frame = footage_socket.recv_string()
        # img = base64.b64decode(frame)
        # npimg = np.fromstring(img, dtype=np.uint8)
        # source = cv2.imdecode(npimg, 1)
        # imageRGB = cv2.cvtColor(source , cv2.COLOR_BGR2RGB)
        # cv2.imshow("Stream", imageRGB)
        # cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break
    