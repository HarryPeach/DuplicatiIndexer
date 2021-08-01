import ijson
from expects import expect, equal
from jsonpy.__main__ import decode_filelist


def test_decode_filelist():
    """Tests the decode_filelist function."""
    dec_str = decode_filelist('./tests/resources/sample_filelist.json')
    objects = ijson.items(bytes(dec_str, 'utf-8'), 'item')

    file_count = 0
    folder_count = 0
    for obj in objects:
        if obj["type"] == "File":
            file_count += 1
        elif obj["type"] == "Folder":
            folder_count += 1

    expect(file_count).to(equal(2))
    expect(folder_count).to(equal(1))
