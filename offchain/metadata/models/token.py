from pydantic import validator
import re
import json
import base64
from typing import Optional

from offchain.base.base_model import BaseModel


class Token(BaseModel):
    """Token interface with all information required to uniquely identify an NFT.


    Attributes:
        chain_identifier (str): identifier for network and chain of token,
            formatted as NETWORK_NAME-CHAIN_NAME (e.g. "ETHEREUM-MAINNET").
        collection_address (str): collection address of token.
        token_id (int): unique identifier of token.
        uri (str, optional): the uri where the metadata is stored.
    """

    collection_address: str
    token_id: int
    chain_identifier: str = "ETHEREUM-MAINNET"
    uri: Optional[str] = None

    @validator("chain_identifier")
    def validate_chain_identifier(cls, chain_identifier):
        if not re.match("^[A-Z]*-[A-Z]*$", chain_identifier):
            raise ValueError(
                "Expected chain identifier to be formatted as NETWORKNAME-CHAINNAME, e.g. ETHEREUM-MAINNET"
            )

        return chain_identifier

    # There are cases where unicode characters (\xf0\x9f\x99\x82\\n\\) can appear in strings
    # (ex: Edu Nouns) blindly using unicode_escape will cause the string to be escaped incorrectly
    # only escape strings that can't be parsed as json.

    # Some uri strings are escaped incorrectly because of unicode_escape being used to deal with
    # unicode characters in the uri. This validator deals with those incorrectly escaped strings
    @validator("uri")
    def validate_token_uri(cls, uri):
        prefix = "data:application/json;base64,"
        if uri is not None and uri.startswith(prefix):
            uri = uri[len(prefix) :]  # noqa
            raw = base64.b64decode(uri)
            try:
                json.loads(raw)
                return prefix + base64.b64encode(raw).decode("utf-8")
            except Exception:
                escaped = raw.decode("utf-8").encode("unicode_escape")
                return prefix + base64.b64encode(escaped).decode("utf-8")
        return uri
