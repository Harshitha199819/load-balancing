import socket
import random
import time

def handle_request(connection):
    request = connection.recv(1024).decode('utf-8')
    if "GET /status" in request:
        delay = random.uniform(0.5, 2.0)  # Delay between 0.5 to 2 seconds
        time.sleep(delay)
        connection.send(b"200 OK - Status")
    else:
        # Normal request handling
        connection.send(b"200 OK - Response from server")
    connection.close()

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}...")

    while True:
        connection, _ = server_socket.accept()
        handle_request(connection)

if __name__ == "__main__":
    start_server(9008)  # Or start_server(9009) for the second server
