from os import listdir, path
from urllib.parse import urljoin
from urllib.request import pathname2url
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
import ujson as json
from config import Config
from assets_updater import ArcaeaAssetsUpdater
from song_info.query import SongRandom, SongAlias, SongInfo
from exception import AUAException

app = FastAPI()
songs_dir = path.abspath(path.join(path.dirname(__file__), "data", "assets", "songs"))
char_dir = path.abspath(path.join(path.dirname(__file__), "data", "assets", "char"))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return FileResponse(
        path.abspath(path.join(path.dirname(__file__), "song_info", "index.html")),
        status_code=404,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=403,
        content=jsonable_encoder({"status": 403, "content": "invalid request"}),
    )


@app.exception_handler(RuntimeError)
async def fastapi_exception_handler(request: Request, exc: RuntimeError):
    return JSONResponse(
        status_code=404,
        content=jsonable_encoder(
            {"status": 404, "content": "There is nothing here, go back!"}
        ),
    )


@app.exception_handler(AUAException)
async def fastapi_exception_handler(request: Request, exc: AUAException):
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"status": exc.status, "content": exc.message}),
    )


@app.get("/favicon.ico")
async def _():
    return FileResponse(
        path.abspath(path.join(path.dirname(__file__), "data", "icon.ico"))
    )


@app.get("/assets/songs/{song_id}/{file_name}")
async def _(song_id: str, file_name: str):
    if not path.exists(path.join(songs_dir, song_id)) and (
        "dl_" + song_id in listdir(songs_dir)
    ):
        song_id = "".join(["dl_", song_id])
    return FileResponse(path.join(songs_dir, song_id, file_name))


@app.get("/api/version")
async def _(request: Request):
    with open(path.join(path.dirname(__file__), "data", "version.json"), "r") as file:
        return json.loads(file.read())


@app.get("/api/slst")
async def _(request: Request):
    return FileResponse(path.join(songs_dir, "songlist"))


@app.get("/api/song_list")
async def _(request: Request):
    song_dict = dict()
    for song in listdir(songs_dir):
        if path.isdir(path.join(songs_dir, song)):
            if path.exists(path.join(songs_dir, song, "base.jpg")):
                song_dict[song.replace("dl_", "")] = [
                    urljoin(
                        str(request.base_url),
                        pathname2url(
                            path.join(
                                "assets", "songs", song.replace("dl_", ""), "base.jpg"
                            )
                        ),
                    )
                ]
                if path.exists(path.join(songs_dir, song, "3.jpg")):
                    song_dict[song.replace("dl_", "")].append(
                        urljoin(
                            str(request.base_url),
                            pathname2url(
                                path.join(
                                    "assets", "songs", song.replace("dl_", ""), "3.jpg"
                                )
                            ),
                        )
                    )
    return song_dict


@app.get("/api/char_list")
async def _(request: Request):
    char_list = dict()
    for char in listdir(char_dir):
        char_list[char] = urljoin(
            str(request.base_url), pathname2url(path.join("assets", "char", char))
        )
    return char_list


@app.get("/assets/char/{image_name}")
async def _(image_name: str):
    return FileResponse(path.join(char_dir, image_name))


@app.get("/api/song/random")
async def _(start: float = 0, end: float = 200, difficulty: int = -1):
    return SongRandom.song_random(start, end, difficulty)


@app.get("/api/song/alias")
async def _(songname: str):
    return SongAlias.song_alias(songname)


@app.get("/api/song/info")
async def _(songname: str, difficulty: int = -1):
    return SongInfo.song_info(songname, difficulty)


@app.post("/api/force_update")
async def _(request: Request, background_tasks: BackgroundTasks):
    if (
        "Authorization" in request.headers
        and request.headers["Authorization"] == Config.token
    ):
        background_tasks.add_task(ArcaeaAssetsUpdater.force_update)
        return {"message": "Succeeded."}
    else:
        return {"message": "Access denied."}


@app.post("/api/unzip")
async def _(request: Request, background_tasks: BackgroundTasks):
    if (
        "Authorization" in request.headers
        and request.headers["Authorization"] == Config.token
    ):
        background_tasks.add_task(ArcaeaAssetsUpdater.unzip_file)
        return {"message": "Succeeded."}
    else:
        return {"message": "Access denied."}
