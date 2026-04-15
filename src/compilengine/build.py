import tomllib
from .. import cli


def build(name: str, author: str):
    REGISTRY_BASE = (
        "https://raw.githubusercontent.com/sawn1c-repos/registry/main/packages"
    )
    url = f"{REGISTRY_BASE}/{author}/{name}.toml"
    tomllib.load(url)
    if author not in url or author == "":
        cli.error(
            f"Package {name} by {author} requires a valid author (to specify the package)"
        )
    elif name not in url or name == "":
        cli.error(
            f"Package {name} by {author} requires a valid name (to specify the package)"
        )
