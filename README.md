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

### Step 6
This is WRT to the `StepSix` directory. 

- `basic_metrics.py` calculates TP, FP, TN, FN values
- `presix.py` does some preprocessing based on DataFrames we get from the end of StepFour and StepFive
- `roc.py` is where the metrics calculation functions exist
- `metrics.py` was used to create the `.csv`s for each mesh in batches
- `agg.py` aggregates everything to give us `grand_metrics.csv`.

The expectation for this branch is that we have a directory called `FINAL_remeshed_repaired_normalized_ShapeDB` containing a directory with pre-processed meshes which has been run through the aforementioned pipeline

### Step 5 and Step 4

This is WRT to the `StepFive` and `StepFour` directory. Both these steps require a `matrix.csv` to be present. This is a matrix of feature vectors. More info on how it's built below

- `HNSW.py` builds a graph for Dimensionality Reduction with the function `g()`. This graph is passed to `df` with an input mesh to get a dataframe mentioned in Step 6 (`presix.py`)
- `create_matrix.py` helps us create the matrix of feature vectors. Once again the `FINAL_remeshed_repaired_normalized_ShapeDB` directory of preprocessed meshes is a prerequisite.
- `z_normalize.py` normalizes the global descriptors in our matrix.
- `read_csv.py` assumes we have a directory of CSVs for our Shape Property Descriptors (More about that in the `shape-prop-desc` branch) and is for the convenience of reading these CSVs and combining them in `matrix.csv`
- `expand_hist_df.py` is where we convert our vector of histogram descriptors into a bunch of scalars. Our plan was to do feature weighing here, but we didn't have the time to finish this.
- `dist.py` gives us a dataframe returning the Euclidean distances of our Mesh with all other Meshes as mentioned in Step 6.
