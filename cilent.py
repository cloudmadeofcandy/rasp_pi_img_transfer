import base64
import cv2
import zmq
import numpy as np

port = "5555"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port) # binds to anything that wants to connect

camera = cv2.VideoCapture(0)  # init the camera

while True:
    try:

        """The first block of code uses the np.frombuffer to handle raw bytes.
           The second block of code uses the base64 encoding to transfer the bytes
        """
        grabbed, frame = camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = np.array(buffer).tobytes()
        socket.send(jpg_as_text)

#         grabbed, frame = camera.read()  # grab the current frame
#         frame = cv2.resize(frame, (640, 480))  # resize the frame
#         encoded, buffer = cv2.imencode('.jpg', frame)
#         jpg_as_text = base64.encode(buffer)
#         socket.send(jpg_as_text)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break
    