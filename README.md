# DuplicatiIndexer

> 📃 A way to easily find files that exist within a Duplicati backup 

## What is this

When [Duplicati](https://www.duplicati.com/) creates a backup, it creates an index file called `filelist.json`. This file can often be gigabytes in size, making it very hard to search for files within the backup.

This project creates an index file that is on average 40x smaller than `filelist.json` and is easily searchable with the program.

## How does it work

The program uses `ijson` to stream the massive JSON index and creates a "[MARISA trie](https://github.com/s-yata/marisa-trie)" of the paths found. Since the items are stored in the "trie" (as seen below) they can be searched by a prefix very quickly.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Trie_example.svg/400px-Trie_example.svg.png)

## How do I use it?

1. Install [Python 3](https://python.org) and [Poetry](https://python-poetry.org/)
2. Run `poetry install` in the project root directory
3. Retrieve the `filelist.json` file from the backup's `*.dlist.zip` archive
4. To create an index:
   1. Run `poetry run python -m jsonpy create [input] [output]`
   2. If you run this command without arguments it will, by default, ingest a file called `filelist.json` and spit out `index.marisa.gz`
5. To search an existing index
   1. Run `poetry run python -m jsonpy search [input] [search term]`

## What is this licensed under?

```
  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
```