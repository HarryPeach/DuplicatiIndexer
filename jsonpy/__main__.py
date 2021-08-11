import typer
import logging
from pathlib import Path

from jsonpy import __version__
from jsonpy.create import create_index
from jsonpy.search import search_index

DEFAULT_FILELIST_NAME = "filelist.json"  # The default name of the filelist
DEFAULT_INDEX_NAME = "index.marisa.gz"  # The default name of the index file

app = typer.Typer(help="Create and search marisa-trie duplicati indexes")


@app.callback()
def main(verbose: bool = False):
    """
    Handle global options
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
    create_index(input_file, output_file)


@app.command()
def search(
        input_file: Path = typer.Argument(
            default=DEFAULT_INDEX_NAME, help="The path to the index file"),
        search_term: str = typer.Argument(..., help="The term to search for")):
    """Search for a term in a created index"""
    search_index(input_file, search_term)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(message)s")
    logging.info(f"DuplicatiIndexer v{__version__}")
    app()
