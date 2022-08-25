from offchain.constants.addresses import CollectionAddress
from offchain.metadata.constants.nouns import Seeds
from offchain.metadata.fetchers import BaseFetcher
from offchain.metadata.models.metadata import Metadata, MediaDetails, MetadataStandard, Attribute
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry
from offchain.metadata.web3.batching import BatchContractViewCaller

STANDARD = MetadataStandard.NOUNS_STANDARD


@ParserRegistry.register
class NounsParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [
        CollectionAddress.NOUNS,
        CollectionAddress.LIL_NOUNS,
    ]

    def __init__(
        self, fetcher: BaseFetcher, contract_caller: BatchContractViewCaller
    ) -> None:
        self.contract_caller = contract_caller
        super().__init__(fetcher)

    def parse_attributes(self, seeds: Seeds) -> list[Attribute]:
        attributes = []

        def normalize_value(value: str) -> str:
            return value.replace("-", " ")

        for trait, value in seeds.__dict__.values():
            attribute = Attribute(
                trait_type=trait,
                value=normalize_value(value),
                display_type=None,
            )
            attributes.append(attribute)

        return attributes

    def batch_seeds(self, token_ids: list[int]) -> list[Seeds]:
        seeds = []

        results = self.caller.single_address_single_fn_many_args(
            self.contract_address,
            function_sig="seeds(uint256)",
            return_type=["uint48", "uint48", "uint48", "uint48", "uint48"],
            args=[[id] for id in token_ids],
        )

        for result in results:
            deserialized = Seeds.from_raw(
                background_index=result[0],
                body_index=result[1],
                accessory_index=result[2],
                head_index=result[3],
                glasses_index=result[4],
            )
            seeds.append(deserialized)

        return seeds

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:
        mime, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        image = None
        image_uri = raw_data.get("image") or raw_data.get("image_data")
        if image_uri:
            image_mime, image_size = self.fetcher.fetch_mime_type_and_size(image_uri)
            image = MediaDetails(size=image_size, uri=image_uri, mime_type=image_mime)

        def seeds(token_id: int) -> Seeds:
            return self.batch_seeds([token_id])[0]

        attributes = self.parse_attributes(seeds(token.token_id))

        return Metadata(
            chain_identifier=token.chain_identifier,
            collection_address=token.collection_address,
            token_id=token.token_id,
            token_uri=token.uri,
            raw_data=raw_data,
            standard=STANDARD,
            attributes=attributes,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime,
            image=image,
        )
