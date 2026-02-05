from pathlib import Path
from typing import Union, Iterator, List
import logging

class FileOps:
    def __init__(self, base_path: Union[str, Path, None] = None):
        self.base_path = Path(base_path).resolve() if base_path else Path.cwd()

        