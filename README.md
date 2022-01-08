
TAGGING
=======
A program providing some utilities to manage tagging of files.

Commands
--------
- `ls <filename>` -- Lists the tags associated with a given file.
- `filter <tag>` -- Lists the files tagged with a given tag.
- `add <tag> <filename>` -- Add a tag to the given file.
- `rm <tag> <filename>` -- Remove a tag from the given file.

Building
--------
Install the latest `setuptools` and `build` modules, then build the package.
```
pip install --upgrade setuptools build
python -m build
```