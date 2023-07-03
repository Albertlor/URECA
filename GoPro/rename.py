import os
import json

from datetime import datetime


def rename_gopro_files(folder_path):
    files = os.listdir(folder_path)
    path = './rename.json'
    check_file = os.path.isfile(path)

    if not check_file:
        with open('rename.json', 'w') as f1:
            json.dump({
                "YYYYMMDD_HHMM":0
            }, f1, indent=4)

    with open('rename.json') as f1:
        rename = json.load(f1)

    for file in files:
        if not file.startswith('.'):  # Skip hidden files
            old_name = os.path.join(folder_path, file)
            creation_time = os.path.getctime(old_name)
            timestamp = datetime.fromtimestamp(creation_time)
            new_name = timestamp.strftime(r"%Y%m%d_%H%M")
            new_name = os.path.join(folder_path, new_name)
            
            if new_name in rename:
                rename[new_name] += 1

            else:
                rename[new_name] = 0
                
            with open('rename.json', 'w') as f1:
                json.dump(rename, f1, indent=4)

            with open('rename.json') as f1:
                rename = json.load(f1)

            new_name = rf"{os.path.splitext(new_name)[0]}_{rename[new_name]}{os.path.splitext(file)[1]}"
            if not os.path.exists(new_name):
                os.rename(old_name, new_name)
                print(f"Renamed {file} to {new_name}", flush=True)
            else:
                print(f"Skipping {file} - File with the new name already exists")            


# Replace 'folder_path' with the path to your GoPro files folder
folder_path = r"C:\Users\Albertlor\Videos\testing"
rename_gopro_files(folder_path)