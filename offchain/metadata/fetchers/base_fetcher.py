from typing import Protocol


class BaseFetcher(Protocol):
    """Protocol for fetchers

    Requires timeout and max_retries variables to be passed in init function.

    All fetchers must implement:
    - setters for timeout and max_retries
    - a function for registering an adapter to a url prefix
    - a function for fetching mime type and size
    - a function for fetching content from a url
    """

    timeout: int
    max_retries: int

    def __init__(self, timeout: int, max_retries: int) -> None:
        pass

    def set_timeout(self):
        pass

    def set_max_retries(self):
        pass

    def register_adapter(self):
        """Given an adapter and url prefix, register the adapter to the url prefix."""
        pass

    def fetch_mime_type_and_size(self):
        """Given a url, return the mime type and size of the content"""
        pass

    def fetch_content(self):
        """Given a url, return the content in the form of a dict"""
        pass
