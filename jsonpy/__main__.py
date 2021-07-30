import gzip
import ijson
import marisa_trie
import pickle


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


if __name__ == "__main__":
    decoded = decode_filelist("filelist.json")
    save_gzipped_trie(decoded, "index.marisa.gz")

    trie = load_gzipped_trie("index.marisa.gz")
    matches = [s for s in trie.items() if "cool" in s[0]]
    print(matches)
