import socket
import threading
import time

def send_health_status(server_id, lb_host, lb_port):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as health_socket:
                health_socket.connect((lb_host, lb_port))
                health_status = f"Server {server_id} is healthy"
                health_socket.send(health_status.encode('utf-8'))
                print(f"Server {server_id} sent health status to LB")
        except Exception as e:
            print(f"Error sending health status from Server {server_id}: {e}")
        time.sleep(10)  # Health check interval

def send_kill_signal(server_id, lb_host, lb_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as kill_socket:
            kill_socket.connect((lb_host, lb_port))
            kill_signal = f"Server {server_id} shutting down"
            kill_socket.send(kill_signal.encode('utf-8'))
            print(f"Server {server_id} sent shutdown signal to LB")
    except Exception as e:
        print(f"Error sending kill signal from Server {server_id}: {e}")

def start_server(server_id, port, lb_host, lb_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))  # Bind to all network interfaces
    server_socket.listen(5)
    print(f"Backend Server {server_id} listening on port {port}...")

    health_thread = threading.Thread(target=send_health_status, args=(server_id, lb_host, lb_port))
    health_thread.daemon = True
    health_thread.start()

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Server {server_id} received connection from IP: {addr[0]}, Port: {addr[1]}")
            request = client_socket.recv(1024).decode('utf-8')
            print(f"Server {server_id} received request: {request} from IP: {addr[0]}")

            response = f"Response from Server {server_id}"
            client_socket.send(response.encode('utf-8'))
            client_socket.close()
    except KeyboardInterrupt:
        print(f"Server {server_id} shutting down...")
        send_kill_signal(server_id, lb_host, lb_port)
    finally:
        server_socket.close()

if __name__ == "__main__":
    SERVER_ID = 1
    SERVER_PORT = 8001
    LB_HOST = '172.31.8.174'
    LB_PORT = 9090

    start_server(SERVER_ID, SERVER_PORT, LB_HOST, LB_PORT)

ubuntu@ip-172-31-7-238:
