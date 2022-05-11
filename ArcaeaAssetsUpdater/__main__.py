from route import app
from scheduler_job import scheduler
import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

# from _RHelper import RHelper

# root = RHelper()
config = Config()
config.bind = ["localhost:17777"]
# config.certfile = ""
# config.keyfile = ""


@app.on_event("startup")
async def _():
    scheduler.start()


if __name__ == "__main__":
    asyncio.run(serve(app, config))
