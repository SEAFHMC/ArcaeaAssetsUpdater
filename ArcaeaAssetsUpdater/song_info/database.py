from _RHelper import RHelper
import peewee as pw
from song_info.schema import SongList
import ujson as json

root = RHelper()


class Data:
    db = pw.SqliteDatabase(root.data("arcsong.db"))
    with open(root.data("arcsong.json"), "r", encoding="UTF-8") as f:
        jsons = json.loads(f.read())
    song_list = SongList(**jsons["content"])


class alias(pw.Model):
    sid = pw.IntegerField()
    alias = pw.CharField()

    class Meta:
        database = Data.db
        primary_key = pw.CompositeKey("sid", "alias")


class charts(pw.Model):
    song_id = pw.CharField()
    rating = pw.IntegerField()
    rating_class = pw.IntegerField()
    name_en = pw.CharField()
    name_jp = pw.CharField()

    class Meta:
        database = Data.db
        primary_key = pw.CompositeKey(
            "song_id", "rating", "rating_class", "name_en", "name_jp"
        )
