Setup Python, [Poetry](https://python-poetry.org/) and check out it's [Basic Usage](https://python-poetry.org/docs/basic-usage/).

To clone the project run `git clone --recurse-submodules git@github.com:apoorvaanand1998/multimedia-retrieval.git`


## Important!
### Before running, download the different Databases and supporting files and folders:
1. Download the .zip from https://drive.google.com/drive/folders/1y_vEdfwZUfW2cIBNpMoLZBegCo-6HZ3m?usp=sharing
2. Unzip
3. Copy all folders in the root directory of the project
If you wanna test it its (from repo root folder):
- pipenv install -r requirements.txt
- pipenv shell
- cd mr-tool/src
- python _init_.py

## Make sure you have a Python (>= 3.11) installation on your machine
### after cloning/downloading repository execture following commands in project root folder

To install dependencies 
1. `pip install pipenv`
2. `pipenv install -r requirements.txt`

To run 
1. `pipenv shell`
2. `python mr-tool/src/__init__.py`
