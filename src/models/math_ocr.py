"""
Mathematical OCR model module for La-Math-ex.

This module provides functionality to convert handwritten mathematical
expressions to LaTeX using TrOCR models.
"""

import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import numpy as np
from typing import Union, List, Optional
import io
import base64


class MathOCRModel:
    """
    Mathematical OCR model using TrOCR for handwritten math recognition.
    """
    
    DEFAULT_MODEL = 'fhswf/TrOCR_Math_handwritten'
    
    def __init__(self, 
                 model_name: str = None,
                 device: str = None):
        """
        Initialize the Math OCR model.
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to use ('cuda', 'cpu', or None for auto)
        """
        self.model_name = model_name or self.DEFAULT_MODEL
        
        # Determine device
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        self.processor = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the TrOCR processor and model."""
        print(f"Loading TrOCR model: {self.model_name}")
        print(f"Using device: {self.device}")
        
        try:
            self.processor = TrOCRProcessor.from_pretrained(self.model_name)
            self.model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            print("Model loaded successfully")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def predict_from_image(self, 
                          image: Union[Image.Image, np.ndarray, str],
                          return_confidence: bool = False) -> Union[str, tuple]:
        """
        Convert a handwritten math image to LaTeX.
        
        Args:
            image: PIL Image, numpy array, or file path
            return_confidence: Whether to return confidence scores
            
        Returns:
            LaTeX string, or (LaTeX string, confidence) if return_confidence=True
        """
        # Handle different image input types
        if isinstance(image, str):
            # File path
            pil_image = Image.open(image).convert("RGB")
        elif isinstance(image, np.ndarray):
            # Numpy array
            pil_image = Image.fromarray(image).convert("RGB")
        elif isinstance(image, Image.Image):
            # PIL Image
            pil_image = image.convert("RGB")
        else:
            raise ValueError(f"Unsupported image type: {type(image)}")
        
        # Process image
        pixel_values = self.processor(
            images=pil_image, 
            return_tensors="pt"
        ).pixel_values.to(self.device)
        
        # Generate prediction
        with torch.no_grad():
            if return_confidence:
                generated_ids = self.model.generate(
                    pixel_values, 
                    return_dict_in_generate=True,
                    output_scores=True
                )
                generated_text = self.processor.batch_decode(
                    generated_ids.sequences, 
                    skip_special_tokens=True
                )[0]
                
                # Calculate confidence (simplified approach)
                scores = generated_ids.scores
                if scores:
                    confidence = torch.mean(torch.stack([
                        torch.max(torch.softmax(score, dim=-1)) 
                        for score in scores
                    ])).item()
                else:
                    confidence = 0.0
                
                return generated_text, confidence
            else:
                generated_ids = self.model.generate(pixel_values)
                generated_text = self.processor.batch_decode(
                    generated_ids, 
                    skip_special_tokens=True
                )[0]
                return generated_text
    
    def predict_batch(self, 
                     images: List[Union[Image.Image, np.ndarray, str]],
                     batch_size: int = 4) -> List[str]:
        """
        Process multiple images in batches.
        
        Args:
            images: List of images to process
            batch_size: Number of images to process at once
            
        Returns:
            List of LaTeX strings
        """
        results = []
        
        for i in range(0, len(images), batch_size):
            batch = images[i:i + batch_size]
            batch_results = []
            
            for image in batch:
                try:
                    result = self.predict_from_image(image)
                    batch_results.append(result)
                except Exception as e:
                    print(f"Error processing image {i}: {e}")
                    batch_results.append("")
            
            results.extend(batch_results)
        
        return results
    
    def predict_from_base64(self, base64_data: str) -> str:
        """
        Convert base64 encoded image to LaTeX.
        
        Args:
            base64_data: Base64 encoded image data
            
        Returns:
            LaTeX string
        """
        # Remove header if present
        if "," in base64_data:
            header, encoded = base64_data.split(",", 1)
        else:
            encoded = base64_data
        
        # Decode base64 data
        decoded_data = base64.b64decode(encoded)
        
        # Create PIL image
        image = Image.open(io.BytesIO(decoded_data))
        
        return self.predict_from_image(image)
    
    def evaluate_accuracy(self, 
                         test_images: List[Union[Image.Image, str]],
                         ground_truth: List[str]) -> dict:
        """
        Evaluate model accuracy on test data.
        
        Args:
            test_images: List of test images
            ground_truth: List of ground truth LaTeX strings
            
        Returns:
            Dictionary with evaluation metrics
        """
        if len(test_images) != len(ground_truth):
            raise ValueError("Number of images and ground truth labels must match")
        
        predictions = self.predict_batch(test_images)
        
        # Calculate exact match accuracy
        exact_matches = sum(1 for pred, gt in zip(predictions, ground_truth) 
                          if pred.strip() == gt.strip())
        accuracy = exact_matches / len(predictions)
        
        # Calculate character-level accuracy (simplified)
        char_correct = 0
        total_chars = 0
        
        for pred, gt in zip(predictions, ground_truth):
            pred_clean = pred.strip()
            gt_clean = gt.strip()
            
            # Simple character matching
            for p, g in zip(pred_clean, gt_clean):
                if p == g:
                    char_correct += 1
                total_chars += 1
            
            # Account for length differences
            total_chars += abs(len(pred_clean) - len(gt_clean))
        
        char_accuracy = char_correct / total_chars if total_chars > 0 else 0
        
        return {
            "exact_match_accuracy": accuracy,
            "character_accuracy": char_accuracy,
            "total_samples": len(predictions),
            "exact_matches": exact_matches
        }
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "processor_class": type(self.processor).__name__,
            "model_class": type(self.model).__name__,
            "model_loaded": self.model is not None
        }
    
    def __repr__(self) -> str:
        """String representation of the model."""
        return f"MathOCRModel(model='{self.model_name}', device='{self.device}')"