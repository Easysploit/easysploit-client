import platform
import subprocess
from linux import connect_to_server as connect_to_server_linux

class MissingDependencyError(Exception):
    pass

class UnsupportedOSError(Exception):
    pass

def check_environment():
    allowed_os = ['Linux']
    current_os = platform.system()
    if current_os not in allowed_os:
        raise UnsupportedOSError("This script can only be run on allowed operating systems.\nAllowed operating systems: " + ', '.join(allowed_os))
    if current_os == 'Linux':
        check_linux()
    return current_os

    
def check_linux():
    required_commands = ["screen", "msfconsole"]
    for command in required_commands:
        if subprocess.run(["which", command], capture_output=True, text=True).returncode != 0:
            raise MissingDependencyError(f"Required command '{command}' is not installed on Linux.")

def main():
    try:
        check_environment()
        if platform.system() == 'Linux':
            connect_to_server_linux()
    except (UnsupportedOSError, MissingDependencyError) as e:
        print(f"Cannot run the script: {e}")

if __name__ == '__main__':
    main()