import gzip
import ijson
import pickle
import typer
import logging
import marisa_trie
from pathlib import Path

from jsonpy import __version__

DEFAULT_FILELIST_NAME = "filelist.json"  # The default name of the filelist
DEFAULT_INDEX_NAME = "index.marisa.gz"  # The default name of the index file

app = typer.Typer(help="")


def save_gzipped_trie(decoded_file: str, output_file: str):
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


def load_gzipped_trie(file: str) -> marisa_trie.Trie:
    """Loads a gzipped index into a marisa trie

    Args:
        file (str): The path to the gzipped index

    Returns:
        marisa_trie.Trie: The trie object
    """
    trie = marisa_trie.Trie()
    logging.debug(f"Loading trie from file: {file}")
    with gzip.open(file, 'rb') as f_in:
        trie = pickle.loads(f_in.read())
    return trie


def decode_filelist(file: str):
    """Decode the file from UTF-8-SIG to UTF-8

    Args:
        file (str): The input file path

    Returns:
        str: The output file as a string object
    """
    # read file as utf-8-sig
    s = open(file, mode='r', encoding='utf-8-sig').read()
    return s


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
    return True


@app.callback()
def main(verbose: bool = False):
    """
    Manage users in the awesome CLI app.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)


@app.command()
def create(input_file: Path = typer.Argument(
        default=DEFAULT_FILELIST_NAME,
        help="The path to the filelist.json file"),
        output_file: Path = typer.Argument(
        default=DEFAULT_INDEX_NAME, help="The path to the created index")):
    """Create an index from a filelist.json file
    """
    if not check_input_file(input_file):
        raise typer.Exit(code=1)

    decoded = decode_filelist(input_file)
    save_gzipped_trie(decoded, output_file)


@app.command()
def search(
        input_file: Path = typer.Argument(
            default=DEFAULT_INDEX_NAME, help="The path to the index file"),
        search_term: str = typer.Argument(..., help="The term to search for")):
    """Search for a term in a created index"""
    if not check_input_file(input_file):
        raise typer.Exit(code=1)

    trie = load_gzipped_trie(input_file)
    matches = [s for s in trie.items() if search_term in s[0]]
    logging.debug(f"Found {len(matches)} match(es)")
    typer.echo([x[0] for x in matches])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(message)s")
    logging.info(f"DuplicatiIndexer v{__version__}")
    app.command()(main)
    app()
