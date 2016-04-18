import zipfile
import glob
import os
import json
import errno
import sys
import shutil
from functools import reduce
from PIL import Image
from collections import OrderedDict


class MyProject(object):

    def unzip_file(self, source_path, destination_path):
        with zipfile.ZipFile(source_path) as zfile:
            zfile.extractall(destination_path)
            zfile.close()

    def create_thumbnail(self, source_path, destination_path):
        size = 100, 100
        image = Image.open(source_path)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(destination_path)
        image.close()

    def create_thumbnails(self, file_name):
        text_to_append = "_thumbnail."
        file_name_components = file_name.split('.')
        new_file_name = file_name_components[0] + text_to_append + file_name_components[1]
        self.create_thumbnail(file_name, new_file_name)

    def json_reader(self, file_path):
        with open(file_path) as data_file:
            data = json.load(data_file)
            return data

    def create_and_step_into_directory(self, directory):
        try:
            os.makedirs(directory)
            os.chdir(directory)
        except OSError:
            print("Error, could not create directory: " + directory)
            raise

    def create_folder_tree(self, images_directory, directory_tree):
        for directory in directory_tree:
            if "." in directory:
                self.copy_files(images_directory + "\\" + directory, os.getcwd())
                self.create_thumbnails(directory)
                print("Found file: " + directory)
            else:
                self.create_and_step_into_directory(directory)
                self.create_folder_tree(images_directory, directory_tree[directory])
        os.chdir("..")

    def create_folders(self, images_directory):
        data = self.json_reader(images_directory + "\\manifest.json")
        structure = data["directory_structure"]
        self.create_folder_tree(images_directory, structure)

    def copy_files(self, image_directory, destination):
        shutil.copy(image_directory, destination)

    def zip_folder(self, source_path):
        shutil.make_archive("simonsZip", "zip", source_path)

    def zip_dir(self, zipname, dir_to_zip):
        dir_to_zip_len = len(dir_to_zip.rstrip(os.sep)) + 1
        with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zf:
            for dirname, subdirs, files in os.walk(dir_to_zip):
                for filename in files:
                    path = os.path.join(dirname, filename)
                    entry = path[dir_to_zip_len:]
                    zf.write(path, entry)

    def zipdir(path, zip_filename):
        zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(path):
            for file in files:
                zipf.write(os.path.join(root, file))
        zipf.close()

    def Main(self):
        if ".zip" in sys.argv[1]:
            self.unzip_file(str(sys.argv[1]), str(sys.argv[2]))
            print('Number of arguments:', len(sys.argv), 'arguments.')
            print('Argument List:', str(sys.argv[1]))
        else:
            IMAGES_DIRECTORY = os.path.abspath(sys.argv[1])
            self.create_folders(IMAGES_DIRECTORY)
            print('Not a zip file')


run = MyProject()
#file_list = ['images/jpeg.jpeg', 'images/page04b.jpg']
#run.unzip_file("package.zip", "images")
IMAGES_DIRECTORY = os.path.abspath("./images")
IMAGES_THEMES = os.path.abspath("./image_themes")
#run.create_thumbnail('images/jpeg.jpeg', 'images/jpeg_thumbnail.jpeg')
#run.rename_image('images/jpeg.jpeg')
#run.create_thumbnails(file_list)
#print(run.json_reader("images/manifest.json"))
#run.create_folders(IMAGES_DIRECTORY)
#run.zip_folder("./images_themes")
#run.zipdir('./image_themes/', "jake.zip")
#run.zipper(IMAGES_THEMES, "juanito.zip")
run.Main()