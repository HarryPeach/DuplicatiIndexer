"""Functions for searching an index
"""
import marisa_trie
import logging
import gzip
import pickle
import typer

from pathlib import Path

from jsonpy.utilities import check_input_file


def search_index(input_file: Path, search_term: str, color: bool) -> None:
    """Search for a term in a created index

    Args:
        input_file (Path): The index file to search
        search_term (str): The term to search for within the index
        color (bool): Whether color output should be enabled
    """
    if not check_input_file(input_file):
        raise typer.Exit(code=1)

    trie = _load_gzipped_trie(input_file)
    matches = [s for s in trie.items() if search_term in s[0]]
    logging.debug(f"Found {len(matches)} match(es)")
    _show_searches([x[0] for x in matches], search_term, color)


def _show_searches(matches: list, search_term: str, color: bool) -> None:
    """Shows the search results in a readable format

    Args:
        matches (list): The list of matches
        search_term (str): The term searched for
        color (bool): Whether ANSI color should be enabled
    """
    for item in matches:
        if color:
            print(_get_color_split_string(item, search_term))
        else:
            print(item)


def _get_color_split_string(string: str, keyword: str) -> str:
    """Returns a string with the keyword highlighted

    Args:
        string (str): The string to highlight
        keyword (str): The keyword to highlight
    """
    import re
    split = re.split(f"({keyword})", string)

    arranged_string = ""
    flag = True
    for item in split:
        if flag:
            arranged_string = arranged_string + '\033[39m'
            arranged_string = arranged_string + item
        else:
            arranged_string = arranged_string + "\033[92;1m"
            arranged_string = arranged_string + item
            arranged_string = arranged_string + '\033[0m'
        flag = not flag

    arranged_string = arranged_string + '\033[0m'

    return arranged_string


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
