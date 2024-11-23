import socket
import threading
import time

# Define backend server addresses
backend_servers = [("172.31.7.238", 9008), ("172.31.8.222", 9009)]
health_status = {server: False for server in backend_servers}  # Tracks health status of each server

def health_check(server):
    """Check if a backend server is healthy."""
    host, port = server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((host, port))
            s.sendall(b"GET /health HTTP/1.1\r\nHost: localhost\r\n\r\n")
            response = s.recv(1024).decode('utf-8')
            if "200 OK" in response:
                health_status[server] = True
            else:
                health_status[server] = False
    except:
        health_status[server] = False

def monitor_servers():
    """Continuously monitor each server's health."""
    while True:
        for server in backend_servers:
            health_check(server)
            print(f"Health status of {server}: {health_status[server]}")
        time.sleep(5)

def get_healthy_server():
    """Get a healthy server if available."""
    for server, healthy in health_status.items():
        if healthy:
            return server
    return None

def start_load_balancer():
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind(('0.0.0.0', 8080))
    lb_socket.listen(5)
    print("Load Balancer listening on port 8080...")

    # Start health monitoring thread
    monitor_thread = threading.Thread(target=monitor_servers)
    monitor_thread.daemon = True
    monitor_thread.start()

    while True:
        client_socket, client_addr = lb_socket.accept()
        print(f"Received connection from {client_addr}")
        request = client_socket.recv(1024).decode('utf-8')

        # Get a healthy server
        healthy_server = get_healthy_server()

        if healthy_server is None:
            client_socket.send(b"HTTP/1.1 503 Service Unavailable\r\n\r\n")
            client_socket.close()
            continue

        # Forward the request to the healthy server with client info
        server_host, server_port = healthy_server
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect((server_host, server_port))
                forward_request = f"{request}\nCLIENT_IP:{client_addr[0]}\nCLIENT_PORT:{client_addr[1]}"
                server_socket.send(forward_request.encode('utf-8'))
                print(f"Forwarded request to {healthy_server} with client info for direct response.")
        except Exception as e:
            print(f"Error forwarding to server: {e}")
            client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        
        client_socket.close()

if __name__ == "__main__":
    start_load_balancer()
