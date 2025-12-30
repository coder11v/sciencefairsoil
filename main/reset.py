import os
import shutil

def reset_out_folder():
    # Define the target directory
    target_dir = 'out'

    # Check if the directory exists
    if not os.path.exists(target_dir):
        print(f"The directory '{target_dir}' does not exist. Creating it now...")
        os.makedirs(target_dir)
        return

    # Iterate over the contents of the folder
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        try:
            # Check if it is a file or a symbolic link, then delete
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it is a directory, skip it (preserve all folders and their contents)
            elif os.path.isdir(file_path):
                pass  # Do nothing - preserve the directory and everything in it
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    print(f"Successfully reset '{target_dir}/' — all files deleted, folders and their contents preserved.")

if __name__ == "__main__":
    reset_out_folder()