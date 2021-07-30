import gzip
import ijson
import shutil


# def get_items():
#     convertStreamToUtf8 = codecs.getreader('utf-8-sig')
#     with open('filelist.json', 'r') as zipentry:
#         with convertStreamToUtf8(zipentry) as zipentryutf8:
#             print(zipentry.read())
#             data = ijson.parse(zipentryutf8)

def gzip_index(file, outfile):
    with open(file, 'rb') as f_in:
        with gzip.open(outfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            # f_out.writelines(f_in)


def create_index(file, outfile):
    with open(file, 'r') as f:
        objects = ijson.items(f, "item.path")

        with open(outfile, 'w') as index_out:
            for o in objects:
                index_out.write(o + '\n')


def decode_utf8_bom(file: str, outfile: str):
    """Decode the file from UTF-8-SIG to UTF-8

    Args:
        file (str): The input file
        outfile (str): The output file
    """
    # read file as utf-8-sig
    s = open(file, mode='r', encoding='utf-8-sig').read()
    # write file as utf-8
    open(outfile, mode='w', encoding='utf-8').write(s)


if __name__ == "__main__":
    decode_utf8_bom("filelist.json", "out.json")
    create_index("out.json", "index.idx")
    gzip_index("index.idx", "index.gdx")
