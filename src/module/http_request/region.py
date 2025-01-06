import aiohttp
import asyncio
import json
from string import Template

from module.http_request.base import HttpRequestBase
from module.http_request.hhcw_ppwp import HhcwPpwp
from module.file_management import FileManagement
from g import DOMAIN


class Region(HttpRequestBase):

    # CONSTANT Begin

    __LABEL = 'region'
    __URL = Template(
      "{}/wilayah/pemilu/ppwp/$end.json".format(
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
        self.__hhcw_ppwp = HhcwPpwp(
          is_save_json_files=is_save_json_files,
          is_debug=is_debug)

    # PROTECTED Begin

    async def __get_response(self,
                             session,
                             code: str,
                             prefix: str) -> list:
        end_url = \
            "{0}/{1}".format(prefix, code) if \
            (prefix is not None) and (prefix != '0') \
            else code
        url = self.__URL.substitute(
          {'end': end_url}
        )
        regions = await self._get_json(
          session=session,
          url=url)
        for region in regions:
            region['prefix'] = end_url
        if self.__is_save_json_files:
            file_management = FileManagement.get_instance()
            folderpath = \
                file_management._get_json_out_folderpath_by_prefix(
                  prefix=prefix)
            filename = "{}.json".format(code)
            content = json.dumps(regions)
            await file_management._write_to_file(
              folderpath=folderpath,
              filename=filename,
              content=content)
        return regions

    async def __get_regions_and_hhcw_ppwps(
      self,
      session: aiohttp.ClientSession,
      temp_regions: list,
      lv: int) -> tuple:
        process = []
        for region in temp_regions:
            code = region['kode']
            prefix = \
                region['prefix'] if \
                'prefix' in region.keys() \
                else None
            process.append(
              self.__get_response(
                session=session,
                code=code,
                prefix=prefix)
            )
        responses = await asyncio.gather(*process)
        regions = []
        process = []
        for response in responses:
            if lv == 4:
                for region in response:
                    code = region['kode']
                    process.append(
                      self.__hhcw_ppwp._get_hhcw_ppwps(
                        session=session,
                        code=code,
                        prefix=region['prefix'])
                    )
            regions.extend(response)
        if lv == 4:
            hhcw_ppwps = await asyncio.gather(*process)
        else:
            hhcw_ppwps = None
        return regions, hhcw_ppwps

    # PROTECTED End

    # PRIVATE Begin

    async def _get_regions_and_hhcw_ppwps(self) -> tuple:
        regions = []
        hhcw_ppwps = []
        session = await self._get_session()
        temp_regions = await self.__get_response(
          session=session,
          code='0',
          prefix=None)
        regions.extend(temp_regions)
        for lv in range(1, 5):
            temp_regions, temp_hhcw_ppwps = \
              await self.__get_regions_and_hhcw_ppwps(
                session=session,
                temp_regions=temp_regions,
                lv=lv)
            regions.extend(temp_regions)
            if temp_hhcw_ppwps is not None:
                hhcw_ppwps.extend(temp_hhcw_ppwps)
        await session.close()
        return (regions, hhcw_ppwps)

    # PRIVATE End
