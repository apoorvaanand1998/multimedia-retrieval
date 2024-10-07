import os
import random
import shutil


def sample_files_from_subdirectories(source_dir, dest_dir, percentage):
    """
    Iterate over subdirectories in `source_dir` and copy a percentage of files to `dest_dir`.

    Args:
        source_dir (str): Path to the directory containing subdirectories.
        dest_dir (str): Path to the destination directory where sampled files will be copied.
        percentage (float): Percentage of files to copy from each subdirectory (0 < percentage <= 100).
    """
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over each subdirectory in the source directory
    for subdir in os.listdir(source_dir):
        subdir_path = os.path.join(source_dir, subdir)
        if os.path.isdir(subdir_path):
            # List all files in the current subdirectory
            files = [f for f in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, f))]

            # Calculate number of files to sample
            num_files_to_sample = int(len(files) * (percentage / 100))

            # Randomly select files to copy
            sampled_files = random.sample(files, num_files_to_sample)

            # Create corresponding subdirectory in the destination directory
            dest_subdir_path = os.path.join(dest_dir, subdir)
            if not os.path.exists(dest_subdir_path):
                os.makedirs(dest_subdir_path)

            # Copy the sampled files to the destination subdirectory
            for file in sampled_files:
                src_file_path = os.path.join(subdir_path, file)
                dest_file_path = os.path.join(dest_subdir_path, file)
                shutil.copy(src_file_path, dest_file_path)

            print(f"Copied {num_files_to_sample}/{len(files)} files from {subdir_path} to {dest_subdir_path}")


if __name__ == "__main__":
    source_directory = 'ShapeDatabase_INFOMR'
    destination_directory = 'ShapeDB_sample'
    percentage_of_files = 100
    sample_files_from_subdirectories(source_directory, destination_directory, percentage_of_files)
