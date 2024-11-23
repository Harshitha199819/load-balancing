import socket
import threading
import time

# List of backend servers (IP, Port)
backend_servers = [("172.31.7.238", 9008), ("172.31.8.222", 9009)]

# Store combined RTT and processing delay metrics
server_metrics = {}

# Measure RTT by TCP handshake
def measure_rtt_tcp(server_ip, port):
    try:
        start_time = time.time()
        with socket.create_connection((server_ip, port), timeout=2):
            rtt = (time.time() - start_time) * 1000  # RTT in ms
        return rtt
    except Exception as e:
        print(f"Error measuring RTT for {server_ip}:{port} - {e}")
        return float('inf')  # Return infinity if connection fails

# Measure processing delay by sending a lightweight probe request
def measure_processing_delay(server_ip, port):
    try:
        start_time = time.time()
        with socket.create_connection((server_ip, port), timeout=2) as s:
            s.sendall(b"GET /status")
            response = s.recv(1024)
            delay = (time.time() - start_time) * 1000  # Delay in ms
        return delay
    except Exception as e:
        print(f"Error measuring processing delay for {server_ip}:{port} - {e}")
        return float('inf')  # Return infinity if connection fails

# Continuously update RTT + processing delay for each server every 5 seconds
def update_server_metrics():
    while True:
        for server_ip, port in backend_servers:
            rtt = measure_rtt_tcp(server_ip, port)
            processing_delay = measure_processing_delay(server_ip, port)
            total_delay = rtt + processing_delay
            server_metrics[(server_ip, port)] = total_delay
            print(f"Server {server_ip}:{port} - RTT: {rtt:.2f} ms, Processing Delay: {processing_delay:.2f} ms, Total: {total_delay:.2f} ms")
        time.sleep(5)  # Update every 5 seconds

# Select the server with the lowest combined RTT and processing delay
def select_best_server():
    active_servers = {server: delay for server, delay in server_metrics.items() if delay != float('inf')}
    if active_servers:
        return min(active_servers, key=active_servers.get)
    return None

# Handle client requests by forwarding to the best server
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request: {request}")

    best_server = select_best_server()
    if not best_server:
        client_socket.send(b"HTTP/1.1 503 Service Unavailable\r\n\r\n")
        client_socket.close()
        print("No available servers. Returned 503 to client.")
        return

    server_ip, server_port = best_server
    try:
        with socket.create_connection((server_ip, server_port)) as server_socket:
            server_socket.send(request.encode('utf-8'))
            response = server_socket.recv(1024)
            client_socket.send(response)
            print(f"Forwarded request to server {server_ip}:{server_port} with response to client.")
    except Exception as e:
        print(f"Error forwarding request to server {server_ip}:{server_port} - {e}")
        client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
    finally:
        client_socket.close()

# Start the load balancer to listen for client connections
def start_load_balancer():
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind(('0.0.0.0', 8080))
    lb_socket.listen(5)
    print("Load Balancer running on port 8080...")

    # Start background thread to update server metrics every 5 seconds
    threading.Thread(target=update_server_metrics, daemon=True).start()

    while True:
        client_socket, addr = lb_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_load_balancer()
