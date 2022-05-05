"""
 - Author: DiheChen
 - Date: 2021-08-14 23:42:42
 - LastEditTime: 2021-08-21 00:04:28
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from os import path
from sys import platform
from zipfile import ZipFile
import ujson as json
from aiohttp import ClientSession
from aiofile import async_open
from config import Config

if platform == "win32":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class ArcaeaAssetsUpdater:
    work_path = path.abspath(path.join(path.dirname(__file__), "data"))
    version_info = path.join(work_path, "version.json")

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_local_version_info():
        with open(ArcaeaAssetsUpdater.version_info, "r") as file:
            return json.loads(file.read())["value"]["version"]

    @staticmethod
    def mark_version_info(data: dict):
        with open(ArcaeaAssetsUpdater.version_info, "w") as f:
            f.write(json.dumps(data, indent=4))
        return None

    @staticmethod
    async def download_file(force_download: bool = False):
        async with ClientSession() as session:
            async with session.get(
                "https://webapi.lowiro.com/webapi/serve/static/bin/arcaea/apk",
                proxy=Config.proxy,
                verify_ssl=False,
            ) as resp:
                if resp.ok:
                    j = await resp.json()
                    if (
                        not force_download
                        and j["value"]["version"]
                        == ArcaeaAssetsUpdater.get_local_version_info()
                    ):
                        return False
                    ArcaeaAssetsUpdater.mark_version_info(j)
                    async with session.get(
                        j["value"]["url"],
                        proxy=Config.proxy,
                        verify_ssl=False,
                        timeout=None,
                    ) as resp:
                        async with async_open(
                            path.join(
                                ArcaeaAssetsUpdater.work_path,
                                f"arcaea_{j['value']['version']}.apk",
                            ),
                            "wb",
                        ) as res:
                            while True:
                                chunk = await resp.content.read(1024 * 1024 * 8)
                                if chunk:
                                    await res.write(chunk)
                                else:
                                    break
                        return True

    @staticmethod
    async def unzip_file():
        zip_file = ZipFile(
            path.join(
                ArcaeaAssetsUpdater.work_path,
                f"arcaea_{ArcaeaAssetsUpdater.get_local_version_info()}.apk",
            )
        )
        file_list = zip_file.namelist()
        for f in file_list:
            if f.startswith("assets"):
                zip_file.extract(f, ArcaeaAssetsUpdater.work_path)
        return True

    @staticmethod
    async def force_update():
        if await ArcaeaAssetsUpdater.download_file(force_download=True):
            await ArcaeaAssetsUpdater.unzip_file()
