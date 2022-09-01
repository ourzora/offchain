# flake8: noqa: E501
from unittest.mock import MagicMock, Mock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    Attribute,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.loot import LootParser
from offchain.web3.contract_caller import ContractCaller


class TestLootParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0xff9c1b15b16263c61d017ee9f65c50e4ae0113d7",
        token_id=345,
        uri=None,
    )

    raw_data = {
        "name": "Bag #345",
        "description": "Loot is randomized adventurer gear generated and "
        "stored on chain. Stats, images, and other "
        "functionality are intentionally omitted for "
        "others to interpret. Feel free to use Loot in "
        "any way you want.",
        "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaW5ZTWluIG1lZXQiIHZpZXdCb3g9IjAgMCAzNTAgMzUwIj48c3R5bGU+LmJhc2UgeyBmaWxsOiB3aGl0ZTsgZm9udC1mYW1pbHk6IHNlcmlmOyBmb250LXNpemU6IDE0cHg7IH08L3N0eWxlPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9ImJsYWNrIiAvPjx0ZXh0IHg9IjEwIiB5PSIyMCIgY2xhc3M9ImJhc2UiPlF1YXJ0ZXJzdGFmZjwvdGV4dD48dGV4dCB4PSIxMCIgeT0iNDAiIGNsYXNzPSJiYXNlIj5IYXJkIExlYXRoZXIgQXJtb3Igb2YgQnJpbGxpYW5jZTwvdGV4dD48dGV4dCB4PSIxMCIgeT0iNjAiIGNsYXNzPSJiYXNlIj5MaW5lbiBIb29kIG9mIFBlcmZlY3Rpb248L3RleHQ+PHRleHQgeD0iMTAiIHk9IjgwIiBjbGFzcz0iYmFzZSI+T3JuYXRlIEJlbHQ8L3RleHQ+PHRleHQgeD0iMTAiIHk9IjEwMCIgY2xhc3M9ImJhc2UiPkxlYXRoZXIgQm9vdHMgb2YgU2tpbGw8L3RleHQ+PHRleHQgeD0iMTAiIHk9IjEyMCIgY2xhc3M9ImJhc2UiPkRyYWdvbnNraW4gR2xvdmVzIG9mIEFuZ2VyPC90ZXh0Pjx0ZXh0IHg9IjEwIiB5PSIxNDAiIGNsYXNzPSJiYXNlIj5OZWNrbGFjZTwvdGV4dD48dGV4dCB4PSIxMCIgeT0iMTYwIiBjbGFzcz0iYmFzZSI+VGl0YW5pdW0gUmluZzwvdGV4dD48L3N2Zz4=",
    }

    image_uri = '<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" viewBox="0 0 350 350"><style>.base { fill: white; font-family: serif; font-size: 14px; }</style><rect width="100%" height="100%" fill="black" /><text x="10" y="20" class="base">Quarterstaff</text><text x="10" y="40" class="base">Hard Leather Armor of Brilliance</text><text x="10" y="60" class="base">Linen Hood of Perfection</text><text x="10" y="80" class="base">Ornate Belt</text><text x="10" y="100" class="base">Leather Boots of Skill</text><text x="10" y="120" class="base">Dragonskin Gloves of Anger</text><text x="10" y="140" class="base">Necklace</text><text x="10" y="160" class="base">Titanium Ring</text></svg>'

    def test_loot_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = LootParser(fetcher=fetcher, contract_caller=contract_caller)
        assert parser.should_parse_token(token=self.token) == True

    def test_loot_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", 0))
        fetcher.fetch_content = Mock(side_effect=[self.raw_data, self.image_uri])
        parser = LootParser(fetcher=fetcher, contract_caller=contract_caller)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0xff9c1b15b16263c61d017ee9f65c50e4ae0113d7",
                token_id=345,
                uri="data:application/json;base64,eyJuYW1lIjogIkJhZyAjMzQ1IiwgImRlc2NyaXB0aW9uIjogIkxvb3QgaXMgcmFuZG9taXplZCBhZHZlbnR1cmVyIGdlYXIgZ2VuZXJhdGVkIGFuZCBzdG9yZWQgb24gY2hhaW4uIFN0YXRzLCBpbWFnZXMsIGFuZCBvdGhlciBmdW5jdGlvbmFsaXR5IGFyZSBpbnRlbnRpb25hbGx5IG9taXR0ZWQgZm9yIG90aGVycyB0byBpbnRlcnByZXQuIEZlZWwgZnJlZSB0byB1c2UgTG9vdCBpbiBhbnkgd2F5IHlvdSB3YW50LiIsICJpbWFnZSI6ICJkYXRhOmltYWdlL3N2Zyt4bWw7YmFzZTY0LFBITjJaeUI0Yld4dWN6MGlhSFIwY0RvdkwzZDNkeTUzTXk1dmNtY3ZNakF3TUM5emRtY2lJSEJ5WlhObGNuWmxRWE53WldOMFVtRjBhVzg5SW5oTmFXNVpUV2x1SUcxbFpYUWlJSFpwWlhkQ2IzZzlJakFnTUNBek5UQWdNelV3SWo0OGMzUjViR1UrTG1KaGMyVWdleUJtYVd4c09pQjNhR2wwWlRzZ1ptOXVkQzFtWVcxcGJIazZJSE5sY21sbU95Qm1iMjUwTFhOcGVtVTZJREUwY0hnN0lIMDhMM04wZVd4bFBqeHlaV04wSUhkcFpIUm9QU0l4TURBbElpQm9aV2xuYUhROUlqRXdNQ1VpSUdacGJHdzlJbUpzWVdOcklpQXZQangwWlhoMElIZzlJakV3SWlCNVBTSXlNQ0lnWTJ4aGMzTTlJbUpoYzJVaVBsRjFZWEowWlhKemRHRm1aand2ZEdWNGRENDhkR1Y0ZENCNFBTSXhNQ0lnZVQwaU5EQWlJR05zWVhOelBTSmlZWE5sSWo1SVlYSmtJRXhsWVhSb1pYSWdRWEp0YjNJZ2IyWWdRbkpwYkd4cFlXNWpaVHd2ZEdWNGRENDhkR1Y0ZENCNFBTSXhNQ0lnZVQwaU5qQWlJR05zWVhOelBTSmlZWE5sSWo1TWFXNWxiaUJJYjI5a0lHOW1JRkJsY21abFkzUnBiMjQ4TDNSbGVIUStQSFJsZUhRZ2VEMGlNVEFpSUhrOUlqZ3dJaUJqYkdGemN6MGlZbUZ6WlNJK1QzSnVZWFJsSUVKbGJIUThMM1JsZUhRK1BIUmxlSFFnZUQwaU1UQWlJSGs5SWpFd01DSWdZMnhoYzNNOUltSmhjMlVpUGt4bFlYUm9aWElnUW05dmRITWdiMllnVTJ0cGJHdzhMM1JsZUhRK1BIUmxlSFFnZUQwaU1UQWlJSGs5SWpFeU1DSWdZMnhoYzNNOUltSmhjMlVpUGtSeVlXZHZibk5yYVc0Z1IyeHZkbVZ6SUc5bUlFRnVaMlZ5UEM5MFpYaDBQangwWlhoMElIZzlJakV3SWlCNVBTSXhOREFpSUdOc1lYTnpQU0ppWVhObElqNU9aV05yYkdGalpUd3ZkR1Y0ZEQ0OGRHVjRkQ0I0UFNJeE1DSWdlVDBpTVRZd0lpQmpiR0Z6Y3owaVltRnpaU0krVkdsMFlXNXBkVzBnVW1sdVp6d3ZkR1Y0ZEQ0OEwzTjJaejQ9In0=",
            ),
            raw_data={
                "name": "Bag #345",
                "description": "Loot is randomized adventurer gear generated and "
                "stored on chain. Stats, images, and other "
                "functionality are intentionally omitted for "
                "others to interpret. Feel free to use Loot in "
                "any way you want.",
                "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHByZXNlcnZlQXNwZWN0UmF0aW89InhNaW5ZTWluIG1lZXQiIHZpZXdCb3g9IjAgMCAzNTAgMzUwIj48c3R5bGU+LmJhc2UgeyBmaWxsOiB3aGl0ZTsgZm9udC1mYW1pbHk6IHNlcmlmOyBmb250LXNpemU6IDE0cHg7IH08L3N0eWxlPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9ImJsYWNrIiAvPjx0ZXh0IHg9IjEwIiB5PSIyMCIgY2xhc3M9ImJhc2UiPlF1YXJ0ZXJzdGFmZjwvdGV4dD48dGV4dCB4PSIxMCIgeT0iNDAiIGNsYXNzPSJiYXNlIj5IYXJkIExlYXRoZXIgQXJtb3Igb2YgQnJpbGxpYW5jZTwvdGV4dD48dGV4dCB4PSIxMCIgeT0iNjAiIGNsYXNzPSJiYXNlIj5MaW5lbiBIb29kIG9mIFBlcmZlY3Rpb248L3RleHQ+PHRleHQgeD0iMTAiIHk9IjgwIiBjbGFzcz0iYmFzZSI+T3JuYXRlIEJlbHQ8L3RleHQ+PHRleHQgeD0iMTAiIHk9IjEwMCIgY2xhc3M9ImJhc2UiPkxlYXRoZXIgQm9vdHMgb2YgU2tpbGw8L3RleHQ+PHRleHQgeD0iMTAiIHk9IjEyMCIgY2xhc3M9ImJhc2UiPkRyYWdvbnNraW4gR2xvdmVzIG9mIEFuZ2VyPC90ZXh0Pjx0ZXh0IHg9IjEwIiB5PSIxNDAiIGNsYXNzPSJiYXNlIj5OZWNrbGFjZTwvdGV4dD48dGV4dCB4PSIxMCIgeT0iMTYwIiBjbGFzcz0iYmFzZSI+VGl0YW5pdW0gUmluZzwvdGV4dD48L3N2Zz4=",
            },
            attributes=[
                Attribute(
                    trait_type="Chest",
                    value="Hard Leather Armor of Brilliance",
                    display_type=None,
                ),
                Attribute(trait_type="Foot", value="Leather Boots of Skill", display_type=None),
                Attribute(
                    trait_type="Hand",
                    value="Dragonskin Gloves of Anger",
                    display_type=None,
                ),
                Attribute(
                    trait_type="Head",
                    value="Linen Hood of Perfection",
                    display_type=None,
                ),
                Attribute(trait_type="Neck", value="Necklace", display_type=None),
                Attribute(trait_type="Ring", value="Titanium Ring", display_type=None),
                Attribute(trait_type="Waist", value="Ornate Belt", display_type=None),
                Attribute(trait_type="Weapon", value="Quarterstaff", display_type=None),
            ],
            standard=None,
            name="Bag #345",
            description="Loot is randomized adventurer gear generated and "
            "stored on chain. Stats, images, and other "
            "functionality are intentionally omitted for "
            "others to interpret. Feel free to use Loot in "
            "any way you want.",
            mime_type="application/json",
            image=MediaDetails(
                size=None,
                sha256=None,
                uri="%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20preserveAspectRatio%3D%22xMinYMin%20meet%22%20viewBox%3D%220%200%20350%20350%22%3E%3Cstyle%3E.base%20%7B%20fill%3A%20white%3B%20font-family%3A%20serif%3B%20font-size%3A%2014px%3B%20%7D%3C/style%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22black%22%20/%3E%3Ctext%20x%3D%2210%22%20y%3D%2220%22%20class%3D%22base%22%3EQuarterstaff%3C/text%3E%3Ctext%20x%3D%2210%22%20y%3D%2240%22%20class%3D%22base%22%3EHard%20Leather%20Armor%20of%20Brilliance%3C/text%3E%3Ctext%20x%3D%2210%22%20y%3D%2260%22%20class%3D%22base%22%3ELinen%20Hood%20of%20Perfection%3C/text%3E%3Ctext%20x%3D%2210%22%20y%3D%2280%22%20class%3D%22base%22%3EOrnate%20Belt%3C/text%3E%3Ctext%20x%3D%2210%22%20y%3D%22100%22%20class%3D%22base%22%3ELeather%20Boots%20of%20Skill%3C/text%3E%3Ctext%20x%3D%2210%22%20y%3D%22120%22%20class%3D%22base%22%3EDragonskin%20Gloves%20of%20Anger%3C/text%3E%3Ctext%20x%3D%2210%22%20y%3D%22140%22%20class%3D%22base%22%3ENecklace%3C/text%3E%3Ctext%20x%3D%2210%22%20y%3D%22160%22%20class%3D%22base%22%3ETitanium%20Ring%3C/text%3E%3C/svg%3E",
                mime_type="image/svg+xml",
            ),
        )
