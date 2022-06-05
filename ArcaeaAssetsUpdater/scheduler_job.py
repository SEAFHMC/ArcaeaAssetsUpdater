"""
 - Author: DiheChen
 - Date: 2021-08-14 23:46:20
 - LastEditTime: 2021-08-15 04:52:14
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from assets_updater import ArcaeaAssetsUpdater

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")


@scheduler.scheduled_job("cron", hour=8, minute=15)
async def _():
    if await ArcaeaAssetsUpdater.download_file():
        await ArcaeaAssetsUpdater.unzip_file()
