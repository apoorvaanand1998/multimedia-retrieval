Setup Python, [Poetry](https://python-poetry.org/) and check out it's [Basic Usage](https://python-poetry.org/docs/basic-usage/).

To clone the project run `git clone --recurse-submodules git@github.com:apoorvaanand1998/multimedia-retrieval.git`

To install dependencies 
1. `cd multimedia-retrieval/mr-tool`
2. `poetry install --no-root`

To run 
1. `cd mr-tool`
2. Run `poetry shell` and `cd ..`
3. Run `python mr-tool/src/__init__.py <filename>` (eg. `python mr-tool/src/__init__.py "Tree/D00096.obj"`)

## How the Code Works

This branch only concerns the generation of Shape Property Descriptors (The rest of StepThree is in other branches). Each SPD gets it's own `.py` file and the Histogram generation happens at `hist_gen.py`. This file assumes that we have the `FINAL_remeshed_repaired_normalized_ShapeDB` preprocessed mesh directory. It outputs a bunch of csvs to `Output/ShapePropDesc2`, a CSV for every class. Within the CSV, the ordering goes `(A3, mesh1), (A3, mesh2)...(A3, meshn), (D1, mesh1), ...(D4, meshn)`
