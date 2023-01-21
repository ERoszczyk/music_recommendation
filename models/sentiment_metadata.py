from pydantic import BaseModel


class SentimentMetadata(BaseModel):
    sentiment_id: int
    wikipedia_language_code: str
    language_name_eng: str
    language_name_native: str
    last_updated: str
