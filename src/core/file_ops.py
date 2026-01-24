import os
from pathlib import Path
from typing import Union, Optional, List, BinaryIO, TextIO
import logging



class FileOperations:
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self._setup_logging()

    
    def _setup_logging(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler =  logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _resolve_path(self, filepath: Union[str, Path]) -> Path:
        
        path = Path(filepath)

        if not path.is_absolute():
            return self.base_path / path
        
        try:
            return path.resolve()
        except Exception:
            return path
        

    def _log_error(self, message: str, level: str = "ERROR"):
        # Log error messages
        log_level = getattr(self.logger, level.lower(), logging.ERROR)
        self.logger.log(log_level, message)
    

    def _ensure_parent_exists(self, path: Path) -> bool:
        
        # Ensure if parent directory exists, if not create it

        try:
            parent_dir = path.parent
            if not parent_dir.exists():
                parent_dir.mkdir(parents=True ,exist_ok=True)
                self._log_error(f"Created parent directory: {parent_dir}", "INFO")
                return True
        except Exception as e:
            self._log_error(f"Failed to create parent directory for {path}: {e}")
            return False
        
        
    def _safe_open(self, path: Path, mode: str = 'r', **kwargs):
        """
        Safely open a file with proper error handling and cleanup.        
        This is a context manager that ensures files are properly closed
        even if an error occurs.
        """
        class SafeFileOpener:
            def __init__(self, path, mode, kwargs):
                self.path = path
                self.mode = mode
                self.kwargs = kwargs
                self.file = None
            
            def __enter__(self):
                self.file = open(self.path, self.mode, **self.kwargs)
                return self.file
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if self.file:
                    self.file.close()
                return False
        
        return SafeFileOpener(path, mode, kwargs)



    def create_files(self, filepath: Union[str, Path], content: str = "", encoding: str = "utf-8",overwrite: bool = False) -> bool:
        
        # Create a new file with optional content
        try:
            path = self._resolve_path(filepath)

            if path.exists():
                if not overwrite:
                    raise FileExistsError(f"File {path} already exists")
                elif path.is_dir():
                    raise IsADirectoryError(f"File {path} is a directory, not a file")
                
            # Ensure parent directory exists
            self._ensure_parent_exists(path)

            # Create the file with content
            with self._safe_open(path, "w", encoding=encoding) as f:
                f.write(content)

            self._log_error(f"Created file: {path}", "INFO")
            return True
        
        except (FileExistsError, IsADirectoryError):
            raise
        except Exception as e:
            self._log_error(f"Failed to create file {filepath}: {e}")
            return False       
