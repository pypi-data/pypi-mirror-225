import cv2
import socket
import numpy as np
from pathlib import Path

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'  # Change this to the server's IP address
port = 12345
client_socket.connect((host, port))

frame_shape_bytes = client_socket.recv(4 * 3)  # Assuming 3D frame shape
frame_shape = np.frombuffer(frame_shape_bytes, dtype=np.int32)
frame_size = frame_shape.prod() * 3  # Assuming 3 channels

data = b""
while len(data) < frame_size:
    data += client_socket.recv(frame_size - len(data))

frame_bytes = np.frombuffer(data, dtype=np.uint8)
frame = frame_bytes.reshape(frame_shape)

while True:
    cv2.imshow("Received Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the socket and destroy OpenCV windows
client_socket.close()
cv2.destroyAllWindows()
