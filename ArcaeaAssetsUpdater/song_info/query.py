from .database import alias, charts, Data
from random import choice


def get_song_info(song_id: str, difficulty: int = -1):
    song_list = Data.song_list
    try:
        for i in song_list.songs:
            if i.song_id == song_id:
                if difficulty == -1:
                    return [v.dict() for v in i.difficulties]
                return i.difficulties[difficulty].dict()
    except IndexError:
        return None


class SongAlias:
    def song_alias(songname: str):
        song_alias = alias.select().where(
            (alias.sid == songname) | (alias.alias == songname)
        )
        if res := list(song_alias):
            song_alias = alias.select().where(alias.sid == res[0].sid)
            return {
                "status": 0,
                "content": {
                    "song_id": res[0].sid,
                    "alias": [i.alias for i in song_alias],
                },
            }
        elif song_alias := charts.get_or_none((charts.name_en == songname)|(charts.name_jp == songname)):
            song_id = song_alias.song_id,
            return {
                "status": 0,
                "content": {
                    "song_id": song_id,
                    "alias": list(alias.select().where(alias.sid == song_id)),
                },
            }
        return {"status": -5, "message": "invalid songname or songid"}


class SongRandom:
    def make_json(data: charts):
        song_id = data.song_id
        difficulty = data.rating_class
        song_info = get_song_info(song_id, difficulty)
        jsons = {
            "song_id": song_id,
            "difficulty": difficulty,
            "song_info": song_info,
        }
        return jsons

    def song_random(start: float, end: float, difficulty: int = -1):
        if difficulty not in (-1, 0, 1, 2, 3):
            return {"status": -9, "message": "invalid difficulty"}
        if difficulty != -1 and difficulty:
            result = charts.select().where(
                (charts.rating >= start * 10)
                & (end * 10 >= charts.rating)
                & (charts.rating_class == difficulty)
            )
        elif difficulty == -1:
            result = charts.select().where(
                (charts.rating >= start * 10) & (end * 10 >= charts.rating)
            )
        return {
            "status": 0,
            "content": choice([SongRandom.make_json(i) for i in result]),
        }


class SongInfo:
    def song_info(songname: str, difficulty: int = -1):
        song_alias = SongAlias.song_alias(songname)
        if song_alias["status"] != 0:
            return {"status": -5, "message": "invalid songname or songid"}
        song_id = song_alias["content"]["song_id"]
        if song_info := get_song_info(song_id=song_id, difficulty=difficulty):
            return {
                "status": 0,
                "content": {"song_id": song_id, "song_info": song_info},
            }
        else:
            return {"status": -9, "message": "invalid difficulty"}
