import socket

# Define message format constants
MESSAGE_START = b"CMD:"  # Message start identifier
MESSAGE_END = b"\n"  # Message end identifier
COMMAND_DELIMITER = b" "  # Delimiter between command and parameters

def receive_and_forward():
  # Create a socket (replace with appropriate socket type based on network needs)
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind(('localhost', 12345))  # Replace with desired port
  server_socket.listen(1)  # Listen for connections

  # Accept connection from controller
  connection, address = server_socket.accept()
  print(f"Connection established from {address}")

  while True:
    # Receive data from controller
    data = connection.recv(1024)  # Adjust buffer size as needed

    if not data:
      break

    # Process received data
    message = data.decode()
    if not message.startswith(MESSAGE_START.decode()) or not message.endswith(MESSAGE_END.decode()):
      print("Invalid message format")
      continue

    # Extract command and parameters
    parts = message.strip(MESSAGE_START + MESSAGE_END).split(COMMAND_DELIMITER.decode())
    command = parts[0]
    params = parts[1:] if len(parts) > 1 else []

    # Translate command and parameters to ROS message (example for Twist message)
    twist_msg = Twist()
    if command == "forward":
      twist_msg.linear.x = float(params[0])  # Assuming speed as parameter
    elif command == "backward":
      twist_msg.linear.x = -float(params[0])  # Assuming speed as parameter
    elif command == "turn":
      twist_msg.angular.z = float(params[0])  # Assuming angle as parameter
    else:
      print(f"Unknown command: {command}")
      continue

    # (Optional) Implement logic to send the Twist message to turtlesim node using ROS 2 client libraries

    # Send response message to controller (optional)
    response = "Command received"
    connection.sendall(response.encode())

  connection.close()
  server_socket.close()

if __name__ == '__main__':
  receive_and_forward()