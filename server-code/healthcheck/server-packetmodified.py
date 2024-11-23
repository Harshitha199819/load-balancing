import socket

def handle_client_request(connection):
    try:
        request = connection.recv(1024).decode('utf-8')
        print(f"Server received request: {request}")

        # Extract client IP and port from the forwarded request
        client_info = request.split("CLIENT_IP:")[1]
        client_ip = client_info.split("CLIENT_PORT:")[0].strip()
        client_port = int(client_info.split("CLIENT_PORT:")[1].strip())

        # Process the request (dummy processing here)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from Server!"

        # Send response directly to the client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client_ip, client_port))
        client_socket.send(response.encode('utf-8'))
        print(f"Server responded directly to client at {client_ip}:{client_port}")
        client_socket.close()
    except Exception as e:
        print(f"Error handling client request: {e}")
    finally:
        connection.close()

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}...")

    while True:
        connection, _ = server_socket.accept()
        handle_client_request(connection)

if __name__ == "__main__":
    start_server(9008)  # Run another instance on port 9009 for Server 2
