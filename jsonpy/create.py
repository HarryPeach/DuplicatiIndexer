"""Functions for creation of an index
"""
import ijson
import pickle
import gzip
import logging
import typer
import marisa_trie

from pathlib import Path

from jsonpy.utilities import check_input_file


def create_index(input_file: Path, output_file: Path):
    """Create an index from a filelist.json file

    Args:
        input_file (Path): The input file to create an index from
        output_file (Path): Where to write the index to

    Raises:
        typer.Exit: Exits if the file is not valid
    """
    if not check_input_file(input_file):
        raise typer.Exit(code=1)

    decoded = _decode_filelist(input_file)
    _save_gzipped_trie(decoded, output_file)


def _save_gzipped_trie(decoded_file: str, output_file: str):
    """Create a gzipped trie index from the decoded filelist

    Args:
        decoded_file (str): The decoded filelist string object
        output_file (str): The output file path
    """
    objects = ijson.items(bytes(decoded_file, "utf-8"), "item.path")
    trie = marisa_trie.Trie(objects)
    data = pickle.dumps(trie)
    with gzip.open(output_file, 'wb') as f_out:
        f_out.write(data)
    logging.info(f"Index written to: {output_file}")


def _decode_filelist(file: str):
    """Decode a file from UTF-8-SIG to UTF-8

    Args:
        file (str): The input file path

    Returns:
        str: The output file as a string object
    """
    # read file as utf-8-sig
    s = open(file, mode='r', encoding='utf-8-sig').read()
    return s
