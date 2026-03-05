import gradio as gr
from .inference import TrashDetector

def build_ui(detector: TrashDetector) -> gr.Blocks:
    """
    Creates the UI.

    Args:
        detector (TrashDetector): Logic from the main inference logic.

    Returns:
        gr.Blocks: Gradio block containing the frontend.
    """
    
    with gr.Blocks(title="Trash Object Detection", theme=gr.themes.Soft()) as app:
        gr.Markdown("Local Trash Object Detection")
        gr.Markdown("Upload an image to detect trash")
        
        with gr.Row():
            with gr.Column():
                input_image = gr.Image(type="numpy", label="Upload Image (JPG/PNG)")
                
                with gr.Accordion("Advanved settings", open=False):
                    conf_slider = gr.Slider(minimum=0.1, maximum=1.0, value=.5, label="Confidence Threshold")
                    iou_slider = gr.Slider(minimum=0.1, maximum=1.0, value=.4, label="IOU Threshold")
                    
                detect_btn = gr.Button("Detect Trash", variant="primary")
                
            with gr.Column():
                output_image = gr.AnnotatedImage(label="Detection Results")
                
            
            def process_image(img, conf, iou):
                if img is None:
                    return None
                
                image, annotations = detector.predict(img, conf_threshold=conf, iou_threshold=iou)
                return (image, annotations)
            
            detect_btn.click(
                fn=process_image,
                inputs=[input_image, conf_slider, iou_slider],
                outputs=[output_image]
            )
            
        return app