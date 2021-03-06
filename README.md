
FILETAGGING
===========
A Python package providing some utilities to manage tagging of files.

Usage: `filetagging [OPTIONS]... COMMANDS...`

Commands are executed in the order they are specified. Batch files will be run
before regular commands.

Options
-------
 - `-f, --file <file>` -- Run commands from a batch file.
 - `--help` -- Program usage information.
 - `--version` -- Program version information.

Commands
--------
- `ls [<filename> | <directory>]` -- Lists the tags associated with a file or
    directory. Without an argument, print the tags in the current directory.
- `filter <tag> [directory]` -- Lists the files tagged with a tag.
- `add <tag> <filename>` -- Add a tag to a file.
- `rm <tag> <filename>` -- Remove a tag from a file.
- `mv <source> <destination>` -- Move or rename a file.

Building and Installation
-------------------------
Install the latest `setuptools` and `build` packages and build the `filetagging`
module.
```
pip install --upgrade setuptools build
python -m build
```

Install the built package through `pip`.
```
pip install filetagging*.whl
```

And finally run the installed `filetagging` package.
```
python -m filetagging
```
