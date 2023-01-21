# raw data files downloaded from http://millionsongdataset.com/musixmatch/

from typing import List
import csv
from dao.dao_sentiment_metadata import DAOSentimentMetadata
from models.mxm_label import MxmLabel
from models.sentiment_metadata import SentimentMetadata

if __name__ == '__main__':
    dao_sentiment_metadata: DAOSentimentMetadata = DAOSentimentMetadata()

    with open(
            ".\correctedMetadata.csv",
            'r', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter=",", quotechar="\"")
        next(lines, None)
        for line in lines:
            sentiment_id = line[0]
            wikipedia_language_code = line[1]
            language_name_eng = line[2]
            language_name_native = line[3]
            last_updated = line[4]
            dao_sentiment_metadata.insert_one(SentimentMetadata(sentiment_id=sentiment_id, wikipedia_language_code=wikipedia_language_code, language_name_eng=language_name_eng, language_name_native=language_name_native, last_updated=last_updated))


