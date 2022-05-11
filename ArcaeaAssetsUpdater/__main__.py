"""
 - Author: DiheChen
 - Date: 2021-08-11 23:14:50
 - LastEditTime: 2021-08-15 04:52:49
 - LastEditors: DiheChen
 - Description: None
 - GitHub: https://github.com/Chendihe4975
"""
from route import app
from scheduler_job import scheduler


@app.on_event("startup")
async def _():
    scheduler.start()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=17777)
