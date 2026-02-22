"""
Directory Operations Module
Handles directory management operations
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Union, Optional

logger = logging.getLogger(__name__)


class DirectoryOperations:
    """Handles directory operations"""
    
    @staticmethod
    def create_directory(dirpath: Union[str, Path], parents: bool = True) -> bool:
        """
        Create a new directory
        
        Args:
            dirpath: Path where directory should be created
            parents: If True, create parent directories as needed
            
        Returns:
            True if successful, False otherwise
        """
        try:
            dirpath = Path(dirpath)
            dirpath.mkdir(parents=parents, exist_ok=True)
            logger.info(f"Directory created: {dirpath}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {dirpath}: {e}")
            return False
    
    @staticmethod
    def list_directory(dirpath: Union[str, Path], 
                    show_hidden: bool = False,
                    files_only: bool = False,
                    dirs_only: bool = False) -> Optional[List[Path]]:
        """
        List contents of a directory
        
        Args:
            dirpath: Path to directory to list
            show_hidden: If True, include hidden files
            files_only: If True, only return files
            dirs_only: If True, only return directories
            
        Returns:
            List of Path objects, None if error
        """
        try:
            dirpath = Path(dirpath)
            if not dirpath.exists():
                logger.error(f"Directory not found: {dirpath}")
                return None
            
            if not dirpath.is_dir():
                logger.error(f"Not a directory: {dirpath}")
                return None
            
            items = list(dirpath.iterdir())
            
            # Filter hidden files
            if not show_hidden:
                items = [item for item in items if not item.name.startswith('.')]
            
            # Filter by type
            if files_only:
                items = [item for item in items if item.is_file()]
            elif dirs_only:
                items = [item for item in items if item.is_dir()]
            
            # Sort: directories first, then files, alphabetically
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            logger.debug(f"Listed directory: {dirpath} ({len(items)} items)")
            return items
        except Exception as e:
            logger.error(f"Error listing directory {dirpath}: {e}")
            return None
    
    @staticmethod
    def delete_directory(dirpath: Union[str, Path], recursive: bool = False) -> bool:
        """
        Delete a directory
        
        Args:
            dirpath: Path to directory to delete
            recursive: If True, delete non-empty directories
            
        Returns:
            True if successful, False otherwise
        """
        try:
            dirpath = Path(dirpath)
            if not dirpath.exists():
                logger.error(f"Directory not found: {dirpath}")
                return False
            
            if not dirpath.is_dir():
                logger.error(f"Not a directory: {dirpath}")
                return False
            
            if recursive:
                shutil.rmtree(dirpath)
            else:
                dirpath.rmdir()
            
            logger.info(f"Directory deleted: {dirpath}")
            return True
        except Exception as e:
            logger.error(f"Error deleting directory {dirpath}: {e}")
            return False
    
    @staticmethod
    def copy_directory(source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Copy a directory to a new location
        
        Args:
            source: Source directory path
            destination: Destination directory path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                logger.error(f"Source directory not found: {source}")
                return False
            
            if not source.is_dir():
                logger.error(f"Source is not a directory: {source}")
                return False
            
            shutil.copytree(source, destination, dirs_exist_ok=True)
            logger.info(f"Directory copied: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"Error copying directory {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def move_directory(source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Move a directory to a new location
        
        Args:
            source: Source directory path
            destination: Destination directory path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                logger.error(f"Source directory not found: {source}")
                return False
            
            if not source.is_dir():
                logger.error(f"Source is not a directory: {source}")
                return False
            
            shutil.move(str(source), str(destination))
            logger.info(f"Directory moved: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"Error moving directory {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def get_directory_size(dirpath: Union[str, Path]) -> Optional[int]:
        """
        Calculate total size of a directory
        
        Args:
            dirpath: Path to directory
            
        Returns:
            Size in bytes, None if error
        """
        try:
            dirpath = Path(dirpath)
            if not dirpath.exists() or not dirpath.is_dir():
                logger.error(f"Invalid directory: {dirpath}")
                return None
            
            total_size = sum(
                f.stat().st_size 
                for f in dirpath.rglob('*') 
                if f.is_file()
            )
            
            logger.debug(f"Directory size calculated: {dirpath} = {total_size} bytes")
            return total_size
        except Exception as e:
            logger.error(f"Error calculating directory size {dirpath}: {e}")
            return None
    
    @staticmethod
    def is_empty(dirpath: Union[str, Path]) -> Optional[bool]:
        """
        Check if a directory is empty
        
        Args:
            dirpath: Path to directory
            
        Returns:
            True if empty, False if not, None if error
        """
        try:
            dirpath = Path(dirpath)
            if not dirpath.exists() or not dirpath.is_dir():
                logger.error(f"Invalid directory: {dirpath}")
                return None
            
            return not any(dirpath.iterdir())
        except Exception as e:
            logger.error(f"Error checking if directory is empty {dirpath}: {e}")
            return None
