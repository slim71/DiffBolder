import os
import sys
import re
from datetime import datetime
from typing import Union
from Logger import get_logger
from utils import logged_input
from constants import DESIRED_EXTENSIONS
from DocxFile import DocxFile
from FdxFile import FdxFile


class DiffBolder:
    full_filename: str
    file_extension: str
    file_name: str
    older_file_name: str
    file_path: str
    file_handler: Union[DocxFile, FdxFile, None]

    def __init__(self):
        self.logger = get_logger(str(self.__class__))
        self.full_filename = None
        self.file_extension = None
        self.file_name = None
        self.older_file_name = None
        self.file_path = None
        self.file_handler = None

    def ask_file(self):
        # TODO: check if file provided in the path?
        self.file_path = os.path.abspath(logged_input("Insert path to the file: "))
        provided_filename = logged_input("Insert name of the file: ")

        # Check for the extension
        try:
            # Try to split name and extension
            self.file_name, self.file_extension = provided_filename.split(".")
            self.full_filename = provided_filename
        except ValueError:
            # Only name provided
            self.logger.warning(
                "No extension provided. I'll try to see if it's a .docx or a .fdx"
            )
            self.full_filename = self.find_file(provided_filename)
            self.file_name, self.file_extension = self.full_filename.split(".")
            self.logger.info("File found!")

        if not os.path.exists(self.file_path) or not os.path.exists(
            os.path.join(self.file_path, self.full_filename)
        ):
            self.logger.error("File or path not found!")
            sys.exit()

        if self.file_extension == "docx":
            self.file_handler = DocxFile(self.file_path, self.file_name)
        else:
            self.file_handler = FdxFile(self.file_path, self.file_name)

    def find_file(self, filename):
        for obj in os.listdir(self.file_path):
            if os.path.isfile(os.path.join(self.file_path, obj)) and re.search(fr"{filename}\.\w+", obj):
                obj_extension = obj.split(".")[1]  # TODO: what if more dots are used?
                if obj_extension in DESIRED_EXTENSIONS:
                    return obj

        self.logger.error("Could not detect file extension!")
        sys.exit()

    def find_older_reference(self):
        list_of_files = os.listdir(self.file_path)

        files_with_date = []
        for obj in list_of_files:
            if os.path.isfile(os.path.join(self.file_path,obj)) and self.file_name in obj:
                files_with_date.append(obj.split(".")[0])  # TODO: what if more dots are used?

        if len(files_with_date) == 0:
            self.logger.warning(
                "No previous version of the file has been found! The provided one will be set as reference"
            )
            self.file_handler.create_new_reference()
            sys.exit()

        dates = []
        for file in files_with_date:
            try:
                dates.append(datetime.strptime("-".join(file.split("-")[1:]).strip(), "%d-%m-%y"))
            except ValueError:
                # To keep the indexing constant
                dates.append(datetime.today())

        most_recent = max(dt for dt in dates if dt < datetime.now())

        self.logger.info(
            "Most recent reference file found is from %s",
            most_recent.strftime("%d-%m-%y"),
        )
        self.older_file_name = files_with_date[dates.index(most_recent)]
        self.logger.debug("Related filename: %s", self.older_file_name)

    def run(self):
        self.ask_file()
        self.find_older_reference()
        self.file_handler.run(".".join([self.older_file_name, self.file_extension]))
