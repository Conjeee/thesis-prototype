import sys
from pathlib import Path
from ultralytics import YOLO
from .config import Config


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


def pt_to_onnx(model_location: str = Config.MODEL_PATH):
    model = YOLO(model_location)
    model.export(format="onnx")
    
    
if __name__=="__main__":
    pt_to_onnx()