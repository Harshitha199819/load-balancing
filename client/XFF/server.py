import socket
import time

# Set a fixed port for listening to server responses
fixed_response_port = 12345

def send_request():
    lb_host = '172.31.8.174'  # Replace with the Load Balancer IP
    lb_port = 8080

    for i in range(5):  # Send multiple requests for testing
        try:
            # Connect to the load balancer
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.bind(('', 0))  # Bind to any available port
            client_socket.connect((lb_host, lb_port))
            
            # Create the request
            request = f"GET / Request {i+1} HTTP/1.1\r\nHost: {lb_host}\r\nX-Forwarded-For: {client_socket.getsockname()[0]}:{fixed_response_port}\r\n\r\n"
            client_socket.send(request.encode('utf-8'))
            print(f"Client sent request: {request.strip()}")

            # Close the connection to the load balancer
            client_socket.close()

            # Open a socket to listen on the fixed port
            response_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            response_socket.bind(('', fixed_response_port))  # Bind to the fixed port
            response_socket.listen(1)
            print(f"Listening for response on fixed port {fixed_response_port}")

            # Accept the incoming connection from the server
            conn, addr = response_socket.accept()
            response = conn.recv(1024).decode('utf-8')
            print(f"Client received response from server: {response.strip()}")
            conn.close()

            # Close the response listening socket
            response_socket.close()

        except Exception as e:
            print(f"Error during request {i+1}: {e}")
        
        finally:
            time.sleep(1)  # Wait 1 second before sending the next request

if __name__ == "__main__":
    send_request()
