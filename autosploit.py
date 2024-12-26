import socket
import subprocess

def connect_to_server():
    host = 'easysploit.rocknroll17.com'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print("Connected to the server.")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            command = data.decode().strip()
            print(f"Server: {command}")
            if "Screen:" in command:
                screen_name = command.split("Screen:")[1].strip()
                subprocess.run(["screen", "-dmS", screen_name], check=True)
                client_socket.sendall(b"OK")
            elif "Command:" in command:
                command = command.split("Command:")[1].strip()
                print(f"Parsed Command: {command}")
                subprocess.run(["screen", "-S", screen_name, "-X", "stuff", f"{command}\n"], check=True)
                if command == "exploit":
                    while subprocess.run(["fuser", f"{listen_port}/tcp"], capture_output=True, text=True).returncode:
                        pass
                client_socket.sendall(b"OK")
            elif command == "exit":
                print("Exit command received from the server.")
                client_socket.sendall(b"OK")
                client_socket.close()
                break
            elif command == "EXPLOIT":
                subprocess.run(["screen", "-r", f"{screen_name}"], check=True)
                client_socket.sendall(b"OK")
                # subprocess.run(["gnome-terminal", "--", "screen", "-r", f"{screen_name}"], check=True)
            else:
                if "Port:" in command:
                    listen_port = int(command.split("Port:")[1].strip())
                    client_socket.sendall(b"OK")
                    
    except KeyboardInterrupt:
        print("Program terminated by the user.")
    except ConnectionRefusedError:
        print("Connection refused. Please check the server.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        try:
            subprocess.run(["screen", "-S", screen_name, "-X", "quit"], check=True)
            client_socket.close()
        except:
            pass

if __name__ == '__main__':
    connect_to_server()