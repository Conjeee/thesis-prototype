import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    """

    
    Args:
        relatice_path (str): _description_

    Returns:
        Path: _description_
    """
    
    try:
        base_path = Path(sys._MEIPASS)
    
    except AttributeError:
        base_path = Path(__file__).resolve().parent.parent
        
    return base_path/relative_path