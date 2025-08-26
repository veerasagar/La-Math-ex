# La-Math-ex

A modular Python package for mathematical expression recognition from handwritten and LaTeX sources.

## Features

- **InkML Processing**: Read and process InkML files containing handwritten mathematical expressions
- **Mathematical OCR**: Convert handwritten math to LaTeX using TrOCR models
- **Interactive Drawing**: Create drawing interfaces for inputting mathematical expressions
- **Data Visualization**: Visualize ink data and mathematical expressions
- **Flexible Configuration**: Easy-to-use configuration system
- **Extensible Design**: Modular architecture for easy extension

## Installation

```bash
pip install la-math-ex
```

Or for development:

```bash
git clone https://github.com/veerasagar/La-Math-ex.git
cd La-Math-ex
pip install -e .
```

## Quick Start

### Basic Usage

```python
from la_math_ex import MathOCRModel, DrawingInterface

# Create a drawing interface
interface = DrawingInterface()
drawing_pad = interface.create_drawing_pad()

# Initialize OCR model
model = MathOCRModel()

# Convert drawing to LaTeX
latex_text = model.predict_from_image("drawing.png")
print(f"LaTeX: {latex_text}")
```

### Processing InkML Files

```python
from la_math_ex import InkProcessor, InkVisualizer

# Read InkML file
ink = InkProcessor.read_inkml_file("math_expression.inkml")

# Visualize the ink
fig = InkVisualizer.display_ink(ink)

# Get statistics
stroke_count = InkProcessor.stroke_count(ink)
point_count = InkProcessor.point_count(ink)
```

### Download Mathematical Datasets

```python
from la_math_ex import DataDownloader

# Download MathWriting dataset
downloader = DataDownloader()
dataset_path = downloader.download_mathwriting_dataset()
```

## Package Structure

```bash
la_math_ex/
├── __init__.py          # Main package imports
├── data/                # Data processing modules
│   ├── ink_processor.py # InkML file processing
│   └── __init__.py
├── models/              # Model modules
│   ├── math_ocr.py      # Mathematical OCR with TrOCR
│   └── __init__.py
├── ui/                  # User interface modules
│   ├── drawing_interface.py # Interactive drawing
│   └── __init__.py
├── utils/               # Utility modules
│   ├── data_downloader.py   # Dataset downloading
│   ├── image_utils.py       # Image processing
│   ├── config.py            # Configuration management
│   └── __init__.py
└── visualization/       # Visualization modules
    ├── ink_visualizer.py # Ink data visualization
    └── __init__.py
```

## Core Components

### InkProcessor

Handles reading and processing InkML files:

- Read InkML files with stroke and annotation data
- Normalize ink coordinates
- Calculate bounding boxes
- Get stroke and point statistics

### MathOCRModel

Mathematical OCR using TrOCR models:

- Convert handwritten math images to LaTeX
- Support for batch processing
- Confidence scoring
- Model evaluation utilities

### DrawingInterface

Interactive drawing capabilities:

- HTML5 canvas-based drawing pad
- Customizable brush settings
- Save drawings as images
- Google Colab integration

### InkVisualizer

Visualization tools for ink data:

- Display single and multiple inks
- Plot stroke statistics
- Visualize bounding boxes
- Save visualizations

### DataDownloader

Dataset management utilities:

- Download MathWriting dataset
- Extract and organize data
- List dataset contents
- Get sample files

## Requirements

- Python >= 3.8
- PyTorch >= 1.12.0
- Transformers >= 4.20.0
- Pillow >= 9.0.0
- NumPy >= 1.21.0
- Matplotlib >= 3.5.0

## Examples

See `example_usage.py` for comprehensive examples of all functionality.

Run the demo:

```bash
python example_usage.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{la_math_ex,
  title={La-Math-ex: Mathematical Expression Recognition Package},
  author={La-Math-ex Team},
  year={2024},
  url={https://github.com/veerasagar/La-Math-ex}
}
```
