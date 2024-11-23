import socket
import time

def send_request(request_number):
    lb_host = '172.31.8.174'  # Replace with your Load Balancer IP
    lb_port = 8080

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((lb_host, lb_port))
        
        request = f"GET / Request {request_number}"
        client_socket.send(request.encode('utf-8'))
        print(f"Client sent request: {request}")

        # Receive the response from the server
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Client received response: {response}")
    except Exception as e:
        print(f"Error during request {request_number}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    for i in range(20):  # Send 20 requests
        send_request(i + 1)
        time.sleep(1)  # 1-second delay between requests
