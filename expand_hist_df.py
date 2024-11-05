import pandas as pd

original_hist_df = pd.read_csv('')
# Initialize an empty list to store expanded DataFrames
expanded_dfs = []

# Iterate through each column
for col in original_hist_df.columns:
    # Create a DataFrame where each array element becomes a separate column
    expanded_col_df = pd.DataFrame(original_hist_df[col].tolist(), index=original_hist_df.index)
    
    # Rename columns to include the original column name as a prefix
    expanded_col_df.columns = [f"{col}_{i}" for i in range(expanded_col_df.shape[1])]
    
    # Append the expanded DataFrame to the list
    expanded_dfs.append(expanded_col_df)

# Concatenate all expanded columns along with the original index
expanded_df = pd.concat(expanded_dfs, axis=1)
