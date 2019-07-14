import argparse
import logging

from . import backend
from . import config
from . import osutil

log = logging.getLogger("userstorage")


def main():
    parser = argparse.ArgumentParser(
        description='Set up storage tests')
    parser.add_argument("command", choices=["setup", "teardown"])
    parser.add_argument("config_file", help="Configuration file")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(name)s] %(levelname)-7s %(message)s")

    cfg = config.load_config(args.config_file)

    if args.command == "setup":
        setup(cfg)
    elif args.command == "teardown":
        teardown(cfg)


def setup(cfg):
    osutil.create_dir(cfg.BASE_DIR)

    for b in cfg.BACKENDS.values():
        try:
            b.setup()
        except backend.Error as e:
            if b.required:
                raise
            log.warning("Skipping %s storage: %s", b.name, e)


def teardown(cfg):
    for b in cfg.BACKENDS.values():
        b.teardown()

    osutil.remove_dir(cfg.BASE_DIR)


if __name__ == "__main__":
    main()