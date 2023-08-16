import os
import zipfile

def move_and_zip_files(source_folder, destination_folder):
    try:
        if not os.path.exists(source_folder):
            print(f"Source folder '{source_folder}' does not exist.")
            return

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        files = os.listdir(source_folder)

        for file in files:
            source_file_path = os.path.join(source_folder, file)
            destination_file_path = os.path.join(destination_folder, file + '.zip')

            if os.path.isdir(source_file_path):
                continue

            with zipfile.ZipFile(destination_file_path, 'w') as zip_file:
                zip_file.write(source_file_path, os.path.basename(source_file_path))
            
            os.remove(source_file_path)

            print(f"File '{file}' zipped and moved to '{destination_folder}'")

    except Exception as e:
        print(f"error: {e}")

if __name__ == '__main__':
    source_folder_path = '/path/to/source/folder'
    destination_folder_path = '/path/to/destination/folder'
    move_and_zip_files(source_folder_path, destination_folder_path)
