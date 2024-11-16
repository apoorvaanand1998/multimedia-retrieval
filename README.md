Setup Python, [Poetry](https://python-poetry.org/) and check out it's [Basic Usage](https://python-poetry.org/docs/basic-usage/).

To clone the project run `git clone --recurse-submodules git@github.com:apoorvaanand1998/multimedia-retrieval.git`

To install dependencies 
1. `cd multimedia-retrieval/mr-tool`
2. `poetry install --no-root`

To run 
1. `cd mr-tool`
2. Run `poetry shell` and `cd ..`
3. Run `python mr-tool/src/__init__.py <filename>` (eg. `python mr-tool/src/__init__.py "Tree/D00096.obj"`)

Before running, download the different Databases and supporting files and folders:
1. Download the .zip from https://drive.google.com/drive/folders/1y_vEdfwZUfW2cIBNpMoLZBegCo-6HZ3m?usp=sharing
2. Unzip
3. Copy all folders in the root directory of the project
