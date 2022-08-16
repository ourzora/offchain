from typing import Protocol


class BaseFetcher(Protocol):
    def register_adapter(self):
        """Given an adapter and url prefix, register the adapter to the url prefix."""
        pass

    def fetch_mime_type_and_size(self):
        """Given a url, return the mime type and size of the content"""
        pass

    def fetch_content(self):
        """Given a url, return the content in the form of a dict"""
        pass
