import aiohttp
import json
from string import Template

from module.http_request.base import HttpRequestBase
from module.file_management import FileManagement
from g import DOMAIN


class HhcwPpwp(HttpRequestBase):

    # CONSTANT Begin

    __LABEL = 'hhcw'
    __URL = Template(
      "{}/pemilu/hhcw/ppwp/$end.json".format(
        DOMAIN)
    )

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

    async def _get_hhcw_ppwps(self,
                              session: aiohttp.ClientSession,
                              code: str,
                              prefix: str) -> dict:
        end_url = "{0}/{1}".format(
          prefix,
          code)
        url = self.__URL.substitute(
          {'end': end_url})
        hhcw_ppwps = await self._get_json(
          session=session,
          url=url)
        hhcw_ppwps.update(
          {
            'code': code,
            'prefix': prefix}
        )
        if self.__is_save_json_files:
            file_management = FileManagement.get_instance()
            folderpath = \
                file_management._get_json_out_folderpath_by_prefix(
                  prefix=prefix)
            filename = "{}.json".format(code)
            content = json.dumps(hhcw_ppwps)
            await file_management._write_to_file(
              folderpath=folderpath,
              filename=filename,
              content=content)
        return hhcw_ppwps

    # PRIVATE End
