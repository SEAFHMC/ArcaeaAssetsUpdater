from typing import List, Optional
from .basemodel import Base
from .song_info import SongInfo


class Song(Base):
    song_id: str
    difficulties: List[SongInfo]
    alias: Optional[List[str]]


class SongList(Base):
    songs: List[Song]
