import aiofiles
import asyncio
import aiohttp

from module.file_management import FileManagement


class HttpRequestBase:

    # Constructor
    def __init__(self,
                 label: str,
                 is_debug: bool):
        self.__label = label
        self.__is_debug = is_debug

    # PRIVATE Begin

    async def _log(self,
                   message: str):
        if self.__is_debug:
            file_management = FileManagement.get_instance()
            await file_management._write_to_log(
              label=self.__label,
              message=message)

    async def _get_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

    async def _get_json(self,
                        session: aiohttp.ClientSession,
                        url: str):
        out = None
        is_request = True
        retry = 1
        while is_request:
            await self._log(
              "Connect '{}', to get JSON".format(url))
            try:
                async with session.get(url) as response:
                    status_code = response.status
                    await self._log(
                      "Connect '{0}', Status-Code={1}".format(
                        url,
                        status_code))
                    if status_code == 200:
                        out = await response.json()
                        is_request = False
                    elif (status_code in [500, 503]) and (retry < 3):
                        retry += 1
                    else:
                        raise Exception(
                          "Connect {0}, Status-Code={1}".format(
                            url,
                            status_code)
                        )
            except asyncio.TimeoutError:
                await self._log(
                  "Connect '{}', Time-Out".format(url))
                await asyncio.sleep(5)
                continue
        return out

    async def _download_file(self,
                             session: aiohttp.ClientSession,
                             url: str,
                             filepath: str):
        await self._log(
          message="Download from '{0}' to {1}".format(
            url,
            filepath))
        async with session.get(url) as response:
            status_code = response.status
            await self._log(
              message="Download '{0}', Status-Code={1}".format(
                url,
                status_code))
            if status_code == 200:
                async with aiofiles.open(
                  filepath, mode='wb'
                ) as file_object:
                    data = await response.read()
                    await file_object.write(data)

    # PRIVATE End
