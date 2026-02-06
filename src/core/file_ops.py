from pathlib import Path
from typing import Union, Iterator, List
import logging
import shutil

logger = logging.getLogger(__name__)

class FileOps:
    def __init__(self, base_path: Union[str, Path, None] = None):
        self.base_path = Path(base_path).resolve() if base_path else Path.cwd()

    
    # --------- INTERNAL HELPER FUNCTIONS -------------- #

    def _resolve_path(self, filepath: Union[str, Path]) -> Path:
        path = Path(filepath)
        return path if path.is_absolute() else (self.base_path / path)
    
    def _ensure_parent_dir(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

    def _ensure_file_exists(self, path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if path.is_dir():
            raise IsADirectoryError(f"Expected file but got directory: {path}")
        
    # --------- CRUD OPERATIONS ---------------------- #


    # Create File

    def create_file(self, filepath: Union[str, Path], content: str="", *, encoding: str="utf-8", overwrite: bool=False) -> bool:
        
        try:
            path = self._resolve_path(filepath)

            if path.exists() and not overwrite:
                raise FileExistsError(f"File already exists: {path}")
            if path.exists() and path.is_dir():
                raise IsADirectoryError(f"Cannot create file, path is a directory: {path}")
            
            self._ensure_parent_dir(path)

            with open(path, 'w', encoding=encoding) as f:
                f.write(content)

            logger.info("File created: %s", path)
            return True
        
        except OSError as e:
            logger.error("Error creating file %s: %s", path, e)
            return False

    # Read File 
               
    def read_file(self, filepath: Union[str, Path], *, mode: str="full", encoding: str="utf-8", binary: bool=False, chunk_size=8192) -> Union[str, bytes, List[str], Iterator[Union[str, bytes]]]:

        try:

            path = self._resolve_path(filepath)

            self._ensure_file_exists(path)

            file_mode = "rb" if binary else "r"
            file_encoding = None if binary else encoding

            if mode == "full":
                with open(path, file_mode, encoding=file_encoding) as f:
                    data = f.read()
                logger.info("Read File: %s", path)
                return data
            
            elif mode == "lines":
                with open(path, file_mode, encoding=file_encoding) as f:
                    lines = f.readlines()
                logger.info("Read %d lines from %s", len(lines), path)
                return lines

            elif mode == "chunk":
                def iterator():
                    with open(path, file_mode, encoding=file_encoding) as f:
                        while True:
                            chunk = f.read(chunk_size)
                            if not chunk:
                                break
                            yield chunk

                logger.info("Reading file in chunks: %s", path)
                return iterator()
        
            else:
                raise ValueError(f"Unknown read mode: {mode}")

        except OSError as e:
            logger.error("Failed to read path: %s", path)
            raise


    # Update File

    def update_file(self, filepath: Union[str, Path], content: str="", *, append: bool=False, encoding: str="utf-8") -> bool:

        try:
            path = self._resolve_path(filepath)

            self._ensure_file_exists(path)
            
            update_mode = "a" if append else "w"
            
            with open(path, update_mode, encoding=encoding) as f:
                f.write(content)


            action = "appended to" if append else "updated"
            logger.info("File %s: %s", action, path)
            return True

        except OSError as e:
            logger.error("Failed to update path %s: %s", path, e)
            return False



    # Delete File

    def delete_file(self, filepath: Union[str, Path]) -> bool:

        try: 
            path = self._resolve_path(filepath)

            self._ensure_file_exists(path)
            
            path.unlink()
            logger.info("File deleted successfully: %s", path)
            return True
        
        except OSError as e:
            logger.error("Failed to delete file: %s", path)
            return False

        
   
    # Copy / Move file

    def copy_or_move_file(self, source: Union[str, Path], destination: Union[str, Path], move: bool=False) -> bool:

        try:
            source = self._resolve_path(source)
            destination = self._resolve_path(destination)

            self._ensure_file_exists(source)

            if destination.is_dir():
                destination = destination / source.name
            
            self._ensure_parent_dir(destination)
            
            if move:                
                shutil.move(str(source), str(destination))
                logger.info("%s successfully moved to %s", source, destination)
            else:
                shutil.copy2(source, destination)
                logger.info("%s successfully copy to %s", source, destination)
                
            return True
        
        except OSError as e:
            text = "moving" if move else "copyiing"
            logger.error("Error %s file %s -> %s: %s", text, source, destination, e)
            return False
    
    
    # Rename File

    def rename_file(self, filepath: Union[str, Path], new_name: str) -> bool:
        
        try:
            path = self._resolve_path(filepath)
            self._ensure_file_exists(path)

            new_path = path.parent / new_name
            path.rename(new_path)

            logger.info("File %s renamed successfully", path)
            return True
        
        except OSError as e:
            logger.error("Failed to rename file %s due to %s", path, e)
            return False