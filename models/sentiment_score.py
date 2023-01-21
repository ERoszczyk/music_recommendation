from pydantic import BaseModel


class SentimentScore(BaseModel):
    word: str
    sentiment_score: int  # -1 negative, 1 positive
