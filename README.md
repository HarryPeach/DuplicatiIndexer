# DuplicatiIndexer

> 📃 A way to easily find files that exist within a Duplicati backup 

## What is this

When [Duplicai](https://www.duplicati.com/) creates a backup, it creates an index file called `filelist.json`. This file can often be gigabytes in size, making it very hard to search for files within the backup.

This project creates an index file that is on average 2.5% the size of the `filelist.json` and is easily searchable with the program.