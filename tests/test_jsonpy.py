from pathlib import Path
import ijson
import os
from expects import expect, equal, be_true, be_false
from jsonpy.create import _decode_filelist, _save_gzipped_trie
from jsonpy.search import _load_gzipped_trie
from jsonpy.utilities import check_input_file

RESOURCES_PATH = "./tests/resources"
SAMPLE_FILELIST_PATH = f"{RESOURCES_PATH}/sample_filelist.json"
INDEX_PATH = f"{RESOURCES_PATH}/index.marisa.gz"


def test_decode_filelist():
    """Tests the decode_filelist function."""
    dec_str = _decode_filelist(SAMPLE_FILELIST_PATH)
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


def test_check_input_file():
    """Tests that the input file is valid before continuing"""
    # Test directory
    expect(check_input_file(Path(RESOURCES_PATH))).to(be_false)
    # Test non-existent file
    expect(check_input_file(Path(f"{RESOURCES_PATH}/invalid.file"))).to(be_false)
    # Test .dlist.zip file
    expect(check_input_file(
        Path(f"{RESOURCES_PATH}/sample_dlist.dlist.zip"))).to(be_false)
    # Test valid file
    expect(check_input_file(Path(SAMPLE_FILELIST_PATH))).to(be_true)


def test_trie_conversion():
    """Tests that an index can be created, and then successfully read from"""
    decoded = _decode_filelist(SAMPLE_FILELIST_PATH)
    _save_gzipped_trie(decoded, INDEX_PATH)
    trie = _load_gzipped_trie(INDEX_PATH)

    expect(trie.items()[0][0]).to(equal("C:\\data\\"))
    expect(trie.items()[1][0]).to(equal("C:\\data\\mydoc.txt"))
    expect(trie.items()[2][0]).to(equal("C:\\data\\myvideo.mp4"))

    # Remove the created file afterwards
    try:
        os.remove(INDEX_PATH)
    except OSError:
        pass
