# Easysploit

## Overview
Easysploit Client is a simple tool that generates code to request payload creation from the Easysploit Server. It enables users to customize payload generation with options like admin privilege escalation `-a` and threading `-t`.The generated code can be used to execute the payload directly.

## Features
- Admin Request `-a`: Generate requesting code to server with admin privilege escalation.
- Threading `-t`: Request  requesting code to server with threading support for faster execution.
- Base64 Encoding `-e`: Include base64 encoding for the payload.
- Input File `-f`: Load the payload from a specified input file.
- Output File `-o`: Save the generated code to a specified output file.

## Installation
```
git clone https://github.com/Easysploit/easysploit-client.git
cd easysploit-client
```

## Usage
```
python3 easysploit.py <Attacker-IP> <Port> [-a] [-t] [-e] [-o <output-file>] [-h]
```
- `<Attacker-IP>`: Attacker's local IP address.
- `<Port>`: Listening port on the attacker's machine.
- `-a`: Request admin privilege escalation (optional)
- `-t`: Request threading support for the payload (optional)
- `-e`: Include base64 encoding for the payload (optional)
- `-f <Input file>`: Load the payload from a specified input file (optional)
- `-o <Output file>`: Save the generated code to a specified output file (optional)
- `-h`: Display help message

## Example
```
python3 easysploit.py 192.168.0.1 4444 -a -t -e -o payload.py
```

# Autosploit

## Overview
This project is built to automate reverse TCP session creation, streamlining exploit workflows while avoiding antivirus detection. By utilizing a central server, it generates custom, fileless payloads and ensures connected attackers can execute them seamlessly, setting up TCP sessions automatically in real-time without leaving traces.
**You don't have to create msfconsole listener session manually, just run the server and client, and you are good to go.**

## Features
- Central Server: Manage and control multiple attackers with a central server.
- Real-Time: Automatically set up reverse TCP sessions when payload creation is requested from target machines.
- Automatic TCP Sessions: Automatically set up reverse TCP sessions for connected attackers.

## Usage
```
python3 autosploit.py
```

## License
This project is licensed under the MIT License.

## Terms of Use
This tool is provided for **legal pentesting tests** and should only be used in **authorized environments**.  
Any illegal activity performed using this tool is the **sole responsibility of the user**.  
By using this tool, you agree to these terms and accept full legal responsibility for its use.