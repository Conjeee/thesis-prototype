import cv2
import json
import numpy as np
import onnxruntime as ort
from typing import Tuple, List
from src import get_resource_path

class TrashDetector:
    def __init__(self, model_name: str = "thesis_model.onnx", labels_name: str = "class_labels.json"):
        """
        Initializes the path, loads the labels, starts the ONNX session, and extracts model metadata

        Args:
            modelname (str, optional): _description_. Defaults to "thesis_model.onnx".
            labels_name (str, optional): _description_. Defaults to "class_labels.json".
        """
        
        # Path 
        model_path = get_resource_path(f"models/{model_name}")
        labels_path = get_resource_path(f"models/{labels_name}")
        
        # Label
        with open(labels_path, "r") as f:
            self.classes = json.load(f)
        
        # ONNX session
        self.session = ort.InferenceSession(
            str(model_path),
            providers=['CPUExecutionProvider']
        )
        
        # Metadata
        model_inputs = self.session.get_inputs()
        self.input_name = model_inputs[0].name
        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]
        
        
    def _preprocess(self, image: np.ndarray) -> Tuple[np.ndarray, float, float]:
        """
        Private function that gets the scaling factor, resizes and normalizes input image, and transposes the input image

        Args:
            image (np.ndarray): Input image

        Returns:
            Tuple[np.ndarray, float, float]: input_tensor, x_factor, y_factor
        """
        original_height, original_width = image.shape[:2]
        
        # Scaling factor
        x_factor = original_width / self.input_width
        y_factor = original_height / self.input_height

        # Resize and Normalize
        input_img = cv2.resize(image, (self.input_width, self.input_height))
        input_img = input_img / 255.0
        
        # Transposing channel for OpenCV to Pytorch/ONNX compatibility
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)
        
        return input_tensor, x_factor, y_factor
    
    def predict(self, image: np.ndarray, conf_threshold: float = 0.5, iou_threshold = 0.4) -> Tuple[np.ndarray, List[Tuple[Tuple[int, int, int, int], str]]]:
        """
        Main logic of the inference
        
        Args:
            image (np.ndarray): Input image
            conf_threshold (float, optional): Minimum percent of confidence to show prediction. Defaults to 0.5.
            iou_threshold (float, optional): Minimum percent of intersection/union to show box. Defaults to 0.4.

        Returns:
            Tuple[np.ndarray, List[Tuple[Tuple[int, int, int, int], str]]]: _description_
        """
        # Preprocess
        input_tensor, x_factor, y_factor = self._preprocess(image)
        
        # Model Inference
        outputs = self.session.run(None, {self.input_name: input_tensor})
        
        # Removes unnecessary information and flips it
        predictions = np.squeeze(outputs[0]).T
        
        boxes = []
        scores = []
        class_ids = []
        
        # Filters out low confidence class predictions
        for row in predictions:
            classes_scores = row[4:]
            class_id = np.argmax(classes_scores)
            score = classes_scores[class_id]
            
            if score > conf_threshold:
                cx, cy, w, h = row[0], row[1], row[2], row[3]
                
                left = int((cx - w / 2) * x_factor)
                top = int((cy - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                
                boxes.append([left, top, width, height])
                scores.append(float(score))
                class_ids.append(class_id)
        
        # Filters out boxes with low confidence
        indices = cv2.dnn.NMSBoxes(boxes, scores, conf_threshold, iou_threshold)
        annotations = []
        
        if len(indices) > 0:
            for i in indices.flatten():
                box = boxes[i]
                left, top, width, height = box[0], box[1], box[2], box[3]
                
                x1, y1 = left, top
                x2, y2 = left + width, top + height
                
                label_name = self.classes.get(str(class_ids[i]), f"Class {class_ids[i]}")
                formatted_label = f"{label_name} ({scores[i]:.2f})"
                annotations.append(((x1, y1, x2,y2), formatted_label))
                
        return image, annotations