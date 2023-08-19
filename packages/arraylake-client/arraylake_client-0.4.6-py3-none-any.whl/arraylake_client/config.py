import os
from pathlib import Path

import yaml
from donfig import Config

user_config_dir = Path(os.getenv("ARRAYLAKE_CLIENT_CONFIG", "~/.config/arraylake_client/")).expanduser()
user_config_file = user_config_dir / "config.yaml"

fn = Path(__file__).resolve().parent / "config.yaml"
with fn.open() as f:
    defaults = yaml.safe_load(f)
config = Config("arraylake_client", paths=[user_config_dir], defaults=[defaults])

# maybe move a copy of the defaults to the user config space
config.ensure_file(
    source=fn,
    comment=True,
)
