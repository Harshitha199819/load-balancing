import socket
import threading

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Server received request: {request}")
        
        # Simulate response
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from server!"
        client_socket.send(response.encode('utf-8'))
    finally:
        client_socket.close()

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}...")

    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server(9009)  # Run another instance on port 9009 for the second server
