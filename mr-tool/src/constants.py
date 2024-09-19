import os

DB_RELATIVE_PATH = os.path.join("..", "..")

DB_ORIGINAL_NAME = "ShapeDatabase_INFOMR"
DB_ORIGINAL_RELATIVE_PATH = os.path.join("..", "..", DB_ORIGINAL_NAME)

DB_PREPROCESSED_NAME = "ShapeDatabase_INFOMR_preprocessed"
DB_PREPROCESSED_RELATIVE_PATH = os.path.join("..", "..", DB_PREPROCESSED_NAME)

OUTPUT_DIR_RELATIVE_PATH = os.path.join("..", "..", "Output")
STATS_FILE_NAME = "stats.csv"
STATS_FILE_HEADERS = "Path,Name,Class,Vertices,Faces(Cells),Triangles,Quads,BBox"

UI_MAIN_APP_TITLE = "Multimedia Retrieval Assignment"
UI_NO_ITEM_SELECTED_PLACEHOLDER = "Choose an item from the database"
UI_NO_STATS_FILE = "No statistics file found"
UI_STATS_BUTTON = "Compute Statistics"

DATABASES = [
    DB_ORIGINAL_NAME,
    DB_PREPROCESSED_NAME
]
