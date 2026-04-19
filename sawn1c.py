import sys
import subprocess
import platform

# Add the current directory to the path so we can import src
sys.path.insert(0, ".")

from src import cli  # noqa: E402
from src.compilengine import build  # noqa: E402

system = platform.system()
if system not in ("Linux", "Darwin"):
    print("Sawn1c is only supported on Linux and macOS.")
    sys.exit(1)

print("Welcome to Sawn1c! Type 'sawn1c help' for available commands.")

subprocess.run(["touch", "sawn1c.toml"])

commands = {
    "install": cli.install,
    "uninstall": cli.uninstall,
}

flags = {
    "--build": build.build,
}


def parse_package_string(pkg_string):
    """Parse 'author/package' format into (author, package)"""
    if "/" in pkg_string:
        parts = pkg_string.split("/")
        if len(parts) == 2:
            return parts[0], parts[1]
    return None, pkg_string


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sawn1c <command> [args]")
        print("       sawn1c install author/package [--build]")
        print("       sawn1c uninstall author/package")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        if cmd == "install" and args:
            # Parse author/package format
            author, name = parse_package_string(args[0])

            if author is None:
                print("Error: Package must be in 'author/package' format")
                sys.exit(1)

            # Check for --build flag
            build_flag = "--build" in args

            # Install the package
            cli.install(name, author)

            # Build if --build flag is present
            if build_flag:
                print(f"Building {name}...")
                build.build(name, author)

        elif cmd == "uninstall" and args:
            # Parse author/package format
            author, name = parse_package_string(args[0])

            if author is None:
                print("Error: Package must be in 'author/package' format")
                sys.exit(1)

            cli.uninstall(name, author)

        elif cmd == "help":
            print("Available commands:")
            print("  install author/package [--build]")
            print("  uninstall author/package")
        else:
            print(f"Unknown command '{cmd}'.")
    except Exception as e:
        print(f"Error: {e}")
