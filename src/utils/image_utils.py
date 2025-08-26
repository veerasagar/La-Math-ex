"""
Image processing utilities for La-Math-ex.

This module provides common image processing functions for mathematical
expression recognition tasks.
"""

import numpy as np
from PIL import Image, ImageOps, ImageEnhance
from typing import Tuple, Union, Optional
import io
import base64


class ImageProcessor:
    """Utility class for image processing operations."""
    
    @staticmethod
    def preprocess_for_ocr(image: Image.Image,
                          target_size: Tuple[int, int] = (384, 384),
                          background_color: str = "white",
                          maintain_aspect: bool = True) -> Image.Image:
        """
        Preprocess image for OCR model input.
        
        Args:
            image: Input PIL image
            target_size: Target dimensions (width, height)
            background_color: Background color for padding
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Preprocessed PIL image
        """
        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        if maintain_aspect:
            # Calculate scaling factor
            scale = min(target_size[0] / image.width, target_size[1] / image.height)
            new_size = (int(image.width * scale), int(image.height * scale))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        else:
            image = image.resize(target_size, Image.Resampling.LANCZOS)
        
        # Create new image with background
        result = Image.new("RGB", target_size, background_color)
        
        # Center the image
        x_offset = (target_size[0] - image.width) // 2
        y_offset = (target_size[1] - image.height) // 2
        result.paste(image, (x_offset, y_offset))
        
        return result
    
    @staticmethod
    def enhance_contrast(image: Image.Image, factor: float = 1.5) -> Image.Image:
        """
        Enhance image contrast.
        
        Args:
            image: Input PIL image
            factor: Contrast enhancement factor (1.0 = no change)
            
        Returns:
            Enhanced PIL image
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def binarize_image(image: Image.Image, threshold: int = 128) -> Image.Image:
        """
        Convert image to binary (black and white).
        
        Args:
            image: Input PIL image
            threshold: Threshold value (0-255)
            
        Returns:
            Binary PIL image
        """
        # Convert to grayscale
        gray = image.convert("L")
        
        # Apply threshold
        binary = gray.point(lambda x: 255 if x > threshold else 0, mode="1")
        
        return binary.convert("RGB")
    
    @staticmethod
    def remove_noise(image: Image.Image, kernel_size: int = 3) -> Image.Image:
        """
        Simple noise removal using median filter approximation.
        
        Args:
            image: Input PIL image
            kernel_size: Size of the filter kernel
            
        Returns:
            Filtered PIL image
        """
        # Convert to numpy array
        img_array = np.array(image)
        
        # Simple median filter approximation
        from scipy import ndimage
        filtered = ndimage.median_filter(img_array, size=kernel_size)
        
        return Image.fromarray(filtered)
    
    @staticmethod
    def crop_to_content(image: Image.Image, margin: int = 10) -> Image.Image:
        """
        Crop image to the bounding box of non-white content.
        
        Args:
            image: Input PIL image
            margin: Additional margin around content
            
        Returns:
            Cropped PIL image
        """
        # Convert to grayscale for analysis
        gray = image.convert("L")
        
        # Find bounding box of non-white pixels
        bbox = ImageOps.invert(gray).getbbox()
        
        if bbox is None:
            return image  # No content found
        
        # Add margin
        left, top, right, bottom = bbox
        left = max(0, left - margin)
        top = max(0, top - margin)
        right = min(image.width, right + margin)
        bottom = min(image.height, bottom + margin)
        
        return image.crop((left, top, right, bottom))
    
    @staticmethod
    def base64_to_image(base64_string: str) -> Image.Image:
        """
        Convert base64 string to PIL image.
        
        Args:
            base64_string: Base64 encoded image data
            
        Returns:
            PIL image
        """
        if "," in base64_string:
            header, encoded = base64_string.split(",", 1)
        else:
            encoded = base64_string
        
        decoded_data = base64.b64decode(encoded)
        return Image.open(io.BytesIO(decoded_data))
    
    @staticmethod
    def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
        """
        Convert PIL image to base64 string.
        
        Args:
            image: PIL image
            format: Image format (PNG, JPEG, etc.)
            
        Returns:
            Base64 encoded string
        """
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        encoded_string = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/{format.lower()};base64,{encoded_string}"
    
    @staticmethod
    def resize_with_padding(image: Image.Image, 
                           target_size: Tuple[int, int],
                           fill_color: str = "white") -> Image.Image:
        """
        Resize image to exact size with padding.
        
        Args:
            image: Input PIL image
            target_size: Target dimensions (width, height)
            fill_color: Color for padding
            
        Returns:
            Resized and padded PIL image
        """
        # Calculate scaling factor to fit within target size
        scale = min(target_size[0] / image.width, target_size[1] / image.height)
        new_size = (int(image.width * scale), int(image.height * scale))
        
        # Resize image
        resized = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Create padded image
        padded = Image.new("RGB", target_size, fill_color)
        x_offset = (target_size[0] - new_size[0]) // 2
        y_offset = (target_size[1] - new_size[1]) // 2
        padded.paste(resized, (x_offset, y_offset))
        
        return padded