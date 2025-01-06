import aiofiles
import os
from datetime import datetime

from g import\
 OUTPUT_FOLDER_PATH,\
 DB_FOLDER_PATH,\
 IMAGE_FOLDER_PATH,\
 JSON_FOLDER_PATH,\
 LOG_FOLDER_PATH


class FileManagement:

    # SINGLETON Begin

    __instance = None

    @staticmethod
    def get_instance():
        if FileManagement.__instance is None:
            FileManagement()
        return FileManagement.__instance

    def __init__(self):
        if FileManagement.__instance is not None:
            raise Exception(
              'This class is a singleton, \
use FileManagement.get_instance() instead!'
            )
        else:
            self.__init()
            FileManagement.__instance = self

    # SINGLETON End

    # PROTECTED Begin

    def __init(self):
        if not os.path.isdir(OUTPUT_FOLDER_PATH):
            raise Exception(
              "{} not found!".format(OUTPUT_FOLDER_PATH)
            )
        if not os.path.isdir(DB_FOLDER_PATH):
            os.mkdir(DB_FOLDER_PATH)
        if not os.path.isdir(IMAGE_FOLDER_PATH):
            os.mkdir(IMAGE_FOLDER_PATH)
        if not os.path.isdir(JSON_FOLDER_PATH):
            os.mkdir(JSON_FOLDER_PATH)
        if not os.path.isdir(LOG_FOLDER_PATH):
            os.mkdir(LOG_FOLDER_PATH)

    def __get_out_folderpath_by_prefix(self,
                                       folderpath: str,
                                       prefix: str) -> str:
        if prefix is None:
            return folderpath
        prefix_list = prefix.split('/')
        new_folderpath = folderpath
        for n in range(0, len(prefix_list)):
            new_folderpath = "{0}/{1}".format(
              new_folderpath,
              prefix_list[n])
            if not os.path.isdir(new_folderpath):
                os.mkdir(new_folderpath)
        return new_folderpath

    # PROTECTED End

    # PRIVATE Begin

    def _get_json_out_folderpath_by_prefix(self,
                                           prefix: str) -> str:
        return self.__get_out_folderpath_by_prefix(
          folderpath=JSON_FOLDER_PATH,
          prefix=prefix)

    def _get_image_out_folderpath_by_prefix(self,
                                            prefix: str) -> str:
        return self.__get_out_folderpath_by_prefix(
          folderpath=IMAGE_FOLDER_PATH,
          prefix=prefix)

    async def _write_to_file(self,
                             folderpath: str,
                             filename: str,
                             content: str):
        async with aiofiles.open(
          "{0}/{1}".format(
            folderpath,
            filename), mode='w'
        ) as file_object:
            await file_object.write(content)

    async def _write_to_log(self,
                            label: str,
                            message: str):
        async with aiofiles.open(
          "{0}/{1}.log".format(
            LOG_FOLDER_PATH,
            label), mode='a'
        ) as file_object:
            await file_object.write(
              "{0} - {1}{2}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                message,
                os.linesep)
            )

    # PRIVATE End
