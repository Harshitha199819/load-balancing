import socket
import time
import threading

def send_request(message, request_number):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('172.31.8.174', 8080))  # Replace with your Load Balancer's private IP
        client_socket.send(message.encode('utf-8'))

        # Receive the initial response from the load balancer (either temporary or final)
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Client received response for Request {request_number}: {response}")

        # Keep listening for additional final responses
        while True:
            final_response = client_socket.recv(1024).decode('utf-8')
            if final_response:
                print(f"Client received final response for Request {request_number}: {final_response}")
                break

    except Exception as e:
        print(f"Error sending request {request_number}: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    request_number = 1
    while True:  # Continuously send requests
        threading.Thread(target=send_request, args=(f"Request {request_number}", request_number)).start()
        request_number += 1
        time.sleep(1)  # Adjust the frequency of requests if needed
