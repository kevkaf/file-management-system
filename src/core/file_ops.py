"""
Core File Operations Module
Handles basic CRUD operations for files
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional, Union

logger = logging.getLogger(__name__)


class FileOperations:
    """Handles basic file CRUD operations"""
    
    @staticmethod
    def create_file(filepath: Union[str, Path], content: str = "") -> bool:
        """
        Create a new file with optional content
        
        Args:
            filepath: Path where file should be created
            content: Optional initial content for the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"File created: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error creating file {filepath}: {e}")
            return False
    
    @staticmethod
    def read_file(filepath: Union[str, Path], binary: bool = False) -> Optional[Union[str, bytes]]:
        """ 
        Read file contents
        
        Args:
            filepath: Path to file to read
            binary: If True, read in binary mode
            
        Returns:
            File contents as string or bytes, None if error
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return None
            
            mode = 'rb' if binary else 'r'
            encoding = None if binary else 'utf-8'
            
            with open(filepath, mode, encoding=encoding) as f:
                content = f.read()
            
            logger.debug(f"File read: {filepath}")
            return content
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            return None
    
    @staticmethod
    def update_file(filepath: Union[str, Path], content: str, append: bool = False) -> bool:
        """
        Update file contents
        
        Args:
            filepath: Path to file to update
            content: New content to write
            append: If True, append instead of overwrite
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return False
            
            mode = 'a' if append else 'w'
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)
            
            action = "appended to" if append else "updated"
            logger.info(f"File {action}: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error updating file {filepath}: {e}")
            return False
    
    @staticmethod
    def delete_file(filepath: Union[str, Path]) -> bool:
        """
        Delete a file
        
        Args:
            filepath: Path to file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return False
            
            if filepath.is_dir():
                logger.error(f"Cannot delete directory with delete_file: {filepath}")
                return False
            
            filepath.unlink()
            logger.info(f"File deleted: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file {filepath}: {e}")
            return False
    
    @staticmethod
    def copy_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Copy a file to a new location
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                logger.error(f"Source file not found: {source}")
                return False
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            
            logger.info(f"File copied: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"Error copying file {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def move_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Move a file to a new location
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                logger.error(f"Source file not found: {source}")
                return False
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            
            logger.info(f"File moved: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"Error moving file {source} to {destination}: {e}")
            return False
    
    @staticmethod
    def rename_file(filepath: Union[str, Path], new_name: str) -> bool:
        """
        Rename a file
        
        Args:
            filepath: Path to file to rename
            new_name: New name for the file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                logger.error(f"File not found: {filepath}")
                return False
            
            new_path = filepath.parent / new_name
            filepath.rename(new_path)
            
            logger.info(f"File renamed: {filepath} -> {new_path}")
            return True
        except Exception as e:
            logger.error(f"Error renaming file {filepath}: {e}")
            return False
