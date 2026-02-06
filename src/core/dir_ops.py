import os
import shutil 
from pathlib import Path
from typing import Union, List, Optional
import logging

logger = logging.getLogger(__name__)


class DirOps:
    def __init__(self, current_dir):
        self.current_dir = Path(current_dir) or Path.cwd()

    # ----------------------------------- INTERNAL HELPER FUNCTIONS---------------------------------------------#
    def _ensure_path_exists(self, dirpath: Union[str, Path]) -> bool:
            path = Path(dirpath)
            if not dirpath.exists():
                logger.error("Directory not found: %s", path)
                return False
            if not dirpath.is_dir():
                logger.error("Expected a directory, instead got a file: %s", path)
                return False
            return True
    
    def _resolve_path(self, dirpath: Union[str, Path]) -> Path:
        path = Path(dirpath)
        if not path.is_absolute():
            path = self.current_dir / path
        return path.resolve() 


    # ----------------------------------- CRUD OPERATIONS---------------------------------------------#
    
    # List Directories 

    def list_dir(self, dirpath: Union[str, Path], *,show_hidden: bool=False, dir_only: bool=False, files_only: bool=False, names_only=False) -> Optional[List[Path]]:

        try:
            path = self._resolve_path(dirpath)
            if not self._ensure_path_exists(path):
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

            # Return directory and file names
            
            result = [f"{item.name}/" if item.is_dir() else item.name for item in items] if names_only else items

            logger.info("%d listed in directory %s", len(items), path)
            return result
        
        except OSError as e:
            logger.error("Error listing directory %s: %s", path, e)
            return None
        
    # Create Directory

    def create_dir(self, dirpath: Union[str, Path], parents: bool=True, exists: bool=False) -> bool:

        path = self._resolve_path(dirpath)
        try:
            path.mkdir(parents=parents, exist_ok=exists)
            logger.info("Directory created succssfully: %s", path)
            return True

        except FileExistsError as e:
            logger.error("Directory already exists: %s", path)
            return False
        except OSError as e:
            logger.error("Failed to create Directory %s: %s", path, e)
            return False
        
    # Copy directory 

    def copy_dir(self, source: Union[str, Path], destination: Union[str, Path], exists: bool=False) -> bool:
        
        try:
            source = self._resolve_path(source)
            destination = self._resolve_path(destination)

            if not self._ensure_path_exists(source):
                return False

            shutil.copytree(source, destination, dirs_exist_ok=exists)
            logger.info("Directory copied: %s -> %s", source, destination)
            return True
        
        except FileExistsError as e:
            logger.error("Destination directory already exists: %s. Set exists=True to overwrite/merge.", destination)
            return False
        except OSError as e:
            logger.error("Failed to copy directory %s -> %s: %s", source, destination, e)
            return False

    # Move Directory
        
    def move_dir(self, source: Union[str, Path], destination: Union[str, Path], overwrite: bool=False) -> bool:

        source = self._resolve_path(source)
        destination = self._resolve_path(destination)

        try:
            if not source.exists():
                logger.error("Source not found: %s", source)
                return False
            
            if destination.exists():
                if not overwrite:
                    logger.error("Destination already exists: %s. Set overwrite=True to proceed.", destination)
                else:
                    logger.warning("Overwriting existing directory: %s", destination)
                    shutil.rmtree(destination)
            
            shutil.move(str(source), str(destination))
            logger.info("Directory moved: %s -> %s", source, destination)
            return True
        
        except OSError as e:
            logger.error("Failed to move directory %s -> %s: %s", source, destination, e)
            return False

    # Delete Directory
    
    def delete_dir(self, dirpath: Union[str, Path], ignore_errors: bool = False) -> bool:
        path = self._resolve_path(dirpath)
        
        if not self._ensure_path_exists(path):
            return False

        try:
            
            shutil.rmtree(path, ignore_errors=ignore_errors)
            logger.info("Directory deleted successfully: %s", path)
            return True
        except OSError as e:
            logger.error("Failed to delete directory %s: %s", path, e)
            return False

    # Get Directory size
   
    def get_directory_size(self, dirpath: Union[str, Path]) -> Optional[int]:
                
        try:
            path = self._resolve_path(dirpath)
            if not self._ensure_path_exists(path):
                return 
            
            total_size = sum(f.stat().st_size for f in path.rglob("*") if f.is_file)
            logger.info("Size of %s: %d bytes", path, total_size)
            return total_size

        except OSError as e:
            logger.error("Error accessing files in %s: %s", path, e)
            return None
        
    # Check if directory is empty
    
    def is_empty(self, dirpath: Union[str, Path]) -> Optional[bool]:
        path = self._resolve_path(dirpath)
        
        if not self._ensure_path_exists(path):
            return None

        try:
           return not any(path.iterdir())
        except Exception as e:
            logger.error(f"Error checking if directory is empty {path}: {e}")
            return None            
