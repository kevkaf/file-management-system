import os
import shutil 
from pathlib import Path
from typing import Union, List, Optional
import logging

logger = logging.getLogger(__name__)


class DirOps:
    def __init__(self, current_dir):
        self.current_dir = current_dir or os.getcwd()

    def list_dir(self, dirpath: Union[str, Path], show_hidden: bool=False, dir_only: bool=False, files_only: bool=False) -> Optional[List[Path]]:

        try:
            path = Path(dirpath)
            if not path.exists():
                logger.error("Directory %s not found", path)
                return None
            
            if not path.is_dir():
                logger.error("Not a directory: %s", path)
                return None
            
            items = list(path.iterdir())

            # Filter hidden files
            if not show_hidden:
                items = [item for item in items if not item.name.startswith(".")]

            # Filter by type
            if files_only:
                items = [item for item in items if item.is_file()]
            elif dir_only:
                items = [item for item in items if item.is_dir()]

            # Sort directories then files in a way aphabeticaly way
            items.sort(key= lambda x: (not x.is_dir(), x.name.lower()))

            logger.info("%d listed in directory %s", len(items), path)
            return items
        
        except OSError as e:
            logger.error("Error listing directory %s: %s", path, e)
            return None