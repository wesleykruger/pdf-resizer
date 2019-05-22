import os
import fnmatch
import shutil
import PyPDF2
from pathlib import Path

# Enter your directories here. Use absolute paths.
source_directory = Path("C:/Users/wesleykruger/Documents/PenFed/")  # Where zip file is located


def check_directory():
    if not os.path.exists(source_directory):
        raise Exception("The specified source directory does not exist. Please check your spelling and try again:"
                        "{}".format(source_directory))


def create_directories(root_directory):
    global unzipping_directory
    global pickup_directory
    os.mkdir(os.path.join(root_directory, 'drop-area'))
    os.mkdir(os.path.join(root_directory, 'pickup-area'))
    unzipping_directory = os.path.join(root_directory, 'drop-area')
    pickup_directory = os.path.join(root_directory, 'pickup-area')


def unzip_to_new_directory(start_directory, end_directory):
    pattern = "*.zip"
    for root, dirs, files in os.walk(os.path.abspath(start_directory)):
        for filename in fnmatch.filter(files, pattern):
            shutil.unpack_archive(os.path.join(root, filename), end_directory)


def scale(pdf_path, final_path):
    for file in os.listdir(pdf_path):
        print(file)
        pdf_file_obj = open(os.path.join(pdf_path, file), 'rb')
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        pdf_writer = PyPDF2.PdfFileWriter()  # We will be writing to a new file with scaled dimensions

        for page in range(pdf_reader.numPages):
            page_obj = pdf_reader.getPage(page)
            page_obj.scaleTo(612, 792)  # Measured in points, multiply by 72 for inches
            pdf_writer.addPage(page_obj)

        new_file = open(os.path.join(final_path, file), 'wb')
        pdf_writer.write(new_file)
        pdf_file_obj.close()
        new_file.close()


def zip_folder(zip_this_directory):
    shutil.make_archive(os.path.join(source_directory, 'archive'), 'zip', zip_this_directory)


def remove_leftover_files():
    shutil.rmtree(unzipping_directory)
    shutil.rmtree(pickup_directory)


if __name__ == '__main__':
    check_directory()
    create_directories(source_directory)
    unzip_to_new_directory(source_directory, unzipping_directory)
    scale(unzipping_directory, pickup_directory)
    zip_folder(pickup_directory)
    remove_leftover_files()
    print('Complete')
