# easysploit-client
## Overview
Easysploit Client is a simple tool for generating and customizing payloads by requesting their creation from the Easysploit Server. It provides a way to directly execute the generated payloads and supports additional customizations such as admin privilege escalation `-a` and threading `-t`.

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
