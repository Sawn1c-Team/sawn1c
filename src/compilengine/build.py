import tomllib
from .. import cli


def build(name: str, author: str):
    REGISTRY_BASE = (
        "https://raw.githubusercontent.com/sawn1c-repos/registry/main/packages"
    )
    url = f"{REGISTRY_BASE}/{author}/{name}.toml"
    if author not in url or author == "":
        cli.error(
            f"Package {name} by {author} requires a valid author (to specify the package)"
        )

    # TOML reading for building
    with open(f"{url}", "rb") as f:
        meta = tomllib.load(f)

    build_mode = meta["build"]["type"]
    deps = meta["build"]["dependencies"]
    conf_method = meta["build"]["configure"]
    compile_command = meta["build"]["compile"]
    install_command = meta["build"]["install"]
    if build_mode not in ("autoconf", "cmake", "meson", "custom",):
        cli.error(
            f"Unsupported build type '{build_mode}' for package '{name}' by '{author}'."
        )
    
    for dep in deps:
        cli.install(dep)

    print(f"Building {author}/{name}...")

