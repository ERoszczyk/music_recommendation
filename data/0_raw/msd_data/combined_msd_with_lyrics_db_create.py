from typing import List

from music_recommendation.dao.dao_FMS_Lyrics import DAOFMSLyrics
from music_recommendation.dao.dao_msd_songs import DAOMsdSongs
from music_recommendation.dao.dao_msd_songs_with_lyrics import DAOMsdSongsWithLyrics
from music_recommendation.models.fms_lyrics import FMSLyrics
from music_recommendation.models.msd_song import MsdSong, MsdSongWithLyrics

if __name__ == "__main__":
    # dao_lyrics = DAOFMSLyrics()
    # dao_lyrics.collection.create_index([("title", 1), ("artist", 1)])
    dao_songs: DAOMsdSongs = DAOMsdSongs()
    dao_lyrics: DAOFMSLyrics = DAOFMSLyrics()
    dao_songs_with_lyrics: DAOMsdSongsWithLyrics = DAOMsdSongsWithLyrics()

    # Get all songs
    songs: List[MsdSong] = dao_songs.find_all()
    count= 0
    last_progress = 0
    for song in songs:
        if int(count*1000 / len(songs))>last_progress:
            last_progress = int(count*1000 / len(songs))
            print(f"{last_progress/10}%")
        # Get lyrics for each song
        try:
            fms_lyrics: FMSLyrics = dao_lyrics.find_one_by_query(
                {"title": song.title, "artist": song.artist_name})
            lyrics = fms_lyrics.lyrics
            tag = fms_lyrics.tag
            features = fms_lyrics.features

        except:
            lyrics = None
            tag = None
            features = None

        song_with_lyrics: MsdSongWithLyrics = MsdSongWithLyrics(
            song_id=song.song_id,
            title=song.title,
            release=song.release,
            artist_name=song.artist_name,
            year=song.year,
            tag=tag,
            features=features,
            lyrics=lyrics
        )
        dao_songs_with_lyrics.insert_one(song_with_lyrics)
