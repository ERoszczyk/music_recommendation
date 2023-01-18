# raw data files downloaded from http://millionsongdataset.com/musixmatch/

from typing import List

from music_recommendation.dao.dao_msd_songs import DAOMsdSongs
from music_recommendation.models.msd_song import MsdSong

if __name__ == '__main__':
    dao_songs: DAOMsdSongs = DAOMsdSongs()

    with open(
            ".\song_data.csv",
            'r', encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            split_line: List[str] = line.split(',')
            song_id: str = split_line[0]
            title: str = split_line[1]
            release: str = split_line[2]
            artist_name: str = split_line[3]
            year: int = int(split_line[4])
            dao_songs.insert_one(MsdSong(song_id=song_id, title=title, release=release, artist_name=artist_name, year=year))
