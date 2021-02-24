from getfilelistpy import getfilelist
from google_drive_downloader import GoogleDriveDownloader as gdd
import json
import os
import smart_format

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


def lookup_files_in_folders(folders, sorted_folders, drive_dict):
    for f in sorted_folders:
        all_files = get_files_in_folders(folders[f])
        for fi in all_files:
            file_name = smart_format.replace_me(fi["name"], transliter=True)  #
            download_file_from_google_drive(fi["id"], file_name)
            chapters.append(file_name)
            index_builder(drive_dict)


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
    smart_format.content_parser(file_path)


def index_builder(drive_dict):
    file_path = os.path.join(os.getcwd(), "source", "index.rst")
    output = f'''{drive_dict["name"]}
=================================

.. toctree::
   :maxdepth: 2
   :caption: Оглавление:


'''
    with open(file_path, 'w', encoding='utf-8') as writer:
        writer.write(output)
        for ch in chapters.sort():
            writer.write("   "+ch+"\n")


def to_html():
    os.system("make github")
    smart_format.html_add_comments()


def worm():
    folders, sorted_folders = get_folders(worm_dict)
    lookup_files_in_folders(folders, sorted_folders, worm_dict)
    index_builder(worm_dict)
    to_html()


if __name__ == '__main__':
    worm()
