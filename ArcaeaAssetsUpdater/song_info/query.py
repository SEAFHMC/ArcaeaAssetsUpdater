from .database import alias, charts, Data


class SongAlias:
    def song_alias(song: str):
        song_alias = alias.select().where((alias.sid == song) | (alias.alias == song))
        res = [i for i in song_alias]
        if res:
            song_alias = alias.select().where(alias.sid == res[0].sid)
            return {
                "status": 0,
                "content": {
                    "song_id": res[0].sid,
                    "alias": [i.alias for i in song_alias],
                },
            }
        else:
            return {"status": 0, "message": "invalid songname or songid"}


class SongRandom:
    def song_random(start: float, end: float, difficulty: int = -1):
        if difficulty != -1:
            result = charts.select().where(
                (charts.rating >= start * 10)
                & (end * 10 >= charts.rating)
                & (charts.rating_class == difficulty)
            )
        elif difficulty == -1:
            result = charts.select().where(
                (charts.rating >= start * 10) & (end * 10 >= charts.rating)
            )
        return [SongRandom.make_json(i) for i in result]

    def get_song_info(song_id: str, difficulty: int):
        song_list = Data.song_list
        for i in song_list.songs:
            if i.song_id == song_id:
                return i.difficulties[difficulty].dict()

    def make_json(data: charts):
        song_id = data.song_id
        difficulty = data.rating_class
        song_info = SongRandom.get_song_info(song_id, difficulty)
        jsons = {
            "song_id": song_id,
            "difficulty": difficulty,
            "song_info": song_info,
        }
        return jsons
