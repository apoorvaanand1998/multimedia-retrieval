import os

DB_ORIGINAL_NAME = "ShapeDatabase_INFOMR"
DB_RELATIVE_PATH = os.path.join("..", "..", DB_ORIGINAL_NAME)

OUTPUT_DIR_RELATIVE_PATH = os.path.join("..", "..", "Output")
STATS_FILE_NAME = "stats.csv"
STATS_FILE_HEADERS = "Name,Class,Vertices,Faces(Cells),Triangles,Quads,BBox"

UI_MAIN_APP_TITLE = "Multimedia Retrieval Assignment"
UI_NO_ITEM_SELECTED_PLACEHOLDER = "Choose an item from the database"
UI_NO_STATS_FILE = "No statistics file found at " + os.path.join(OUTPUT_DIR_RELATIVE_PATH, STATS_FILE_NAME)
UI_STATS_BUTTON = "Compute Statistics"

