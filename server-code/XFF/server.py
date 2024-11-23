import socket

def handle_request(connection):
    request = connection.recv(1024).decode('utf-8')
    print(f"Server received request: {request}")

    # Parse the first occurrence of X-Forwarded-For header to get client IP and port
    headers = request.split("\r\n")
    client_ip, client_port = None, None

    for header in headers:
        if header.startswith("X-Forwarded-For:") and client_ip is None:
            client_info = header.split("X-Forwarded-For:")[-1].strip()  # Take only the first entry
            client_ip, client_port = client_info.split(":")
            client_port = int(client_port)
            print(f"Parsed client IP: {client_ip}, client port: {client_port}")
            break  # Exit after the first valid header is found

    # Process the request and prepare a response
    response = "200 OK - Response from server"

    # Send the response directly to the client
    try:
        if client_ip and client_port:
            with socket.create_connection((client_ip, client_port)) as client_socket:
                client_socket.send(response.encode('utf-8'))
                print(f"Server responded directly to client at {client_ip}:{client_port}")
        else:
            print("Error: Client IP and port not found in headers.")
    except Exception as e:
        print(f"Error responding to client at {client_ip}:{client_port} - {e}")

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
    start_server(9008)  # Or start_server(9009) for another server instance; 9008 for server1, 9009 for server2
