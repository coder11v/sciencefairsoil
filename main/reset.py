import os
import shutil
import csv

def reset_out_folder():
    """
    Reset the out folder by:
    1. Appending data from plant_data.csv to archive-demo/plant_data.csv (no header)
    2. Appending data from water.csv to archive-demo/water.csv (with header)
    3. Appending errors to archive-demo/errors.txt
    4. Moving all other files to archive-demo/
    5. Deleting the original files after archiving
    """
    target_dir = 'out'
    archive_dir = os.path.join(target_dir, 'archive-demo')
    
    # Check if the directory exists
    if not os.path.exists(target_dir):
        print(f"The directory '{target_dir}' does not exist. Creating it now...")
        os.makedirs(target_dir)
        return
    
    # Ensure archive directory exists
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"Created archive directory: {archive_dir}")
    
    # Files to handle specially
    plant_data_file = os.path.join(target_dir, 'plant_data.csv')
    water_file = os.path.join(target_dir, 'water.csv')
    errors_file = os.path.join(target_dir, 'errors.txt')
    
    archive_plant_data = os.path.join(archive_dir, 'plant_data.csv')
    archive_water = os.path.join(archive_dir, 'water.csv')
    archive_errors = os.path.join(archive_dir, 'errors.txt')
    
    # 1. Handle plant_data.csv - append data rows (skip header)
    if os.path.isfile(plant_data_file):
        try:
            with open(plant_data_file, 'r') as src:
                reader = csv.reader(src)
                header = next(reader, None)  # Skip the header row
                data_rows = list(reader)  # Get all data rows
            
            if data_rows:  # Only append if there's data
                with open(archive_plant_data, 'a', newline='') as dst:
                    writer = csv.writer(dst)
                    writer.writerows(data_rows)
                print(f"✓ Appended {len(data_rows)} rows to {archive_plant_data}")
            
            os.unlink(plant_data_file)
            print(f"✓ Deleted {plant_data_file}")
        except Exception as e:
            print(f'✗ Failed to process {plant_data_file}. Reason: {e}')
    
    # 2. Handle water.csv - append with header
    if os.path.isfile(water_file):
        try:
            with open(water_file, 'r') as src:
                content = src.read()
            
            if content.strip():  # Only append if there's content
                with open(archive_water, 'a') as dst:
                    dst.write(content)
                print(f"✓ Appended content to {archive_water}")
            
            os.unlink(water_file)
            print(f"✓ Deleted {water_file}")
        except Exception as e:
            print(f'✗ Failed to process {water_file}. Reason: {e}')
    
    # 3. Handle errors.txt - append content
    if os.path.isfile(errors_file):
        try:
            with open(errors_file, 'r') as src:
                content = src.read()
            
            if content.strip():  # Only append if there's content
                with open(archive_errors, 'a') as dst:
                    dst.write(content)
                print(f"✓ Appended errors to {archive_errors}")
            
            os.unlink(errors_file)
            print(f"✓ Deleted {errors_file}")
        except Exception as e:
            print(f'✗ Failed to process {errors_file}. Reason: {e}')
    
    # 4. Move all other files to archive-demo
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        
        # Skip the archive directory itself
        if os.path.isdir(file_path):
            continue
        
        try:
            # Skip the files we already handled
            if filename in ['plant_data.csv', 'water.csv', 'errors.txt']:
                continue
            
            # Move the file to archive-demo
            dst_path = os.path.join(archive_dir, filename)
            shutil.move(file_path, dst_path)
            print(f"✓ Moved {filename} to {archive_dir}")
        except Exception as e:
            print(f'✗ Failed to move {file_path}. Reason: {e}')
    
    print(f"\n✓ Successfully reset '{target_dir}/' — files archived and reset complete.")

if __name__ == "__main__":
    reset_out_folder()