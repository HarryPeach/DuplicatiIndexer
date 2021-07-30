import gzip
import ijson


def create_gzip_from_filelist(decoded_file: str, output_file: str):
    """Create a gzipped index from the decoded filelist

    Args:
        decoded_file (str): The decoded filelist string object
    """
    objects = ijson.items(decoded_file, "item.path")
    with gzip.open(output_file, 'wb') as f_out:
        for o in objects:
            f_out.write(bytes(o + '\n', 'utf-8'))


def decode_gzipped_index(input_file: str, output_file: str):
    """Converts a gzipped index file to a plaintext index file

    Args:
        input_file (str): Gzipped index file
        output_file (str): Plaintext index file
    """
    with gzip.open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for o in f_in:
            f_out.write(o.decode('utf-8'))


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
    create_gzip_from_filelist(decoded, "index.txt.gz")
    decode_gzipped_index("index.txt.gz", "index.txt")
