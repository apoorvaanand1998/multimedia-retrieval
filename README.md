Setup Python, [Poetry](https://python-poetry.org/) and check out it's [Basic Usage](https://python-poetry.org/docs/basic-usage/).

To clone the project run `git clone --recurse-submodules git@github.com:apoorvaanand1998/multimedia-retrieval.git`

To install dependencies 
1. `cd multimedia-retrieval/mr-tool`
2. `poetry install --no-root`

To run 
1. `cd mr-tool`
2. Run `poetry shell` and `cd ..`
3. Run `python mr-tool/src/__init__.py <filename>` (eg. `python mr-tool/src/__init__.py "Tree/D00096.obj"`)

The code for the different steps are split-up into different branches. Specifically, check out the readmes of each branch to see what is going on, and how one can run the code.
