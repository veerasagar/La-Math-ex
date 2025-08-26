"""
La-Math-ex: A modular Python package for mathematical expression recognition
from handwritten and LaTeX sources.

This package provides tools for:
- Processing InkML files and handwritten mathematical expressions
- Converting handwritten math to LaTeX using TrOCR models
- Visualizing mathematical data and expressions
- Interactive drawing interfaces for math input
"""

__version__ = "1.0.0"
__author__ = "La-Math-ex Team"

# Import main components
from .data.ink_processor import InkProcessor, Ink
from .models.math_ocr import MathOCRModel
from .visualization.ink_visualizer import InkVisualizer
from .ui.drawing_interface import DrawingInterface
from .utils.data_downloader import DataDownloader

__all__ = [
    'InkProcessor',
    'Ink',
    'MathOCRModel',
    'InkVisualizer',
    'DrawingInterface',
    'DataDownloader'
]