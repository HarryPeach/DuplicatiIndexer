import ijson
import os
from expects import expect, equal
from jsonpy.__main__ import decode_filelist, load_gzipped_trie, save_gzipped_trie, app


SAMPLE_FILELIST_PATH = "./tests/resources/sample_filelist.json"
INDEX_PATH = "./tests/resources/index.marisa.gz"


def test_decode_filelist():
    """Tests the decode_filelist function."""
    dec_str = decode_filelist(SAMPLE_FILELIST_PATH)
    objects = ijson.items(bytes(dec_str, 'utf-8'), "item")

    file_count = 0
    folder_count = 0
    for obj in objects:
        if obj["type"] == "File":
            file_count += 1
        elif obj["type"] == "Folder":
            folder_count += 1

    expect(file_count).to(equal(2))
    expect(folder_count).to(equal(1))


def test_trie_conversion():
    """Tests that an index can be created, and then successfully read from"""
    decoded = decode_filelist(SAMPLE_FILELIST_PATH)
    save_gzipped_trie(decoded, INDEX_PATH)
    trie = load_gzipped_trie(INDEX_PATH)

    expect(trie.items()[0][0]).to(equal("C:\\data\\"))
    expect(trie.items()[1][0]).to(equal("C:\\data\\mydoc.txt"))
    expect(trie.items()[2][0]).to(equal("C:\\data\\myvideo.mp4"))

    # Remove the created file afterwards
    try:
        os.remove(INDEX_PATH)
    except OSError:
        pass
