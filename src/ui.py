import gradio as gr


def create_ui(interference_callback):
    """
    Builds the gradio interface. 
    
    Args:
        interference_callback (_type_): Function that will handle the ONNX processing.
    """
    
    with gr.Blocks(title="Model UI", theme=gr.themes.Soft()) as app:
        gr.Markdown("# Model UI")
        gr.Markdown("Upload an image below to detect objects.")
        
        with gr.Row():
            
            # Left Column
            with gr.Column():
                input_image = gr.Image(
                    type="numpy",
                    label="1. Drag and drop an image here (JPG/PNG)"
                )
                detect_button = gr.Button("Detect Objects", variant="primary")
                
            # Right Column
            with gr.Column():
                
                output_image = gr.AnnotatedImage(
                    label="2. Detection Results",
                    color_map={"Object": "#ff9900"}
                )
                
        detect_button.click(
            fn=interference_callback,
            inputs=input_image,
            outputs=output_image
        )
        
    return app