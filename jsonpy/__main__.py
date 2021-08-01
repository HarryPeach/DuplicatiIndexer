import gzip
import ijson
import pickle
import click
import logging
from jsonpy import __version__
import marisa_trie


def save_gzipped_trie(decoded_file: str, output_file: str):
    """Create a gzipped trie index from the decoded filelist

    Args:
        decoded_file (str): The decoded filelist string object
        output_file (str): The output file path
    """
    objects = ijson.items(decoded_file, "item.path")
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


@click.group()
@click.option("--verbose/--no-verbose", default=False)
def cli(verbose):
    """Index tools for Duplicati backups"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path(exists=False))
def create(input_file, output_file):
    """Create an index from a filelist.json file

    Args:\n
        input_file (str): The path to the filelist.json file\n
        output_file (str): The path to the created index
    """
    decoded = decode_filelist(input_file)
    save_gzipped_trie(decoded, output_file)


@cli.command()
@click.argument('input_file', type=click.Path(exists=False))
@click.argument('search_term', type=click.STRING)
def search(input_file, search_term):
    """Search for a term in a created index

    Args:\n
        input_file (str): The path to the index file\n
        search_term (str): The term to search for
    """
    trie = load_gzipped_trie(input_file)
    matches = [s for s in trie.items() if search_term in s[0]]
    logging.debug(f"Found {len(matches)} match(es)")
    click.echo([x[0] for x in matches])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[%(levelname)s] %(message)s")
    logging.info(f"DuplicatiIndexer v{__version__}")
    cli()
