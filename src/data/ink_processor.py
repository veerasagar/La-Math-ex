"""
InkML file processing module for La-Math-ex.

This module handles the reading, parsing, and processing of InkML files
containing handwritten mathematical expressions.
"""

import dataclasses
import numpy as np
from xml.etree import ElementTree
from typing import List, Dict, Optional
import os


@dataclasses.dataclass
class Ink:
    """
    Represents a single ink, as read from an InkML file.
    
    Attributes:
        strokes: List of stroke arrays, each with shape (3, number of points)
                where dimensions are (x, y, timestamp)
        annotations: Metadata present in the InkML file
    """
    # Every stroke in the ink.
    # Each stroke array has shape (3, number of points), where the first
    # dimensions are (x, y, timestamp), in that order.
    strokes: List[np.ndarray]
    # Metadata present in the InkML.
    annotations: Dict[str, str]


class InkProcessor:
    """
    Processor class for handling InkML files and ink data.
    """
    
    @staticmethod
    def read_inkml_file(filename: str) -> Ink:
        """
        Simple reader for MathWriting's InkML files.
        
        Args:
            filename: Path to the InkML file
            
        Returns:
            Ink object containing strokes and annotations
            
        Raises:
            FileNotFoundError: If the InkML file doesn't exist
            ValueError: If the file format is invalid
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"InkML file not found: {filename}")
            
        try:
            with open(filename, "r") as f:
                root = ElementTree.fromstring(f.read())
        except ElementTree.ParseError as e:
            raise ValueError(f"Invalid InkML format: {e}")

        strokes = []
        annotations = {}

        for element in root:
            tag_name = element.tag.removeprefix('{http://www.w3.org/2003/InkML}')
            
            if tag_name == 'annotation':
                annotations[element.attrib.get('type')] = element.text

            elif tag_name == 'trace':
                points = element.text.split(',')
                stroke_x, stroke_y, stroke_t = [], [], []
                
                for point in points:
                    try:
                        x, y, t = point.split(' ')
                        stroke_x.append(float(x))
                        stroke_y.append(float(y))
                        stroke_t.append(float(t))
                    except ValueError:
                        continue  # Skip malformed points
                        
                if stroke_x and stroke_y and stroke_t:  # Only add non-empty strokes
                    strokes.append(np.array((stroke_x, stroke_y, stroke_t)))

        return Ink(strokes=strokes, annotations=annotations)
    
    @staticmethod
    def get_bounding_box(ink: Ink) -> Optional[tuple]:
        """
        Calculate the bounding box of all strokes in the ink.
        
        Args:
            ink: Ink object
            
        Returns:
            Tuple of (min_x, min_y, max_x, max_y) or None if no strokes
        """
        if not ink.strokes:
            return None
            
        all_x = []
        all_y = []
        
        for stroke in ink.strokes:
            all_x.extend(stroke[0])  # x coordinates
            all_y.extend(stroke[1])  # y coordinates
            
        return (min(all_x), min(all_y), max(all_x), max(all_y))
    
    @staticmethod
    def normalize_ink(ink: Ink, target_size: tuple = (256, 256)) -> Ink:
        """
        Normalize ink coordinates to fit within target size.
        
        Args:
            ink: Input ink object
            target_size: Target (width, height) for normalization
            
        Returns:
            New Ink object with normalized coordinates
        """
        if not ink.strokes:
            return ink
            
        bbox = InkProcessor.get_bounding_box(ink)
        if bbox is None:
            return ink
            
        min_x, min_y, max_x, max_y = bbox
        width = max_x - min_x
        height = max_y - min_y
        
        if width == 0 or height == 0:
            return ink
            
        scale_x = target_size[0] / width
        scale_y = target_size[1] / height
        scale = min(scale_x, scale_y)  # Maintain aspect ratio
        
        normalized_strokes = []
        for stroke in ink.strokes:
            normalized_x = (stroke[0] - min_x) * scale
            normalized_y = (stroke[1] - min_y) * scale
            normalized_strokes.append(np.array([normalized_x, normalized_y, stroke[2]]))
            
        return Ink(strokes=normalized_strokes, annotations=ink.annotations.copy())
    
    @staticmethod
    def stroke_count(ink: Ink) -> int:
        """Get the number of strokes in the ink."""
        return len(ink.strokes)
    
    @staticmethod
    def point_count(ink: Ink) -> int:
        """Get the total number of points across all strokes."""
        return sum(stroke.shape[1] for stroke in ink.strokes)