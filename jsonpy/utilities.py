"""Shared utilities across the app
"""
import logging

from pathlib import Path


def check_input_file(input_file: Path) -> bool:
    """Checks that a provided input file is valid

    Args:
        input_file (Path): The input file path

    Returns:
        bool: Whether file is valid or not
    """
    if input_file.is_dir():
        logging.error("The provided input file was a directory")
        return False
    elif not input_file.exists():
        logging.error("The provided input file did not exist")
        return False
    elif input_file.name.endswith(".dlist.zip"):
        logging.error(
            "You must first extract the filelist.json from the *.dlist.zip and run the"
            "program on that instead")
        return False
    return True
