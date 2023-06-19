import os
import shutil
import sys

image_extensions = ("jpeg", "png", "jpg", "svg")
video_extensions = ("avi", "mp4", "mov", "mkv")
document_extensions = ("doc", "docx", "txt", "pdf", "xlsx", "pptx")
audio_extensions = ("mp3", "ogg", "wav", "amr")
archive_extensions = ("zip", "gz", "tar")
known_extensions = set()
unknown_extensions = set()
iter_numb = 0

def normalize(text):    # Нормализация текста
    translit_dict = {
          "а": "a",
          "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "yo",
            "ж": "zh",
            "з": "z",
            "и": "i",
            "й": "y",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "h",
            "ц": "ts",
            "ч": "ch",
            "ш": "sh",
            "щ": "sch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
            "А": "A",
            "Б": "B",
            "В": "V",
            "Г": "G",
            "Д": "D",
            "Е": "E",
            "Ё": "YO",
            "Ж": "ZH",
            "З": "Z",
            "И": "I",
            "Й": "Y",
            "К": "K",
            "Л": "L",
            "М": "M",
            "Н": "N",
            "О": "O",
            "П": "P",
            "Р": "R",
            "С": "S",
            "Т": "T",
            "У": "U",
            "Ф": "F",
            "Х": "H",
            "Ц": "TS",
            "Ч": "CH",
            "Ш": "SH",
            "Щ": "SCH",
            "Ъ": "",
            "Ы": "Y",
            "Ь": "",
            "Э": "E",
            "Ю": "YU",
            "Я": "YA",
          }
    normalized = ""
    for char in text:
        if char.isalpha():
            if char in translit_dict:
                normalized += translit_dict[char]
            elif 64 < ord(char) > 91 or 96 < ord(char) > 123:
                normalized += char
            else:
                normalized += "_"
        elif char.isdigit():
            normalized += char
        else:
            normalized += "_"
    return normalized

def normalize_file_name(file_name):  # Нормализация имени файла
    file_name_splitted = file_name.split(".")
    file_extension = file_name_splitted.pop(-1)
    file_name = ""
    for name in file_name_splitted:
        file_name += name
    normalized_file_name = normalize(file_name) + "." + file_extension
    return normalized_file_name, file_extension

def remove_dirs(folder_path):   # Удаление пустых папок
    for root, dirs, _ in os.walk(folder_path):
        for dir in dirs:
            folder_path = os.path.join(root, dir)
            if folder_path not in [
                "archives",
                "video",
                "audio",
                "documents",
                "images",
            ] and not os.listdir(folder_path):
                os.removedirs(folder_path)

def process_file(file_path, folder_path):  # Обработка одного файла
    file_name = os.path.basename(file_path)
    normalized_file_name, file_extension = normalize_file_name(file_name)
    normalized_file_path = os.path.join(folder_path, normalized_file_name)
    os.rename(file_path, normalized_file_path)

    if file_extension in image_extensions:
        destination_folder = "images"
        known_extensions.add(file_extension)
    elif file_extension in video_extensions:
        destination_folder = "video"
        known_extensions.add(file_extension)
    elif file_extension in document_extensions:
        destination_folder = "documents"
        known_extensions.add(file_extension)
    elif file_extension in audio_extensions:
        destination_folder = "audio"
        known_extensions.add(file_extension)
    elif file_extension in archive_extensions:
        destination_folder = "archives"
        known_extensions.add(file_extension)
        destination_folder = os.path.join(folder_path, destination_folder)
        destination_folder = os.path.join(destination_folder, file_name)
        shutil.unpack_archive(normalized_file_path, destination_folder)
        os.remove(normalized_file_path)
    else:
        destination_folder = "unknown"
        unknown_extensions.add(file_extension)

    destination_folder_path = os.path.join(folder_path, destination_folder)
    os.makedirs(destination_folder_path, exist_ok=True)
    try:
        shutil.move(normalized_file_path, destination_folder_path)
    except shutil.Error:
        normalized_file_name = (str(iter_numb) + normalize_file_name(file_name)[0])
        normalized_file_path_new = os.path.join(
            folder_path, normalized_file_name)
        os.rename(normalized_file_path, normalized_file_path_new)
        shutil.move(normalized_file_path_new, destination_folder_path)
    except FileNotFoundError:
        pass

def process_folder(folder_path): # Обработка директории
    for root, _, files in os.walk(folder_path):
        if any(
            folder in root
            for folder in ["archives", "video", "audio", "documents", "images"]
        ):
            continue
        for file_name in files:
            global iter_numb
            iter_numb += 1
            file_path = os.path.join(root, file_name)
            process_file(file_path, folder_path)

def cleaning(): # Основная функция
    if len(sys.argv) < 2:
        print("Please enter folder path")
        sys.exit
    else:
        folder_path = sys.argv[1]
        process_folder(folder_path)
        remove_dirs(folder_path)
    print(f"Известные расширения:{known_extensions}\nНеизвестные расширения:{unknown_extensions}")

if __name__ == "__main__":
    cleaning()
