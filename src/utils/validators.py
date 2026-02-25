""" VALIDATORS MODULE
    INPUT VALIDATION FUNCTIONS
    """

import re
import logging
from pathlib import Path
from typing import Union, List

logger = logging.getLogger(__name__)

class Validators:

    @staticmethod
    def validate_path(path: Union[str, Path], must_exist: bool=False) -> bool:
        """ 
        Validate file/directory path
        Args:
            path: Path to validate
            must_exist: If True, path must exist
        Return:
            True if valid otherwise False"""
        try:
            path = Path(path)

            if must_exist and not path:
                logger.error("Path does not exist: {path}")
                return False

            invalid_charaters = ['<', '>', '|', '\0']
            if any(char in str(path) for char in invalid_charaters):
                logger.error("Path contain invalid characters: {path}")
                return False
            
            return True
        
        except Exception as e:
            logger.error("Invalid path: {e}")
            return False
        
    @staticmethod
    def validate_filename(filename: str) -> bool:
        """ Validate filename
            Args: 
                filename: Filename to validate
            Return:
                True if valid otherwise False"""

        if not filename:
            logger.error("Filename cannot be empty")
            return False
        # Checks for invalid charaters in filename
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '\0']
        if any(char in str(filename) for char in invalid_chars):
            logger.error("Invalid fiulename")
            return False
            
        # Check for reserved name on Windows
        reserved_names = [
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        ]

        name_without_ext = filename.rsplit(".", 1)[0].upper()
        if name_without_ext in invalid_chars:
            logger.error("Filename is a reserved name: {filename}")
            return False
            
        return True
    
    @staticmethod
    def validate_extension(ext: str, valid_extensions: List[str]=None) -> bool:
        """
        Validate file extension
        
        Args:
            extension: Extension to validate
            valid_extensions: List of valid extensions (optional)
            
        Returns:
            True if valid, False otherwise
        """
        if not ext:
            return True

        if not ext.startswith("."):
            ext = f".{ext}"

        if valid_extensions is not None:
            valid_extensions = [extension if extension.startwith(".") else f".{extension}" for extension in valid_extensions]

            if ext.lower() not in [extension.lower() for extension in valid_extensions]:
                logger.error(f"Invalid extension: {ext}")
                return False
            
        return True

    @staticmethod
    def validate_size(size: int, min_size: int = None, max_size: int = None) -> bool:
        """
        Validate file size
        
        Args:
            size: Size in bytes
            min_size: Minimum size in bytes
            max_size: Maximum size in bytes
            
        Returns:
            True if valid, False otherwise
        """
        if size < 0:
            logger.error("Size cannot be negative")
            return False
        
        if min_size is not None and size < min_size:
            logger.error(f"Size {size} is below minimum {min_size}")
            return False
        
        if max_size is not None and size > max_size:
            logger.error(f"Size {size} exceeds maximum {max_size}")
            return False
        
        return True
    
    @staticmethod
    def validate_permissions(permissions: str) -> bool:
        """
        Validate permission string
        
        Args:
            permissions: Permission string (e.g., 'rwxr-xr-x')
            
        Returns:
            True if valid, False otherwise
        """
        if len(permissions) != 9:
            logger.error("Permission string must be 9 characters")
            return False
        
        valid_chars = set('rwx-')
        if not all(char in valid_chars for char in permissions):
            logger.error("Permission string contains invalid characters")
            return False
        
        return True
    
    @staticmethod
    def validate_regex_pattern(pattern: str) -> bool:
        """
        Validate regex pattern
        
        Args:
            pattern: Regex pattern to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            re.compile(pattern)
            return True
        except re.error as e:
            logger.error(f"Invalid regex pattern: {e}")
            return False
        
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename by removing invalid characters
        
        Args:
            filename: Filename to sanitize
            
        Returns:
            Sanitized filename
        """
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

        for char in invalid_chars:
            filename = filename.replace(char, "_")
        
        filename = filename.strip(". ")

        if not filename:
            filename = "unnamed"
        return filename
        
    @staticmethod
    def validate_archive_format(format_str: str) -> bool:
        """
        Validate archive format
        
        Args:
            format_str: Archive format (zip, tar, tar.gz, tar.bz2, tar.xz)
            
        Returns:
            True if valid, False otherwise
        """
        valid_formats = ['zip', 'tar', 'tar.gz', 'tar.bz2', 'tar.xz']
        
        if format_str.lower() not in valid_formats:
            logger.error(f"Invalid archive format: {format_str}")
            return False
        
        return True
    
    @staticmethod
    def validate_hash_algorithm(algorithm: str) -> bool:
        """
        Validate hash algorithm
        
        Args:
            algorithm: Hash algorithm name
            
        Returns:
            True if valid, False otherwise
        """
        valid_algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        
        if algorithm.lower() not in valid_algorithms:
            logger.error(f"Invalid hash algorithm: {algorithm}")
            return False
        
        return True