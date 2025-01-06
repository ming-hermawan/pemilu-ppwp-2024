import re

from g import CMD_DB_SQLITE


class CmdInputException(Exception):
    pass


class CmdInput:

    # CONSTANT Begin

    __DEBUG_REGEX = r"--debug=(YES|NO)"
    __SAVE_JSON_FILES_REGEX = r"--save-json-files=(YES|NO)"
    __SAVE_IMAGE_FILES_REGEX = r"--save-image-files=(YES|NO)"
    __SAVE_DB_REGEX = r"--db=(NO|{})".format(CMD_DB_SQLITE)
    __SAVE_DB_FILENAME_REGEX = r"--db-filename=(\w*)"
    __DEFAULT_DB_FILENAME = 'pemilu-ppwp-2024.db'

    # CONSTANT End

    # Constructor
    def __init__(self,
                 argv: list):
        # Initialization
        argv_len = len(argv)
        # No Parameter
        if argv_len < 5:
            raise CmdInputException(
              '''ERROR Parameters
Usage: python main.py --save-json-files=(YES|NO) --save-image-files=(Y\
ES|NO) --db=(NO|sqlite) --debug=(YES|NO) --db-filename=[SQLite filename]
Get Indonesia 2024 election data.

--save-json-file      Save gathered data to JSON files.
--save-image-files    Get & save images.
--db                  Save gathered data to database. (Only support SQ\
Lite now)
--db-filename         SQlite filename. (Optional)
''')
        # --debug Parameter
        find_results = re.findall(
          self.__DEBUG_REGEX,
          argv[4])
        if len(find_results) > 0:
            if find_results[0] == 'YES':
                self.__is_debug = True
            elif find_results[0] == 'NO':
                self.__is_debug = False
            else:
                raise CmdInputException(
                  'Unknown --debug parameter!'
                )

        # --save-json-files Parameter
        find_results = re.findall(
          self.__SAVE_JSON_FILES_REGEX,
          argv[1])
        if len(find_results) > 0:
            if find_results[0] == 'YES':
                self.__is_save_json_files = True
            elif find_results[0] == 'NO':
                self.__is_save_json_files = False
            else:
                raise CmdInputException(
                  'Unknown --save-json-files parameter!'
                )
        else:
            raise CmdInputException(
              'No --save-json-files parameter!'
            )

        # --save-image-files Parameter
        find_results = re.findall(
          self.__SAVE_IMAGE_FILES_REGEX,
          argv[2])
        if len(find_results) > 0:
            if find_results[0] == 'YES':
                self.__is_save_image_files = True
            elif find_results[0] == 'NO':
                self.__is_save_image_files = False
            else:
                raise CmdInputException(
                  'Unknown --save-image-files parameter!'
                )
        else:
            raise CmdInputException(
              'No --save-image-files parameter!'
            )

        # --db Parameter
        find_results = re.findall(
          self.__SAVE_DB_REGEX,
          argv[3])
        if len(find_results) > 0:
            if find_results[0] == CMD_DB_SQLITE:
                self.__db = CMD_DB_SQLITE
            elif find_results[0] == 'NO':
                self.__db = None
            else:
                raise CmdInputException(
                  'Unknown --db parameter!'
                )
        else:
            raise CmdInputException(
              'No --db parameter!'
            )

        # --db-filename Parameter
        self.__db_filename = None
        if self.__db == CMD_DB_SQLITE:
            if argv_len < 6:
                self.__db_filename = self.__DEFAULT_DB_FILENAME
            else:
                find_results = re.findall(
                  self.__SAVE_DB_FILENAME_REGEX,
                  argv[5])
                if len(find_results) > 0:
                    self.__db_filename = find_results[0]

    # PRIVATE Begin

    def _is_debug(self) -> bool:
        return self.__is_debug

    def _is_save_json_files(self) -> bool:
        return self.__is_save_json_files

    def _is_save_image_files(self) -> bool:
        return self.__is_save_image_files

    def _get_db(self) -> str:
        return self.__db

    def _get_db_filename(self) -> str:
        return self.__db_filename

    # PRIVATE End
