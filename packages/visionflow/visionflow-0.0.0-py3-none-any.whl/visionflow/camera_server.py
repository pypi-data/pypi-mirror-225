
import cv2
import socket
import numpy as np
from pathlib import Path

# Create a capture object for the webcam
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# collect a test frame
success, frame = capture.read()

# Check if the capture object was successfully opened
if not capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'  # Change this to your server's IP address if needed
port = 12345
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

client_socket, client_address = server_socket.accept()
print(f"Connection from: {client_address}")

while True:
    ret, frame = capture.read()

    # Serialize the frame as bytes
    frame_bytes = frame.tobytes()

    # Get the frame shape for reconstruction
    frame_shape = frame.shape

    # Send the frame shape first
    frame_shape_bytes = np.array(frame_shape, dtype=np.int32).tobytes()
    client_socket.sendall(frame_shape_bytes)

    # Send the frame data
    client_socket.sendall(frame_bytes)

# Close the sockets and release the capture object
client_socket.close()
server_socket.close()
capture.release()
