import socket
import threading
import time
import os
import psutil
import subprocess

# Define backend server addresses
backend_servers = [("172.31.7.238", 9008), ("172.31.8.222", 9009)]

# Dictionary to store bandwidth usage for each server
bandwidth_usage = {server: 0 for server in backend_servers}

def get_network_bandwidth():
    """Measure network bandwidth using psutil and speedtest-cli."""
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv
    time.sleep(1)
    net_io = psutil.net_io_counters()
    new_bytes_sent = net_io.bytes_sent
    new_bytes_recv = net_io.bytes_recv
    bandwidth = (new_bytes_sent + new_bytes_recv - bytes_sent - bytes_recv) / 1024  # KB/s
    return bandwidth

def monitor_bandwidth():
    """Continuously monitor each backend server's network bandwidth."""
    while True:
        for server in backend_servers:
            bandwidth_usage[server] = get_network_bandwidth()
            print(f"Bandwidth for {server}: {bandwidth_usage[server]} KB/s")
        time.sleep(5)  # Check every 5 seconds

def get_best_bandwidth_server():
    """Get the server with the highest available bandwidth."""
    return max(bandwidth_usage, key=bandwidth_usage.get)

def start_load_balancer():
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind(('0.0.0.0', 8080))
    lb_socket.listen(5)
    print("Load Balancer listening on port 8080...")

    # Start bandwidth monitoring in a background thread
    monitor_thread = threading.Thread(target=monitor_bandwidth)
    monitor_thread.daemon = True
    monitor_thread.start()

    while True:
        client_socket, client_addr = lb_socket.accept()
        print(f"Received connection from {client_addr}")
        request = client_socket.recv(1024).decode('utf-8')

        # Get the server with the highest available bandwidth
        best_server = get_best_bandwidth_server()

        # Forward request to the selected server
        server_host, server_port = best_server
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect((server_host, server_port))
                server_socket.send(request.encode('utf-8'))
                response = server_socket.recv(1024)
                client_socket.send(response)
                print(f"Forwarded request to {best_server} with bandwidth {bandwidth_usage[best_server]} KB/s")
        except Exception as e:
            print(f"Error forwarding to server: {e}")
            client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_load_balancer()
