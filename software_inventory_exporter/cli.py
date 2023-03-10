#!/usr/bin/env python3
"""Cli and main module."""

import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Any, List, Optional

import uvicorn
import yaml

from software_inventory_exporter.api import app

logger = logging.getLogger(__name__)


def main(argv: Optional[List[Any]] = None) -> None:
    """Program entry point."""
    parser = ArgumentParser(
        prog="Software Inventory Exporter",
        description="Exporter for apt packages and snaps in json via web",
    )
    parser.add_argument("config")
    args = parser.parse_args(argv)
    target_config = Path(args.config)

    if not target_config.is_file():
        logger.error("The config file doesn't exist.")
        raise SystemExit(1)

    try:
        config = yaml.safe_load(target_config.read_text(encoding="utf-8"))["settings"]
        uvicorn.run(app, host=config["bind_address"], port=int(config["port"]))

    except (KeyError, yaml.YAMLError) as error:
        logger.error("Config file wrong format: %s.", error)
        raise SystemExit(1) from error


if __name__ == "__main__":  # pragma: no cover
    main()
