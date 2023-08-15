from PIL import Image
import os
import hashlib


def get_last_modification(file):
    """get time of last modification of passed file

    Args:
        file (str): absolute path of file
    """
    if file is not None:
        if os.path.exists(file):
            return os.stat(file).st_mtime
        else:
            return None
    else:
        return None


def get_smallest_image(directory):
    """Based on a directory with images return the smallest horizontal image

    Args:
        directory (str): Path containing images

    Returns:
        str: Absolute file path
    """
    img_list = [directory + file for file in os.listdir(directory)]
    size_sorted = sorted(img_list, key=os.path.getsize)

    r = None
    for image in size_sorted:
        img = Image.open(image)
        if img.size[0] > img.size[1]:
            r = image
            break

    if r != None:
        return r
    elif size_sorted:
        return size_sorted[0]
    else:
        return None


def get_file_sha1(file_path: str):
    try:
        with open(file_path, "r") as f:
            data = f.read()
            file_sha1 = hashlib.sha1(data.encode("utf-8")).hexdigest()
            return file_sha1
    except Exception as e:
        print(f"Error:\n{e}")
