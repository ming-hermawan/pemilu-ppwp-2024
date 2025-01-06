import json

from module.http_request.base import HttpRequestBase
from module.file_management import FileManagement
from g import DOMAIN, JSON_FOLDER_PATH


class Ppwp(HttpRequestBase):

    # CONSTANT Begin

    __LABEL = 'ppwp'
    __URL = "{}/pemilu/ppwp.json".format(
        DOMAIN)

    # CONSTANT End

    # Constructor
    def __init__(self,
                 is_save_json_files: bool,
                 is_debug: bool):
        super().__init__(
          label=self.__LABEL,
          is_debug=is_debug)
        self.__is_save_json_files = is_save_json_files

    # PRIVATE Begin

    async def _get_ppwps(self) -> dict:
        session = await self._get_session()
        ppwps = await self._get_json(
          session=session,
          url=self.__URL)
        if self.__is_save_json_files:
            file_management = FileManagement.get_instance()
            await file_management._write_to_file(
              folderpath=JSON_FOLDER_PATH,
              filename='ppwp.json',
              content=json.dumps(ppwps))
        await session.close()
        return ppwps

    # PRIVATE End
