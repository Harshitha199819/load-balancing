import socket
import threading

# Define backend server addresses
backend_servers = [("172.31.7.238", 9008), ("172.31.8.222", 9009)]
current_server = 0

# Select server in a round-robin manner for simplicity
def round_robin():
    global current_server
    server = backend_servers[current_server % len(backend_servers)]
    current_server += 1
    return server

# Handle client connections
def handle_client(client_socket, client_address):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request from {client_address}: {request}")

    # Select the best server to handle the request
    server_ip, server_port = round_robin()
    print(f"Forwarding request to {server_ip}:{server_port} for client {client_address}")

    try:
        # Connect to the chosen server
        with socket.create_connection((server_ip, server_port)) as server_socket:
            # Add X-Forwarded-For header to encapsulate client IP information
            modified_request = f"{request}\r\nX-Forwarded-For: {client_address[0]}:{client_address[1]}\r\n"
            server_socket.send(modified_request.encode('utf-8'))
    except Exception as e:
        print(f"Error connecting to server {server_ip}:{server_port} - {e}")
        client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
    finally:
        client_socket.close()

# Start the load balancer to listen for client connections
def start_load_balancer():
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind(('0.0.0.0', 8080))
    lb_socket.listen(5)
    print("Load Balancer running on port 8080...")

    while True:
        client_socket, client_address = lb_socket.accept()
        print(f"Accepted connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_load_balancer()
