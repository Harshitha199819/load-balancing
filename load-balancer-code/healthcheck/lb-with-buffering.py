import socket
import threading
import queue
import time

# Use the private IP addresses of your backend servers
backend_servers = [("172.31.7.238", 9008), ("172.31.8.222", 9009)]  # Replace with your private IPs
current_server = 0
health_status = {9008: False, 9009: False}  # Tracks the health of each server
request_queue = queue.Queue()  # Buffer for holding requests

def round_robin():
    global current_server
    available_servers = [server for server in backend_servers if health_status[server[1]]]
    if not available_servers:
        return None  # No healthy servers available
    server = available_servers[current_server % len(available_servers)]
    current_server = (current_server + 1) % len(available_servers)
    return server

def listen_for_health_updates(lb_port):
    health_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    health_socket.bind(('0.0.0.0', lb_port))
    health_socket.listen(5)
    print(f"Load Balancer health listener running on port {lb_port}...")

    while True:
        conn, addr = health_socket.accept()
        health_message = conn.recv(1024).decode('utf-8')
        print(f"Received health update: {health_message}")

        # Parse the health message and update the status map
        if "healthy" in health_message:
            server_id = int(health_message.split('-')[1].split(':')[0])
            port = 9007 + server_id  # Adjusting the port based on server_id
            health_status[port] = True
        elif "kill" in health_message:
            server_id = int(health_message.split('-')[1].split(':')[0])
            port = 9007 + server_id
            health_status[port] = False
        conn.close()

def process_buffered_requests():
    while True:
        if not request_queue.empty():
            client_socket, request, request_number = request_queue.get()
            backend_server = round_robin()
            if backend_server:
                try:
                    # Forward the buffered request to the selected backend server
                    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    server_socket.connect(backend_server)
                    server_socket.send(request.encode('utf-8'))

                    # Receive the response from the backend server
                    response = server_socket.recv(1024).decode('utf-8')
                    server_socket.close()

                    # Notify the client with the final response
                    client_socket.send(f"Final response for buffered Request {request_number}: {response}".encode('utf-8'))
                except Exception as e:
                    print(f"Error processing buffered request: {e}")
                finally:
                    client_socket.close()
            else:
                # Re-add the request to the buffer if no server is available
                request_queue.put((client_socket, request, request_number))
        time.sleep(1)  # Small delay to prevent busy waiting

def start_load_balancer():
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind(('0.0.0.0', 8080))
    lb_socket.listen(5)
    print("Load Balancer listening on port 8080...")

    # Start threads to handle health checks and process buffered requests
    health_thread = threading.Thread(target=listen_for_health_updates, args=(9090,))
    health_thread.daemon = True
    health_thread.start()

    buffer_thread = threading.Thread(target=process_buffered_requests)
    buffer_thread.daemon = True
    buffer_thread.start()

    while True:
        client_socket, addr = lb_socket.accept()
        print(f"Load Balancer received connection from {addr}")

        request = client_socket.recv(1024).decode('utf-8')
        request_number = int(request.split()[1])  # Extracting request number for identification
        print(f"Load Balancer received request {request_number}: {request}")

        # Determine which backend server to forward the request to
        backend_server = round_robin()

        if backend_server is None:
            # No available servers, buffer the request
            print(f"No servers available. Buffering Request {request_number}.")
            client_socket.send(f"Request {request_number} received. Waiting for server to be available.".encode('utf-8'))
            request_queue.put((client_socket, request, request_number))
        else:
            try:
                # Forward the request to the selected backend server
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.connect(backend_server)
                server_socket.send(request.encode('utf-8'))

                # Receive the response from the backend server
                response = server_socket.recv(1024).decode('utf-8')
                server_socket.close()

                # Send the final response to the client
                client_socket.send(f"Final response from server for Request {request_number}: {response}".encode('utf-8'))
            except Exception as e:
                print(f"Error forwarding request: {e}")
                client_socket.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            finally:
                client_socket.close()

if __name__ == "__main__":
    start_load_balancer()
