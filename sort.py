import os
import pathlib 
import shutil 
import re 
import random
import argparse

# path = r"C:\Users\jp120\Desktop\Bałagan"
path = argparse.ArgumentParser()
path.add_argument('path_to_folder_Balagan')
path = path.parse_args()
path = path.path_to_folder_Balagan

os.chdir(path)

LIST_OF_DIR = ['images', 'documents', 'audio', 'video', 'archives', 'others']
EXT_IMAGES = ['.JPEG', '.PNG', '.JPG', '.SVG']
EXT_VIDEO = ['.AVI', '.MP4', '.MOV', '.MKV']
EXT_DOCUMENTS = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
EXT_AUDIO = ['.MP3', '.OGG', '.WAV', '.AMR']
EXT_ARCHIVE = ['.ZIP', '.GZ', '.TAR']
LIST_OF_EXT = [EXT_IMAGES, EXT_VIDEO, EXT_DOCUMENTS, EXT_AUDIO, EXT_ARCHIVE]


def create_directories(list_of_dir):
    for dir in list_of_dir:
        if not pathlib.Path(dir).exists():
            os.mkdir(dir)


def sort(path):
    
    create_directories(LIST_OF_DIR)
    sort_files(path)
    deleting_dirs(path)
    normalize(path)
    unpack_archives(path)
    data(path)


def create_balagan (path, list_of_ext):
    alphabet = 'abcdefghijłĄŹżćklmnopqrstuwyxz'
    num_of_files = random.randint(10, 50)
    for file in range (num_of_files):
        file_name = ''
        for char in range(random.randint(3,11)):
            file_name += random.choice(alphabet)

        ext_choice = random.choice(random.choice(list_of_ext)) 
        if ext_choice == '.ZIP':
            file_name +=  '.txt'
            with open(file_name, 'w') as file:
                file.write('a')
            shutil.make_archive(file_name, 'zip', path,file_name)

        elif ext_choice ==  '.GZ':
            file_name +=  '.txt'
            with open(file_name, 'w') as file:
                file.write('a')
            shutil.make_archive(file_name, 'gztar', path,file_name)
        elif ext_choice == '.TAR':
            file_name +=  '.txt'
            with open(file_name, 'w') as file:
                file.write('a')
            shutil.make_archive(file_name, 'tar', path,file_name)
        
        else:
            file_name +=  ext_choice
            with open(file_name, 'w') as file:
                file.write('a')


def sort_files(path, path_inner_dir = path):
    for el in pathlib.Path(path_inner_dir).iterdir():
        if el.is_file():
            file_extension = (el.suffix).upper()
            base_path = path + '\\'
            base_suffix = '\\'+ el.name
            if file_extension in EXT_ARCHIVE:
                destination_folder = 'archives'
            elif file_extension in EXT_AUDIO:
                destination_folder = 'audio'
            elif file_extension in EXT_DOCUMENTS:
                destination_folder = 'documents'
            elif file_extension in EXT_IMAGES:
                destination_folder = 'images'
            elif file_extension in EXT_VIDEO:
                destination_folder = 'video'
            else: 
                destination_folder = 'others'

            destination = base_path + destination_folder + base_suffix
            el.replace(destination)
            
        elif el.name not in LIST_OF_DIR:
            print(path_inner_dir + base_suffix)
            sort_files(path, path_inner_dir = path_inner_dir + base_suffix)


def data(path):
    for dir in pathlib.Path(path).iterdir():
        print('\n\nLista plików dla folderu:', dir.name)
        ext_set = set()

        for file in pathlib.Path(path+'\\'+dir.name).iterdir():
            print(file.name)
            ext_set.add(file.suffix)
        if dir.name == 'others':
            print('\nLista rozszerzeń nierozpoznanych: ', ext_set)
        else:
            print('\nLista rozszerzeń dla folderu: ', ext_set)


def deleting_dirs(path):
    for el in pathlib.Path(path).iterdir():
        if el.name not in LIST_OF_DIR:
            shutil.rmtree(el)


def normalize(path):
    polish_to_english = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
        'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }

    for dir in pathlib.Path(path).iterdir():
        if dir.name == 'others':
            continue

        for file in pathlib.Path(path+'\\'+dir.name).iterdir():
            file_new_name = file.name[:]
            for polish, english in polish_to_english.items():
                
                file_new_name = (file_new_name).replace(polish, english)
            file_new_name = re.sub(r'[^.\w]', '_', file_new_name)
            file_new_name = str(dir) +'\\' + file_new_name
            os.rename(file, file_new_name)
            
def unpack_archives(path):
    for archive in pathlib.Path(path + '\\archives').iterdir():

        if ((str(os.path.splitext(str(archive))[1])).upper()) in EXT_ARCHIVE and not archive.is_dir():
            shutil.unpack_archive(str(archive), str(os.path.splitext(str(archive))[0]))
            os.remove(str(archive))


# create_balagan(path, list_of_ext)

sort(path)
