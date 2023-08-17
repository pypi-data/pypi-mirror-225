import os
import requests
import random
import time
import shutil
from win10toast import ToastNotifier
from sampacks.non_use_funcs import (
    image_downloader,
    image_check
)

# Declarations

toaster = ToastNotifier()


class mainfuncs:
    def __init__(self):
        pass

    def coder(self, text):
        """
        Encodes the given text by adding random letters before and after the reversed string.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.
        """
        random_number = ''.join(random.choices(
            'abcdefghijklmnopqrstuvwxyz', k=3))
        text = text.lower()
        text_reverse = text[::-1]
        encoded = random_number + text_reverse + random_number
        return encoded

    def decoder(self, text):
        """
        Decodes the given text by removing the random letters added by the `coder` function.

        Args:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.
        """
        encoded = text[3:-3]
        decoded = encoded[::-1].capitalize()
        return decoded

    def words_capitalizer(self, obj, print_output=False):
        """
        Capitalizes the words in a string or a list of strings.

        Args:
            obj (str or list): The string or list of strings to capitalize.
            print_output (bool): If True, prints the capitalized words. Defaults to False.

        Returns:
            str or list: The capitalized words.
        """
        if isinstance(obj, str):
            words = obj.split()
            capitalized_words = [word.capitalize() for word in words]
            capitalized_text = ' '.join(capitalized_words)
            if print_output:
                print(capitalized_text)
            else:
                return capitalized_text
        elif isinstance(obj, list):
            capitalized_words = [word.capitalize() for word in obj]
            if print_output:
                print(capitalized_words)
            else:
                return capitalized_words

    def words_upper(self, obj, print_output=False):
        """
        Converts the words in a string or a list of strings to uppercase.

        Args:
            obj (str or list): The string or list of strings to convert.
            print_output (bool): If True, prints the converted words. Defaults to False.

        Returns:
            str or list: The converted words.
        """
        if isinstance(obj, str):
            words = obj.split()
            uppercase_words = [word.upper() for word in words]
            uppercase_text = ' '.join(uppercase_words)
            if print_output:
                print(uppercase_text)
            else:
                return uppercase_text
        elif isinstance(obj, list):
            uppercase_words = [word.upper() for word in obj]
            if print_output:
                print(uppercase_words)
            else:
                return uppercase_words

    def words_lower(self, obj):
        """
        Converts the words in a string or a list of strings to lowercase.

        Args:
            obj (str or list): The string or list of strings to convert.

        Returns:
            str or list: The converted words.
        """
        if isinstance(obj, str):
            words = obj.split()
            lowercase_words = [word.lower() for word in words]
            lowercase_text = ' '.join(lowercase_words)
            return lowercase_text
        elif isinstance(obj, list):
            lowercase_words = [word.lower() for word in obj]
            return lowercase_words

    def image_check(self, url):
        valid_extensions = ('png', 'jpg', 'jpeg', 'webp', 'svg')
        valid_domains = ('encrypted-tbn0.gstatic.com',
                         'unsplash', 'pexels', 'image')
        check = None

        for i in valid_extensions:
            if url.split('/')[1] != '' and url.split('/')[1].startswith(i):
                check = True
            elif url.split('/')[1] != '' and url.split('/')[2].startswith(i):
                check = True
            else:
                check = False

        if any(url.endswith(ext) for ext in valid_extensions) or any(domain in url for domain in valid_domains) or check == True:
            return True
        return False

    def downloader(self, url, **kwargs):
        """
        Downloads a file from a given url.
        Args:
            url: Url For The File You Wanna Download.
        Kwargs:
            name: Enter The Name Of The File
            chunk: Chunck_Size For Iter_Content
            location: Where To Save The File.
        Returns:
            Downloads: The Files.
            0.8
        """

        if image_check(url) == True:
            image_downloader(url, **kwargs)
        else:
            if 'name' in kwargs:
                name = kwargs['name']
                raws = url.split('/')[-1]
                join = ''.join(raws)
                if 'extension' in kwargs:
                    name = name + kwargs['extension']
                else:
                    extension = '.' + join.split('.')[1]
                    name = name + extension
            else:
                name = url.split('/')[-1]

            if 'chunk' in kwargs:
                chunk_raw = kwargs['chunk']
                if type(chunk_raw) == int:
                    chunk = chunk_raw
            else:
                chunk = 500

            if 'location' in kwargs:
                location_raw = kwargs['location']
                if os.path.exists(location_raw):
                    location = location_raw
            else:
                location = ''

            file = requests.get(url, stream=True)
            try:
                os.chdir(location)
            except OSError:
                pass
            with open(name, 'wb') as files:
                for i in file.iter_content(chunk_size=chunk):
                    files.write(i)

    def reminder(self, timing, message, title):
        """
        Reminds User A Specific Message On Certain Time.
        Args:
            timing: Intervals Between Reminder
            message: Message To Reminded
            title: Title Of The Reminder
        Returns:
            Reminder As Windows Notification.
        """
        toaster.show_toast(title, message, duration=timing, threaded=True)
        while toaster.notification_active:
            time.sleep(1)

    def sorter(self, path_to_folder, **kwargs):
        """
        Sorts files in a folder into subfolders based on their file extensions.

        Args:
            path_to_folder (str): Path to the folder containing the files to be sorted.
            names (dict, optional): Dictionary mapping file extensions to custom folder names.

        Example:
            To sort files in a folder into subfolders based on their extensions:
            >>> sorter = FileSorter()
            >>> sorter.sorter('/path/to/folder')
            This will create subfolders like '/path/to/folder/png', '/path/to/folder/txt', etc.

            To sort files into custom-named folders:
            >>> custom_names = {'jpg': 'images', 'txt': 'text_files'}
            >>> sorter.sorter('/path/to/folder', names=custom_names)
            This will create subfolders like '/path/to/folder/images', '/path/to/folder/text_files', etc.
        """
        try:
            if 'names' in kwargs:
                names = kwargs['names']
            else:
                names = {}

            ptf = path_to_folder
            for i in os.listdir(ptf):
                splitname = i.split('.')
                if len(splitname) > 1:
                    ext = splitname[1]
                    try:
                        if names.get(ext) is None:
                            folder_name = ext
                            os.mkdir(os.path.join(path_to_folder, ext))
                        else:
                            folder_name = names[ext]
                            os.mkdir(os.path.join(path_to_folder, folder_name))
                    except FileExistsError:
                        shutil.move(os.path.join(path_to_folder, i),
                                    os.path.join(path_to_folder, folder_name, i))
                    shutil.move(os.path.join(path_to_folder, i),
                                os.path.join(path_to_folder, folder_name, i))
        except FileNotFoundError:
            pass

    def file_getter(self, path_to_folder, **kwargs):
        """
        Retrieves files based on specified criteria from a given folder.

        Args:
            path_to_folder (str): Path to the folder containing the files.
            ext (str, optional): File extension to filter by.
            extension (str, optional): Alternative name for the file extension filter.
            name (str, optional): File name to filter by.
            names (dict, optional): Dictionary mapping file extensions to folder names.

        Returns:
            list: A list containing pairs of file names and their corresponding paths.

        Example:
            To get a list of all .txt files in a folder:
            >>> getter = FileGetter()
            >>> result = getter.file_getter('/path/to/folder', ext='txt')
            >>> print(result)
            [('file1.txt', '/path/to/folder/file1.txt'), ('file2.txt', '/path/to/folder/file2.txt')]
        """
        if 'ext' in kwargs:
            ext = kwargs['ext']
        elif 'extension' in kwargs:
            ext = kwargs['extension']
        else:
            ext = None

        if 'name' in kwargs:
            name = kwargs['name']
        elif 'filename' in kwargs:
            name = kwargs['filename']
        else:
            name = None

        results = []
        for i in os.listdir(path_to_folder):
            splitted = i.split('.')
            if len(splitted) > 1:
                if (ext is None or splitted[1] == ext) and (name is None or splitted[0] == name):
                    results.append([i, os.path.join(path_to_folder, i)])
        return results

    def search(self, path_to_folder, **kwargs):
        """
        Search for files based on specified criteria in a given folder.

        Args:
            path_to_folder (str): Path to the folder containing the files and/or folders.
            ext (str, optional): File extension to filter by.
            extension (str, optional): Alternative name for the file extension filter.
            name (str, optional): File name to filter by.
            names (dict, optional): Dictionary mapping file extensions to folder names.

        Returns:
            list: A list of lists containing pairs of file names and their corresponding paths.

        Example:
            To search for all .txt files in a folder and its subfolders:
            >>> getter = FileGetter()
            >>> result = getter.search('/path/to/folder', ext='txt')
            >>> print(result)
            [
                [('file1.txt', '/path/to/folder/file1.txt'), ('file2.txt', '/path/to/folder/file2.txt')],
        """
        mf = mainfuncs()
        if 'ext' in kwargs:
            ext = kwargs['ext']
        elif 'extension' in kwargs:
            ext = kwargs['extension']
        else:
            ext = None

        if 'name' in kwargs:
            name = kwargs['name']
        elif 'filename' in kwargs:
            name = kwargs['filename']
        else:
            name = None

        if name is None and ext is None:
            raise ValueError("At Least Provide On Value Name Or Extension")

        ptf = path_to_folder
        folders = os.listdir(ptf)
        all_folder = False
        all_files = False
        mixed = False
        length = len(folders)
        ctr = 0
        for i in folders:
            try:
                i.split('.')[1]
                ctr += 1
            except Exception as e:
                pass

        if ctr == length:
            all_files = True
        elif ctr == 0:
            all_folder = True
        elif ctr != length and ctr != 0:
            mixed = True

        if all_files:
            return mf.file_getter(ptf, **kwargs)
        elif all_folder:
            main = []
            for folder in folders:
                path = f"{ptf}/{folder}"
                main.append(mf.file_getter(path, **kwargs))
            return main
        elif mixed:
            total_folders = []
            returning = []

            for i in folders:
                try:
                    i.split('.')[1]
                except Exception as e:
                    total_folders.append(i)

            for folder in total_folders:
                path = f"{ptf}/{folder}"
                returning.append(mf.file_getter(path, **kwargs))

            returning.append(mf.file_getter(ptf, **kwargs))

            return returning
