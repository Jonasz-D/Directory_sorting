import os, pathlib, shutil, re, random, argparse

# path = r"C:\Users\jp120\Desktop\Bałagan"
path = argparse.ArgumentParser()
path.add_argument('path_to_folder_Balagan',)
path = path.parse_args()
path = path.path_to_folder_Balagan

os.chdir(path)

list_of_dir = ['images', 'documents', 'audio', 'video', 'archives', 'others']
ext_images = ['.JPEG', '.PNG', '.JPG', '.SVG']
ext_video = ['.AVI', '.MP4', '.MOV', '.MKV']
ext_documents = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
ext_audio = ['.MP3', '.OGG', '.WAV', '.AMR']
ext_archive = ['.ZIP', '.GZ', '.TAR']
list_of_ext = [ext_images, ext_video, ext_documents, ext_audio, ext_archive]


def create_directories(list_of_dir):
    for dir in list_of_dir:
        if not pathlib.Path(dir).exists():
            os.mkdir(dir)


def sort(path):
    
    create_directories(list_of_dir)
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
            if (el.suffix).upper() in ext_archive:
                el.replace(path + '\\' + 'archives'+'\\'+ el.name)
            elif el.suffix.upper() in ext_audio:
                el.replace(path + '\\' + 'audio' +'\\'+ el.name)
            elif el.suffix.upper() in ext_documents:
                el.replace(path + '\\' + 'documents'+'\\'+ el.name)
            elif el.suffix.upper() in ext_images:
                el.replace(path + '\\' + 'images'+'\\'+ el.name)
            elif el.suffix.upper() in ext_video:
                el.replace(path + '\\' + 'video'+'\\'+ el.name)
            else: 
                el.replace(path + '\\' + 'others'+'\\'+ el.name)
        elif el.name not in list_of_dir:
            print(path_inner_dir+'\\' + el.name)
            sort_files(path, path_inner_dir = path_inner_dir+'\\' + el.name)


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
        if el.name not in list_of_dir:
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

        if ((str(os.path.splitext(str(archive))[1])).upper()) in ext_archive and not archive.is_dir():
            shutil.unpack_archive(str(archive), str(os.path.splitext(str(archive))[0]))
            os.remove(str(archive))


# create_balagan(path, list_of_ext)

sort(path)
