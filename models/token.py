from metazerse.models.base_model import BaseModel


class Token(BaseModel):
    collection_address: str
    token_id: int
    uri: str
