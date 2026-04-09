import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    """
    Safely locate a file path.
    
    Args:
        relative_path (str):  Path of the file relative to the base file.

    Returns:
        Path: The absolute path of the file.
    """
    
    try:
        base_path = Path(sys._MEIPASS)
    
    except AttributeError:
        base_path = Path(__file__).resolve().parent.parent
        
    return base_path/relative_path
