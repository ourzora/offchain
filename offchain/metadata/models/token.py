from offchain.base.base_model import BaseModel


class Token(BaseModel):
    chain_identifier: str
    collection_address: str
    token_id: int
    uri: str
