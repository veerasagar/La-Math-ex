"""
Example usage of La-Math-ex package.

This script demonstrates the main functionality of the package including:
- Data downloading and processing
- InkML file handling
- Mathematical OCR with TrOCR
- Drawing interface creation
- Visualization capabilities
"""

import sys
import os

# Add the package to path for local development
sys.path.insert(0, '.')

from la_math_ex import (
    DataDownloader, 
    InkProcessor, 
    MathOCRModel, 
    InkVisualizer, 
    DrawingInterface
)
from la_math_ex.utils.config import config
from la_math_ex.utils.image_utils import ImageProcessor


def example_data_download():
    """Example: Download and explore dataset."""
    print("=== Data Download Example ===")
    
    # Initialize downloader
    downloader = DataDownloader(data_dir=config.data_dir)
    
    # Get dataset info
    info = DataDownloader.get_dataset_info()
    print("Available datasets:", info.keys())
    
    # Note: Uncomment to actually download (large file)
    # dataset_path = downloader.download_mathwriting_dataset()
    # print(f"Dataset downloaded to: {dataset_path}")
    
    # List contents (if dataset exists)
    contents = downloader.list_dataset_contents()
    if "error" not in contents:
        print("Dataset contents:", contents)


def example_inkml_processing():
    """Example: Process InkML files."""
    print("\n=== InkML Processing Example ===")
    
    print("InkML processing workflow:")
    print("1. ink = InkProcessor.read_inkml_file('path/to/file.inkml')")
    print("2. bbox = InkProcessor.get_bounding_box(ink)")
    print("3. normalized_ink = InkProcessor.normalize_ink(ink)")
    print("4. stroke_count = InkProcessor.stroke_count(ink)")


def example_drawing_interface():
    """Example: Create drawing interface."""
    print("\n=== Drawing Interface Example ===")
    
    # Create drawing interface
    interface = DrawingInterface(
        canvas_width=config.get('drawing.canvas_width'),
        canvas_height=config.get('drawing.canvas_height')
    )
    
    # Register save callback (for Colab)
    interface.register_save_callback()
    
    print("Drawing interface created. In Jupyter:")
    print("drawing_pad = interface.create_drawing_pad()")
    print("display(drawing_pad)")
    
    # Get interface info
    info = interface.get_canvas_info()
    print("Canvas configuration:", info)


def example_math_ocr():
    """Example: Mathematical OCR with TrOCR."""
    print("\n=== Mathematical OCR Example ===")
    
    print("Initializing Math OCR model...")
    print("Note: This will download the model on first use")
    
    print("OCR workflow:")
    print("1. model = MathOCRModel()")
    print("2. latex_text = model.predict_from_image('drawing.png')")
    print("3. print(f'Recognized LaTeX: {latex_text}')")


def example_visualization():
    """Example: Visualization capabilities."""
    print("\n=== Visualization Example ===")
    
    print("Visualization workflow:")
    print("1. fig = InkVisualizer.display_ink(ink)")
    print("2. fig = InkVisualizer.display_multiple_inks(ink_list)")
    print("3. fig = InkVisualizer.plot_stroke_statistics(ink_list)")
    print("4. InkVisualizer.save_visualization(fig, 'output.png')")


def example_image_processing():
    """Example: Image processing utilities."""
    print("\n=== Image Processing Example ===")
    
    print("Image processing capabilities:")
    print("- preprocess_for_ocr(): Prepare images for OCR")
    print("- enhance_contrast(): Improve image contrast")
    print("- binarize_image(): Convert to black and white")
    print("- crop_to_content(): Remove white space")
    print("- base64_to_image(): Convert base64 to PIL image")


def example_complete_workflow():
    """Example: Complete workflow from drawing to LaTeX."""
    print("\n=== Complete Workflow Example ===")
    
    print("Complete workflow:")
    print("1. Create drawing interface:")
    print("   interface = DrawingInterface()")
    print("   drawing_pad = interface.create_drawing_pad()")
    print("   display(drawing_pad)")
    print()
    print("2. Draw mathematical expression and save")
    print()
    print("3. Load and preprocess the saved image:")
    print("   image = interface.load_image_from_file('drawing.png')")
    print("   processed = ImageProcessor.preprocess_for_ocr(image)")
    print()
    print("4. Run OCR to get LaTeX:")
    print("   model = MathOCRModel()")
    print("   latex_result = model.predict_from_image(processed)")
    print()
    print("5. Display result:")
    print("   print(f'LaTeX: {latex_result}')")


def main():
    """Run all examples."""
    print("La-Math-ex Package Examples")
    print("=" * 40)
    
    # Create necessary directories
    config.create_directories()
    print(f"Created directories in: {config.data_dir}")
    
    # Run examples
    example_data_download()
    example_inkml_processing()
    example_drawing_interface()
    example_math_ocr()
    example_visualization()
    example_image_processing()
    example_complete_workflow()
    
    print("\n" + "=" * 40)
    print("Examples completed!")
    print("To use in Jupyter notebook, import modules and follow examples above.")


if __name__ == "__main__":
    main()