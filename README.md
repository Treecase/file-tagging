
TAGGING
=======
A program providing some utilities to manage tagging of files.

Commands
--------
- `ls <filename>` -- Lists the tags associated with a file.
- `filter <tag>` -- Lists the files tagged with a tag.
- `add <tag> <filename>` -- Add a tag to a file.
- `rm <tag> <filename>` -- Remove a tag from a file.
- `mv <source> <destination>` -- Move or rename a file.

Building
--------
Install the latest `setuptools` and `build` modules and build the package.
```
pip install --upgrade setuptools build
python -m build
```

And install the built package through `pip`.
```
pip install filetagging*.whl
```

And finally run the installed package.
```
python -m filetagging
```
