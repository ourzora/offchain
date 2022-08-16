from typing import Protocol


class BaseFetcher(Protocol):
    def register_adapter(self):
        pass

    def fetch_mime_type_and_size(self):
        pass

    def fetch_content(self):
        pass
