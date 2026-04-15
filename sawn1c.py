import sys
import subprocess
import tomllib
import platform

system = platform.system()
if system not in ("Linux", "Darwin"):
    print("Sawn1c is only supported on Linux and macOS.")
    sys.exit(1)

# Add the current directory to the path so we can import src
sys.path.insert(0, ".")

from src import cli
from src.compilengine import build

print("Welcome to Sawn1c! Type 'sawn1c help' for available commands.")

subprocess.run(["touch", "sawn1c.toml"])

commands = {
    "install": cli.install,
}

flags = {
    "--build": build.build,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sawn1c <command> [args]")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]
    try:
        if cmd in commands:
            commands[cmd](*args)
        elif cmd in flags:
            flags[cmd](*args)
        elif cmd == "help":
            print("Available commands:")
            for command in commands:
                print(f"  {command}")
        else:
            print(f"Unknown command '{cmd}'.")
    except TypeError as e:
        print(f"Addidtional Arugments required for command '{cmd}'")
