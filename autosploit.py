import os
import platform
import subprocess
from linux import connect_to_server

class MissingDependencyError(Exception):
    pass

class UnsupportedOSError(Exception):
    pass

def check_environment():
    if platform.system() != 'Linux':
        raise UnsupportedOSError("This script can only be run on Linux systems.")
    
    required_commands = ["screen", "msfconsole"]
    for command in required_commands:
        if subprocess.run(["which", command], capture_output=True, text=True).returncode != 0:
            raise MissingDependencyError(f"Required command '{command}' is not installed.")

def main():
    try:
        check_environment()
        connect_to_server()
    except (UnsupportedOSError, MissingDependencyError) as e:
        print(f"Cannot run the script: {e}")

if __name__ == '__main__':
    main()