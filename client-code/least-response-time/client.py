import socket
import time

def send_request():
    lb_host = '172.31.8.174'  # Load balancer IP
    lb_port = 8080

    for i in range(5):  # Send 5 requests
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((lb_host, lb_port))
            request = f"GET / Request {i+1}"
            client_socket.send(request.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Client received response: {response}")
        except Exception as e:
            print(f"Error during request {i+1}: {e}")
        finally:
            client_socket.close()
            time.sleep(1)

if __name__ == "__main__":
    send_request()
