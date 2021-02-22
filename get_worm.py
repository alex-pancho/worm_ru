from getfilelistpy import getfilelist
from google_drive_downloader import GoogleDriveDownloader as gdd
import requests
import json
import os

api_key = None
with open('credentials.json') as json_file:
    credentials = json.load(json_file)
    api_key = credentials.get("api_key")

assert api_key is not None, "api_key is None, check your credentials.json"

worm_dict = {
    "name": "Червь",
    "id": "0B3PmMCiEMlvcRW9QTWtxbjBYN0U",
    "exclude_folders": [
        'Worm (Червь)',
        '!_ORIGINAL_source',
        'Часть 99 - Всё, что нельзя пропустить',
        'Главчервестат'
        ]
    }
chapters = []

def get_drive_source(drive_id, mode="folder"):
    resource = {
        "api_key": api_key,
        "id": drive_id,
        "fields": "files(name,id)",
        }
    if mode == "folder":
        return getfilelist.GetFolderTree(resource)
    else:
        return getfilelist.GetFileList(resource)


def get_folders(drive_dict):
    worm_folder_id = drive_dict["id"]
    res = get_drive_source(worm_folder_id)
    folders_names = res['names']
    folders_id = res['folders']
    folders = dict(zip(folders_names, folders_id))
    for f in drive_dict["exclude_folders"]:
        del folders[f]
    sorted_folders = sorted(folders)
    return folders, sorted_folders


def get_files_in_folders(folder_id):
    all_files = get_drive_source(folder_id, "f").get('fileList')[0].get("files")
    return all_files


def lookup_files_in_folders(folders, sorted_folders):
    for f in sorted_folders:
        all_files = get_files_in_folders(folders[f])
        for fi in all_files:
            download_file_from_google_drive(fi["id"], fi["name"])
            chapters.append(fi["name"])
            input("c..")


def download_file_from_google_drive(file_id, file_name, mime=None):

    if mime is None:
        mime = 'txt'
    file_name = file_name+".rst"
    file_path = os.path.join(os.getcwd(), "source", file_name)
    gdd.download_file_from_google_drive(
        file_id=file_id,
        dest_path=file_path,
        overwrite=True,
        mime=mime
        )

    with open(file_path, 'r', encoding='utf-8') as reader:
        output = reader.readline()
        output = output + reader.readline()
        for line in reader:
            output = output + line.replace("\n", "\n\n")
    with open(file_path, 'w', encoding='utf-8') as writer:
        writer.write(output)

def index_builder(drive_dict, chapters):
    file_path = os.path.join(os.getcwd(), "source", "index.rst")
    output = f'''
    {drive_dict["name"]}
=================================

.. toctree::
   :maxdepth: 2
   :caption: Оглавление:


'''
    with open(file_path, 'w', encoding='utf-8') as writer:
        writer.write(output)
        for ch in chapters:
            writer.write(ch)


def main():
    folders, sorted_folders = get_folders(worm_dict)
    lookup_files_in_folders(folders, sorted_folders)
    index_builder(worm_dict, chapters)



if __name__ == '__main__':
    main()
