import asyncio
import re

from module.http_request.base import HttpRequestBase
from module.file_management import FileManagement


class Image(HttpRequestBase):

    # CONSTANT Begin

    __LABEL = 'image'
    __FILE_NAME_REGEX = r"^https\x3A\x2F\x2Fsirekap\x2Dobj\x2Dformc\x"\
        r"2Ekpu\x2Ego\x2Eid\x2F\w\w\w\w\x2Fpemilu\x2Fppwp\x2F\d\d\x2F"\
        r"\d\d\x2F\d\d\x2F\d\d\x2F\d\d\x2F(\d\d\d\d\d\d\d\d\d\d\d\d\d"\
        r"\x2D\d\d\d\d\d\d\d\d\x2D\d\d\d\d\d\d\x2D\x2D\w\w\w\w\w\w\w"\
        r"\w\x2D\w\w\w\w\x2D\w\w\w\w\x2D\w\w\w\w\x2D\w\w\w\w\w\w\w\w"\
        r"\w\w\w\w\x2Ejpg)$"
    __MAX_DOWNLOAD_PER_PROCESS = 50

    # CONSTANT End

    # Constructor
    def __init__(self,
                 is_debug: bool):
        super().__init__(
          label=self.__LABEL,
          is_debug=is_debug)
        self.__is_save_json_files = False

    # PRIVATE Begin

    async def _download_images(self, hhcw_ppwps) -> dict:
        session = await self._get_session()
        process = []
        for x in hhcw_ppwps:
            hhcw_code = x['code']
            prefix = x['prefix']
            new_prefix = "{0}/{1}".format(prefix, hhcw_code)
            file_management = FileManagement.get_instance()
            folderpath = \
                file_management._get_image_out_folderpath_by_prefix(
                  prefix=new_prefix)
            if ('images' in x.keys()) and (x['images'] is not None):
                filtered_images = list(
                  filter(
                    lambda x2: x2 is not None, x['images']
                  )
                )
                for n in range(0, len(filtered_images)):
                    url = filtered_images[n]
                    try:
                        filename = re.findall(
                          self.__FILE_NAME_REGEX,
                          url)[0]
                    except IndexError:
                        await self._log(
                          message="Skip '{}', Pattern Unknown".format(
                            url))
                        continue
                    filepath = "{0}/{1}".format(
                      folderpath,
                      filename)
                    process.append(
                      self._download_file(
                        session=session,
                        url=url,
                        filepath=filepath)
                    )
                    if len(process) == self.__MAX_DOWNLOAD_PER_PROCESS:
                        await asyncio.gather(*process)
                        process = []
        if len(process) > 0:
            await asyncio.gather(*process)
        await session.close()

    # PRIVATE End
