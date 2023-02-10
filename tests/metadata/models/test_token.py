import pytest

from offchain import Token


class TestToken:
    def test_token_validates_chain_identifier_is_uppercase(self):
        with pytest.raises(ValueError):
            Token(
                collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
                token_id=9559,
                chain_identifier="ethereum-mainnet",
            )

    def test_token_validates_chain_identifier_is_separated_by_hyphen(self):
        with pytest.raises(ValueError):
            Token(
                collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
                token_id=9559,
                chain_identifier="ETHEREUMMAINNET",
            )

    def test_token_validates_chain_identifier_starts_and_ends_correctly(self):
        with pytest.raises(ValueError):
            Token(
                collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
                token_id=9559,
                chain_identifier="aETHEREUM-MAINNETa",
            )

    def test_validate_token_uri(self):
        valid_token = Token(
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id=9559,
            uri="ipfs://bafkreiank5vcp4jtnf35zhnne6h25yolhyf4dfri5kqdpohsv4apkuxl5i",
        )
        valid_base64_token = Token(
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id=9559,
            uri="data:application/json;base64,eyJuYW1lIjogIlpvcmIgIzYwMSIsICJkZXNjcmlwdGlvbiI6ICJab3JicyB3ZXJlIGRpc3RyaWJ1dGVkIGZvciBmcmVlIGJ5IFpPUkEgb24gTmV3IFllYXLigJlzIDIwMjIuIEVhY2ggTkZUIGltYnVlcyB0aGUgcHJvcGVydGllcyBvZiBpdHMgd2FsbGV0IGhvbGRlciwgYW5kIHdoZW4gc2VudCB0byBzb21lb25lIGVsc2UsIHdpbGwgdHJhbnNmb3JtLlxuXG5WaWV3IHRoaXMgTkZUIGF0IFt6b3JiLmRldi9uZnQvNjAxXShodHRwczovL3pvcmIuZGV2L25mdC82MDEpIiwgImltYWdlIjogImRhdGE6aW1hZ2Uvc3ZnK3htbDtiYXNlNjQsUEhOMlp5QjRiV3h1Y3owaWFIUjBjRG92TDNkM2R5NTNNeTV2Y21jdk1qQXdNQzl6ZG1jaUlIWnBaWGRDYjNnOUlqQWdNQ0F4TVRBZ01URXdJajQ4WkdWbWN6NDhjbUZrYVdGc1IzSmhaR2xsYm5RZ2FXUTlJbWQ2Y2lJZ1ozSmhaR2xsYm5SVWNtRnVjMlp2Y20wOUluUnlZVzV6YkdGMFpTZzJOaTQwTlRjNElESTBMak0xTnpVcElITmpZV3hsS0RjMUxqSTVNRGdwSWlCbmNtRmthV1Z1ZEZWdWFYUnpQU0oxYzJWeVUzQmhZMlZQYmxWelpTSWdjajBpTVNJZ1kzZzlJakFpSUdONVBTSXdKU0krUEhOMGIzQWdiMlptYzJWMFBTSXhOUzQyTWlVaUlITjBiM0F0WTI5c2IzSTlJbWh6YkNnek1EQXNJRGN3SlN3Z09UVWxLU0lnTHo0OGMzUnZjQ0J2Wm1aelpYUTlJak01TGpVNEpTSWdjM1J2Y0MxamIyeHZjajBpYUhOc0tETXdNQ3dnTnpJbExDQTRNaVVwSWlBdlBqeHpkRzl3SUc5bVpuTmxkRDBpTnpJdU9USWxJaUJ6ZEc5d0xXTnZiRzl5UFNKb2Myd29NekkzTENBM055VXNJRFkxSlNraUlDOCtQSE4wYjNBZ2IyWm1jMlYwUFNJNU1DNDJNeVVpSUhOMGIzQXRZMjlzYjNJOUltaHpiQ2d6TWprc0lEZzVKU3dnTlRnbEtTSWdMejQ4YzNSdmNDQnZabVp6WlhROUlqRXdNQ1VpSUhOMGIzQXRZMjlzYjNJOUltaHpiQ2d6TWprc0lEazBKU3dnTlRjbEtTSWdMejQ4TDNKaFpHbGhiRWR5WVdScFpXNTBQand2WkdWbWN6NDhaeUIwY21GdWMyWnZjbTA5SW5SeVlXNXpiR0YwWlNnMUxEVXBJajQ4Y0dGMGFDQmtQU0pOTVRBd0lEVXdRekV3TUNBeU1pNHpPRFU0SURjM0xqWXhORElnTUNBMU1DQXdRekl5TGpNNE5UZ2dNQ0F3SURJeUxqTTROVGdnTUNBMU1FTXdJRGMzTGpZeE5ESWdNakl1TXpnMU9DQXhNREFnTlRBZ01UQXdRemMzTGpZeE5ESWdNVEF3SURFd01DQTNOeTQyTVRReUlERXdNQ0ExTUZvaUlHWnBiR3c5SW5WeWJDZ2paM3B5S1NJZ0x6NDhjR0YwYUNCemRISnZhMlU5SW5KblltRW9NQ3d3TERBc01DNHdOelVwSWlCbWFXeHNQU0owY21GdWMzQmhjbVZ1ZENJZ2MzUnliMnRsTFhkcFpIUm9QU0l4SWlCa1BTSk5OVEFzTUM0MVl6STNMak1zTUN3ME9TNDFMREl5TGpJc05Ea3VOU3cwT1M0MVV6YzNMak1zT1RrdU5TdzFNQ3c1T1M0MVV6QXVOU3czTnk0ekxEQXVOU3cxTUZNeU1pNDNMREF1TlN3MU1Dd3dMalY2SWlBdlBqd3ZaejQ4TDNOMlp6ND0ifQ==",  # noqa: E501
        )
        incorrectly_escaped_token = Token(
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id=9559,
            uri="data:application/json;base64,ewogICAgYmxhOiBibGFiYWwKICAgIG51bTI6IG51bTIvbgogICAgYW5kbGFzdDogbGFzdAp9",
        )

        correctly_escaped_uri = "data:application/json;base64,e1xuICAgIGJsYTogYmxhYmFsXG4gICAgbnVtMjogbnVtMi9uXG4gICAgYW5kbGFzdDogbGFzdFxufQ=="  # noqa: E501

        assert valid_token.uri == "ipfs://bafkreiank5vcp4jtnf35zhnne6h25yolhyf4dfri5kqdpohsv4apkuxl5i"
        assert (
            valid_base64_token.uri
            == "data:application/json;base64,eyJuYW1lIjogIlpvcmIgIzYwMSIsICJkZXNjcmlwdGlvbiI6ICJab3JicyB3ZXJlIGRpc3RyaWJ1dGVkIGZvciBmcmVlIGJ5IFpPUkEgb24gTmV3IFllYXLigJlzIDIwMjIuIEVhY2ggTkZUIGltYnVlcyB0aGUgcHJvcGVydGllcyBvZiBpdHMgd2FsbGV0IGhvbGRlciwgYW5kIHdoZW4gc2VudCB0byBzb21lb25lIGVsc2UsIHdpbGwgdHJhbnNmb3JtLlxuXG5WaWV3IHRoaXMgTkZUIGF0IFt6b3JiLmRldi9uZnQvNjAxXShodHRwczovL3pvcmIuZGV2L25mdC82MDEpIiwgImltYWdlIjogImRhdGE6aW1hZ2Uvc3ZnK3htbDtiYXNlNjQsUEhOMlp5QjRiV3h1Y3owaWFIUjBjRG92TDNkM2R5NTNNeTV2Y21jdk1qQXdNQzl6ZG1jaUlIWnBaWGRDYjNnOUlqQWdNQ0F4TVRBZ01URXdJajQ4WkdWbWN6NDhjbUZrYVdGc1IzSmhaR2xsYm5RZ2FXUTlJbWQ2Y2lJZ1ozSmhaR2xsYm5SVWNtRnVjMlp2Y20wOUluUnlZVzV6YkdGMFpTZzJOaTQwTlRjNElESTBMak0xTnpVcElITmpZV3hsS0RjMUxqSTVNRGdwSWlCbmNtRmthV1Z1ZEZWdWFYUnpQU0oxYzJWeVUzQmhZMlZQYmxWelpTSWdjajBpTVNJZ1kzZzlJakFpSUdONVBTSXdKU0krUEhOMGIzQWdiMlptYzJWMFBTSXhOUzQyTWlVaUlITjBiM0F0WTI5c2IzSTlJbWh6YkNnek1EQXNJRGN3SlN3Z09UVWxLU0lnTHo0OGMzUnZjQ0J2Wm1aelpYUTlJak01TGpVNEpTSWdjM1J2Y0MxamIyeHZjajBpYUhOc0tETXdNQ3dnTnpJbExDQTRNaVVwSWlBdlBqeHpkRzl3SUc5bVpuTmxkRDBpTnpJdU9USWxJaUJ6ZEc5d0xXTnZiRzl5UFNKb2Myd29NekkzTENBM055VXNJRFkxSlNraUlDOCtQSE4wYjNBZ2IyWm1jMlYwUFNJNU1DNDJNeVVpSUhOMGIzQXRZMjlzYjNJOUltaHpiQ2d6TWprc0lEZzVKU3dnTlRnbEtTSWdMejQ4YzNSdmNDQnZabVp6WlhROUlqRXdNQ1VpSUhOMGIzQXRZMjlzYjNJOUltaHpiQ2d6TWprc0lEazBKU3dnTlRjbEtTSWdMejQ4TDNKaFpHbGhiRWR5WVdScFpXNTBQand2WkdWbWN6NDhaeUIwY21GdWMyWnZjbTA5SW5SeVlXNXpiR0YwWlNnMUxEVXBJajQ4Y0dGMGFDQmtQU0pOTVRBd0lEVXdRekV3TUNBeU1pNHpPRFU0SURjM0xqWXhORElnTUNBMU1DQXdRekl5TGpNNE5UZ2dNQ0F3SURJeUxqTTROVGdnTUNBMU1FTXdJRGMzTGpZeE5ESWdNakl1TXpnMU9DQXhNREFnTlRBZ01UQXdRemMzTGpZeE5ESWdNVEF3SURFd01DQTNOeTQyTVRReUlERXdNQ0ExTUZvaUlHWnBiR3c5SW5WeWJDZ2paM3B5S1NJZ0x6NDhjR0YwYUNCemRISnZhMlU5SW5KblltRW9NQ3d3TERBc01DNHdOelVwSWlCbWFXeHNQU0owY21GdWMzQmhjbVZ1ZENJZ2MzUnliMnRsTFhkcFpIUm9QU0l4SWlCa1BTSk5OVEFzTUM0MVl6STNMak1zTUN3ME9TNDFMREl5TGpJc05Ea3VOU3cwT1M0MVV6YzNMak1zT1RrdU5TdzFNQ3c1T1M0MVV6QXVOU3czTnk0ekxEQXVOU3cxTUZNeU1pNDNMREF1TlN3MU1Dd3dMalY2SWlBdlBqd3ZaejQ4TDNOMlp6ND0ifQ=="  # noqa: E501
        )  # noqa
        assert incorrectly_escaped_token.uri == correctly_escaped_uri
