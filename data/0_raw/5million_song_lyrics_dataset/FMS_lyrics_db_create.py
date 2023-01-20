# raw data files downloaded from https://www.kaggle.com/datasets/nikhilnayak123/5-million-song-lyrics-dataset
import sys
import csv

from typing import List

from dao.dao_FMS_Lyrics import DAOFMSLyrics
from models.fms_lyrics import FMSLyrics
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def is_info_line(line: str) -> bool:
    split_line: List[str] = line.replace(', ',"").replace(' ,',"").replace(',""',"").replace('"",',"").split(',')
    if len(line) > 200:
        return False

    if not len(split_line) == 7 and not len(split_line) == 8:
        return False
    if len(split_line) == 8:
        try:
            int(split_line[-1])
        except ValueError:
            return False
    try:
        if int(split_line[3]) < 1500 and int(split_line[3]) != 0:
            return False
        int(split_line[4])
        try:
            int(split_line[0])
            return False
        except ValueError:
            try:
                int(split_line[1])
                return False
            except ValueError:
                try:
                    int(split_line[2])
                    return False
                except ValueError:
                    try:
                        int(split_line[5])
                        return False
                    except ValueError:
                        return True
                    except IndexError:
                        return False
    except ValueError:
        return False
    except IndexError:
        return False


if __name__ == '__main__':
    dao_lyrics: DAOFMSLyrics = DAOFMSLyrics()

    with open(
                    ".\ds2.csv",
                    'r', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter=",", quotechar="\"")
        first_line = True
        for line in lines:
            if first_line:
                first_line = False
                continue
            features = ",".join(line[5:-2]). \
                                 replace('","', ';').replace('"', ''). \
                                 replace('{', '').replace('}', '').split(';')
            fms_lyrics = FMSLyrics(
                                title=line[0],
                                tag=line[1],
                                artist=line[2],
                                year=int(line[3]),
                                views=int(line[4]),
                                features=features,
                                lyrics=line[6],
                                song_id=int(line[7])
                            )
            dao_lyrics.insert_one(fms_lyrics)

    # with open(
    #         ".\ds2.csv",
    #         'r', encoding='utf-8') as f:
    #     info_line = ""
    #     lyrics_lines = []
    #     no_previous_song = True
    #     lines = f.readlines()[1:]
    #     counter = 0
    #     for line in lines:
    #         counter+=1
    #         if is_info_line(line):
    #             if no_previous_song:
    #                 no_previous_song = False
    #             else:
    #                 lyrics = ("".join(lyrics_lines[:-1])) + (",".join(lyrics_lines[-1].split('",')[:-1]))
    #                 info_line_split: List[str] = info_line.split(',')
    #                 features = ",".join(info_line_split[5:-1]). \
    #                     replace('","', ';').replace('"', ''). \
    #                     replace('{', '').replace('}', '').split(';')
    #
    #                 try:
    #                     song_id = int(lyrics_lines[-1].split(',')[-1])
    #                 except ValueError as e:
    #                     print(counter)
    #                     raise e
    #                 fms_lyrics = FMSLyrics(
    #                     title=info_line_split[0],
    #                     tag=info_line_split[1],
    #                     artist=info_line_split[2],
    #                     year=int(info_line_split[3]),
    #                     views=int(info_line_split[4]),
    #                     features=features,
    #                     lyrics=lyrics,
    #                     song_id=song_id
    #                 )
    #                 dao_lyrics.insert_one(fms_lyrics)
    #                 lyrics_lines = []
    #             if line.split(',')[-2] == '[Instrumental]':
    #                 info_line_split: List[str] = line.split(',')
    #                 features = ",".join(info_line_split[5:-2]). \
    #                     replace('","', ';').replace('"', ''). \
    #                     replace('{', '').replace('}', '').split(';')
    #                 song_id = info_line_split[-1]
    #                 fms_lyrics = FMSLyrics(
    #                     title=info_line_split[0],
    #                     tag=info_line_split[1],
    #                     artist=info_line_split[2],
    #                     year=int(info_line_split[3]),
    #                     views=int(info_line_split[4]),
    #                     features=features,
    #                     lyrics='[Instrumental]',
    #                     song_id=int(song_id)
    #                 )
    #                 dao_lyrics.insert_one(fms_lyrics)
    #                 no_previous_song = True
    #             else:
    #                 info_line = line
    #                 lyrics_lines.append(info_line.split(',"')[-1])
    #         else:
    #             lyrics_lines.append(line)
