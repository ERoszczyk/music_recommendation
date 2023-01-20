# raw data files downloaded from http://millionsongdataset.com/musixmatch/

from typing import List

from dao.dao_msd_triplets import DAOMsdTriplets
from models.msd_triplet import MsdTriplet

if __name__ == '__main__':
    dao_songs: DAOMsdTriplets = DAOMsdTriplets()

    with open(
            ".\\triplets_file.csv",
            'r', encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            split_line: List[str] = line.split(',')
            user_id: str = split_line[0]
            song_id: str = split_line[1]
            listen_count: int = int(split_line[2])
            dao_songs.insert_one(MsdTriplet(user_id=user_id, song_id=song_id, listen_count=listen_count))
