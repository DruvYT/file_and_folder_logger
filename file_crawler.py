import os

def list_items_in_folder(folder_path):
    return os.listdir(folder_path)

def is_directory(item_path):
    return os.path.isdir(item_path)
