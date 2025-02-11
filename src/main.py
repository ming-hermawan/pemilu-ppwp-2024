import asyncio
import sys
from datetime import datetime

from module.http_request.ppwp import Ppwp
from module.http_request.region import Region
from module.http_request.image import Image
from module.cmd_input import CmdInput, CmdInputException
from module.db.derived.sql.sqlite import DbSqlite
from g import CMD_DB_SQLITE


async def get_ppwps(is_debug: bool,
                    is_save_json_files: bool):
    ppwp = Ppwp(
      is_save_json_files=is_save_json_files,
      is_debug=is_debug)
    return await ppwp._get_ppwps()


async def get_regions_and_hhcw_ppwps(is_debug: bool,
                                     is_save_json_files: bool):
    region = Region(
      is_save_json_files=is_save_json_files,
      is_debug=is_debug)
    return await region._get_regions_and_hhcw_ppwps()


async def process(is_debug: bool,
                  is_save_json_files: bool,
                  is_save_image_files: bool,
                  db: str,
                  db_filename: str):
    ppwps, (regions, hhcw_ppwps) = await asyncio.gather(
      get_ppwps(
        is_debug=is_debug,
        is_save_json_files=is_save_json_files),
      get_regions_and_hhcw_ppwps(
        is_debug=is_debug,
        is_save_json_files=is_save_json_files))
    if db == CMD_DB_SQLITE:
        DbSqlite(db_filename=db_filename).process(
          ppwps=ppwps,
          regions=regions,
          hhcw_ppwps=hhcw_ppwps)
    if is_save_image_files:
        image = Image(is_debug=is_debug)
        await image._download_images(hhcw_ppwps)


def main():
    # 1). Get Input Parameters
    try:
        cmd_input = CmdInput(sys.argv)
    except CmdInputException as e:
        print(e)
        return
    # 2). Process
    time_start = datetime.now().time()
    print("START at {}".format(time_start.strftime("%H:%M:%S")))
    asyncio.run(
      process(
        is_debug=cmd_input._is_debug(),
        is_save_json_files=cmd_input._is_save_json_files(),
        is_save_image_files=cmd_input._is_save_image_files(),
        db=cmd_input._get_db(),
        db_filename=cmd_input._get_db_filename())
    )
    time_end = datetime.now().time()
    print("FINISH at {}".format(time_end.strftime("%H:%M:%S")))


if __name__ == "__main__":
    main()
