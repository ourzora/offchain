from typing import Protocol


class BasePipeline(Protocol):
    """Base protocol for Pipeline classes"""

    def __init__(self) -> None:
        pass

    def run(self):
        """Runs the pipeline"""
        pass
