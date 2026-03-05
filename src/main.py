import multiprocessing
import sys
from .inference import TrashDetector
from .ui import build_ui


def main():
    multiprocessing.freeze_support()
    
    print("Loading custom thesis YOLO model via ONNX Runtime...")
    try:
        detector = TrashDetector()
    
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)
        
    print("Building local user interface...")
    app = build_ui(detector)
    
    print("starting local server... Opening your web browser.")
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        prevent_thread_lock=False,
        quiet=True
    )
    
if __name__ == "__main__":
    main()