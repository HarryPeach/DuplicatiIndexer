# DuplicatiIndexer

> 📃 A way to easily find files that exist within a Duplicati backup 

## What is this

When [Duplicai](https://www.duplicati.com/) creates a backup, it creates an index file called `filelist.json`. This file can often be gigabytes in size, making it very hard to search for files within the backup.

This project creates an index file that is on average 40x smaller than `filelist.json` and is easily searchable with the program.

## How does it work

The program uses `ijson` to stream the massive JSON index and creates a "[MARISA trie](https://github.com/s-yata/marisa-trie)" of the paths found. Since the items are stored in the "trie" (as seen below) they can be searched by a prefix very quickly.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Trie_example.svg/400px-Trie_example.svg.png)

## How do I use it?

1. Install [Python 3](https://python.org) and [Poetry](https://python-poetry.org/)
2. Run `poetry install` in the project root dir
3. `TODO: Create command line interface`