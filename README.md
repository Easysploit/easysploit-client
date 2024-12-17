# easysploit-client
## Overview
Easysploit Client is a simple tool that generates code to request payload creation from the Easysploit Server. It enables users to customize payload generation with options like admin privilege escalation `-a` and threading `-t`. The generated code can be used to execute the payload directly.

## Features
- Admin Request (-a): Generate requesting code to server with admin privilege escalation.
- Threading (-t): Request  requesting code to server with threading support for faster execution.

## Installation
```
git clone https://github.com/Easysploit/easysploit-client.git
cd easysploit-client
```

## Usage
```
python3 easysploit_client.py <Attacker-IP> <Port> [-a] [-t]
```
- `<Attacker-IP>`: Attacker's local IP address.
- `<Port>`: Listening port on the attacker's machine.
- `-a`: Request admin privilege escalation (optional)
- `-t`: Request threading support for the payload (optional)

## Example
```
python3 easysploit_client.py 192.168.0.1 4444 -a -t
```

## License
This project is licensed under the MIT License.
