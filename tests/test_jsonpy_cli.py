from typer.testing import CliRunner
from pathlib import Path
from expects import expect, equal, be_true, contain, be_none

import os
import re

from jsonpy.__main__ import app

runner = CliRunner()

# The sample filelist
SAMPLE_FILELIST_PATH = "tests/resources/sample_filelist.json"
# The sample index
SAMPLE_INDEX_PATH = "tests/resources/sample_index.gz"


def test_create_index():
    """Tests that the cli will successfully create an index"""
    OUTPUT_FILE_PATH = "tests/resources/index.marisa.gz"

    result = runner.invoke(
        app,
        ['create', SAMPLE_FILELIST_PATH,
         OUTPUT_FILE_PATH])

    expect(result.exit_code).to(equal(0))
    expect(Path(OUTPUT_FILE_PATH).exists()).to(be_true)

    try:
        os.remove(OUTPUT_FILE_PATH)
    except OSError:
        pass


def test_create_index_err():
    """Tests that the cli create will error when invalid arguments are provided"""
    OUTPUT_FILE_PATH = "tests/resources/index.marisa.gz"

    result = runner.invoke(
        app,
        ['create', "invalid_file.invalid",
         OUTPUT_FILE_PATH])

    expect(result.exit_code).to(equal(1))


def test_search_index():
    """Tests that the cli will successfully search an index"""
    result = runner.invoke(
        app,
        ['search', SAMPLE_INDEX_PATH, "my", "--no-color"])

    expect(result.exit_code).to(equal(0))
    expect(
        result.output).to(
        contain("C:\\data\\mydoc.txt", "C:\\data\\myvideo.mp4"))

    result = runner.invoke(
        app,
        ['search', SAMPLE_INDEX_PATH, "invalid_search_value"])

    expect(result.exit_code).to(equal(0))
    expect(
        result.output).to_not(
        contain("C:\\data\\mydoc.txt", "C:\\data\\myvideo.mp4"))


def test_search_index_color_opt():
    """Tests that the color option successfully disables colour output"""
    result = runner.invoke(
        app,
        ['search', SAMPLE_INDEX_PATH, "my"])

    ansi_regex = re.compile("\\\x1b\\[\\d{2}m")

    expect(ansi_regex.search(result.output)).to_not(be_none)

    result = runner.invoke(
        app,
        ['search', SAMPLE_INDEX_PATH, "my", "--no-color"])

    ansi_regex = re.compile("\\\x1b\\[\\d{2}m")

    expect(ansi_regex.search(result.output)).to(be_none)


def test_search_index_err():
    """Tests that the cli search will error when invalid arguments are provided"""
    result = runner.invoke(
        app,
        ['search', "invalid_file.invalid", "valid_search_value"])

    expect(result.exit_code).to(equal(1))
