"""Functions for searching an index
"""
import marisa_trie
import logging
import gzip
import pickle
import typer

from pathlib import Path

from jsonpy.utilities import check_input_file


def search_index(input_file: Path, search_term: str):
    """Search for a term in a created index

    Args:
        input_file (Path): The index file to search
        search_term (str): The term to search for within the index
    """
    if not check_input_file(input_file):
        raise typer.Exit(code=1)

    trie = _load_gzipped_trie(input_file)
    matches = [s for s in trie.items() if search_term in s[0]]
    logging.debug(f"Found {len(matches)} match(es)")
    typer.echo([x[0] for x in matches])


def _load_gzipped_trie(file: str) -> marisa_trie.Trie:
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
