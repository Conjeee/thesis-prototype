from ultralytics import YOLO
from src.config import Config

def pt_to_onnx(model_location: str = Config.MODEL_PATH):
    model = YOLO(model_location)
    model.export(format="onnx")
    
    
if __name__=="__main__":
    pt_to_onnx()