import platform
import subprocess
from linux import connect_to_server

class MissingDependencyError(Exception):
    pass

class UnsupportedOSError(Exception):
    pass

def check_environment():
    allowed_os = ['Linux']
    if platform.system() not in allowed_os:
        raise UnsupportedOSError("This script can only be run on allowed operating systems.\nAllowed operating systems: " + ', '.join(allowed_os))
    if platform.system() == 'Linux':
        check_linux()
    

def check_linux():
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