import tomllib
import zipfile
import io
import requests
import os
from .. import cli
from ..security import run_sandboxed_build


def build(pkg_name: str, pkg_author: str):
    # 1. Setup Paths
    # If these are remote, we must use requests
    toml_url = f"https://raw.githubusercontent.com/sawn1c-repos/registry/main/packages/{pkg_author}/{pkg_name}.toml"

    try:
        r = requests.get(toml_url)
        r.raise_for_status()
        meta = tomllib.loads(r.text)
    except Exception as e:
        cli.error(f"Could not fetch metadata: {e}")
        return

    # 2. Check Dependencies
    if os.path.exists("installedpkgs.toml"):
        with open("installedpkgs.toml", "rb") as i:
            installed = tomllib.load(i)
    else:
        installed = {}

    deps = meta.get("build", {}).get("dependencies", [])
    for dep in deps:
        if dep not in installed:
            cli.error(f"Missing dependency: {dep}. Please install it first.")
            return

    # 3. Download Source
    # Using 'binary_mirror' from your TOML example
    mirrors = meta.get("binaries", {}).get("binary_mirror", [])
    if not mirrors:
        cli.error("No download mirrors found in TOML.")
        return

    print(f"Downloading source from {mirrors[0]}...")
    source_req = requests.get(mirrors[0])

    # Extract to a work directory
    work_dir = f"./build_space/{pkg_name}"
    with zipfile.ZipFile(io.BytesIO(source_req.content)) as z:
        z.extractall(work_dir)

    # 4. Run the Sandbox Build (Importing from your other script)
    # This calls the configure/compile/install commands
    success = run_sandboxed_build(pkg_name, pkg_author, "./output_stage")

    if success:
        # Update your installedpkgs.toml
        with open("installedpkgs.toml", "a") as f:
            f.write(f'{pkg_name} = "{meta["package"]["version"]}"\n')
        print(f"Successfully built and recorded {pkg_name}")

    return success
