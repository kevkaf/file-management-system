"""
Helper Utilities Module
General utility functions
"""

import logging
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
import json
import shutil

def setup_logging(log_level: str="INFO", log_file: str=None):
    """ 
    Setup Logging configurations

    Args: 
        log_level: logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional Log file path
    """

    # Create logs directory if it does not exists
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Timestamp to default logs file
    if log_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"file_management_{timestamp}.log"


    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers= [
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def load_config(config_path: Path=None) -> Dict[str, Any]:
    """ 
    Load Configuration from a JSON file
    
    Args: 
        config_path: Path to configuration file
    Return: 
        Configuration Dictionary """
    
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "settings.json"

    try:
        if config_path.exists():
            with open(config_path, "r") as f:
                return json.load(f)
        else:
            # default configuration
            return {
                "default_directory": str(Path.home()),
                "show_hidden_files": False,
                "log_level": "INFO",
                "max_file_size_display": 10485760,
                "date_format": '%Y-%m-%d %H:%M:%S'
            }
        
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return {}
    

def save_config(config: Dict[str, Any], config_path: Path=None) -> bool:
    """ Save configuration to a JSON file
    Args: 
        config: Configuration Dictionary
        config_path: Path to configuration file
    returns: 
        True if successful False otherwise
    """

    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "config.json"
    try:
        config_path.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config_path, f, indent=4)
        logging.info(f"Configuration saved to {config_path}")
        return True
    except Exception as e:
        logging.error(f"Error saving configuration: {e}")
        return False
    
def format_size(size_bytes: int) -> str:
    """ Format bytes to human readable size
    Args:
        size_bytes: size in bytes
    return: 
        Formatted size string"""
    
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes} {unit}"

def format_timestamp(timestamp: float, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Format timestamp to readable string
    
    Args:
        timestamp: Unix timestamp
        format_str: Date format string
        
    Returns:
        Formatted date string
    """
    return datetime.fromtimestamp(timestamp).strftime(format_str)

def confirm_action(prompt: str="Are you sure?", default: bool=False) -> True:
    """
    Ask user for confirmation
    
    Args:
        prompt: Confirmation prompt
        default: Default response if user just presses Enter
        
    Returns:
        True if confirmed, False otherwise
    """
    default_str = "[Y/n]" if default else "[y/N]"
    response = input(f"{prompt} {default_str}").strip().lower()

    if not response:
        return response
        
    return response in ["y", "yes"]

def truncate_string(text: str, max_length: int=50, suffix: str="...") -> str:
    """
    Truncate string to maximum length
    
    Args:
        text: String to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= 50:
        return text
    return text[:max_length - len(suffix)] + suffix

def get_terminal_width() -> int:
    """
    Get terminal width
    
    Returns:
        Terminal width in characters
    """
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80
    
def print_separator(char: str = '-', width: int = None):
    """
    Print a separator line
    
    Args:
        char: Character to use for separator
        width: Width of separator (default: terminal width)
    """
    if width is None:
        width = get_terminal_width()
    print(char * width)

def print_header(text: str, char: str = '='):
    """
    Print a formatted header
    
    Args:
        text: Header text
        char: Character to use for border
    """
    width = get_terminal_width()
    print_separator(char, width)
    print(text.center(width))
    print_separator(char, width)
