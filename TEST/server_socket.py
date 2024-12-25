import socket
import select

def connect_to_server():
    host = 'easysploit.rocknroll17.com'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print("Connected to the server.")
        
        message = "Hello, server!"
        client_socket.sendall(message.encode())
        print(f"Client: {message}")
        
        while True:
            ready_to_read, _, _ = select.select([client_socket], [], [], 1.0)
            if ready_to_read:
                data = client_socket.recv(1024)
                if not data:
                    break
                command = data.decode()
                print(f"Server: {command}")
                if command == "exit":
                    print("Exit command received from the server.")
                    client_socket.close()
                    break
    except KeyboardInterrupt:
        print("Program terminated by the user.")
        client_socket.close()
    except Exception as e:
        print(f"Error occurred while connecting to the server: {e}")
    finally:
        client_socket.close()
        print("Connection to the server closed.")

if __name__ == '__main__':
    connect_to_server()
