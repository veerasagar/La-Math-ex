"""
Drawing interface module for La-Math-ex.

This module provides interactive drawing capabilities for inputting
handwritten mathematical expressions.
"""

import base64
from IPython.display import display, HTML
from PIL import Image
import io
from typing import Optional, Callable
import os


class DrawingInterface:
    """
    Interactive drawing interface for mathematical expression input.
    """
    
    def __init__(self, 
                 canvas_width: int = 800,
                 canvas_height: int = 400,
                 background_color: str = "white",
                 default_brush_color: str = "black",
                 default_brush_size: int = 3):
        """
        Initialize the drawing interface.
        
        Args:
            canvas_width: Width of the drawing canvas
            canvas_height: Height of the drawing canvas
            background_color: Background color of the canvas
            default_brush_color: Default brush color
            default_brush_size: Default brush size
        """
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.background_color = background_color
        self.default_brush_color = default_brush_color
        self.default_brush_size = default_brush_size
        self.callback_registered = False
    
    def create_drawing_pad(self, 
                          title: str = "Mathematical Expression Drawing Pad",
                          enable_color_picker: bool = True,
                          enable_size_slider: bool = True) -> HTML:
        """
        Create an interactive drawing pad.
        
        Args:
            title: Title for the drawing pad
            enable_color_picker: Whether to show color picker
            enable_size_slider: Whether to show brush size slider
            
        Returns:
            HTML object for display in Jupyter notebooks
        """
        # Color picker HTML
        color_picker_html = f"""
            Color:
            <input type="color" id="brushColor" value="{self.default_brush_color}">
        """ if enable_color_picker else ""
        
        # Size slider HTML
        size_slider_html = f"""
            Size:
            <input type="range" id="brushSize" min="1" max="20" value="{self.default_brush_size}">
        """ if enable_size_slider else ""
        
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                #drawingCanvas {{
                    border: 2px solid #333;
                    cursor: crosshair;
                    background-color: {self.background_color};
                }}
                .controls {{
                    margin: 10px 0;
                    padding: 10px;
                    background: #f0f0f0;
                    border-radius: 5px;
                }}
                .controls button {{
                    margin: 5px;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 3px;
                    cursor: pointer;
                    font-size: 14px;
                }}
                .controls button:hover {{
                    opacity: 0.8;
                }}
                #clearBtn {{ background: #ff4444; color: white; }}
                #saveBtn {{ background: #4444ff; color: white; }}
                #undoBtn {{ background: #44ff44; color: black; }}
            </style>
        </head>
        <body>
            <h3>{title}</h3>
            <canvas id="drawingCanvas" width="{self.canvas_width}" height="{self.canvas_height}"></canvas>
            <div class="controls">
                {color_picker_html}
                {size_slider_html}
                <button id="clearBtn" onclick="clearCanvas()">Clear</button>
                <button id="undoBtn" onclick="undoLast()">Undo</button>
                <button id="saveBtn" onclick="saveDrawing()">Save Drawing</button>
            </div>

            <script>
                const canvas = document.getElementById('drawingCanvas');
                const ctx = canvas.getContext('2d');
                let isDrawing = false;
                let strokes = [];
                let currentStroke = [];

                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';

                canvas.addEventListener('mousedown', startDrawing);
                canvas.addEventListener('mousemove', draw);
                canvas.addEventListener('mouseup', stopDrawing);
                canvas.addEventListener('mouseout', stopDrawing);

                function startDrawing(e) {{
                    isDrawing = true;
                    currentStroke = [];
                    const rect = canvas.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    ctx.beginPath();
                    ctx.moveTo(x, y);
                    currentStroke.push({{x: x, y: y}});
                }}

                function draw(e) {{
                    if (!isDrawing) return;
                    
                    const rect = canvas.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    
                    const colorPicker = document.getElementById('brushColor');
                    const sizePicker = document.getElementById('brushSize');
                    
                    if (colorPicker) ctx.strokeStyle = colorPicker.value;
                    if (sizePicker) ctx.lineWidth = sizePicker.value;
                    
                    ctx.lineTo(x, y);
                    ctx.stroke();
                    
                    currentStroke.push({{x: x, y: y}});
                }}

                function stopDrawing() {{
                    if (isDrawing && currentStroke.length > 0) {{
                        strokes.push([...currentStroke]);
                    }}
                    isDrawing = false;
                }}

                function clearCanvas() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    strokes = [];
                    currentStroke = [];
                }}

                function undoLast() {{
                    if (strokes.length > 0) {{
                        strokes.pop();
                        redrawCanvas();
                    }}
                }}

                function redrawCanvas() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    
                    for (const stroke of strokes) {{
                        if (stroke.length > 0) {{
                            ctx.beginPath();
                            ctx.moveTo(stroke[0].x, stroke[0].y);
                            
                            for (let i = 1; i < stroke.length; i++) {{
                                ctx.lineTo(stroke[i].x, stroke[i].y);
                            }}
                            ctx.stroke();
                        }}
                    }}
                }}

                function saveDrawing() {{
                    const dataURL = canvas.toDataURL('image/png');
                    
                    if (typeof google !== 'undefined' && google.colab) {{
                        google.colab.kernel.invokeFunction('notebook.save_image', [dataURL], {{}});
                    }} else {{
                        const link = document.createElement('a');
                        link.download = 'drawing.png';
                        link.href = dataURL;
                        link.click();
                    }}
                }}
            </script>
        </body>
        </html>
        """
        
        return HTML(html_code)
    
    def register_save_callback(self, callback_func: Optional[Callable] = None):
        """
        Register a callback function for saving drawings.
        
        Args:
            callback_func: Function to call when saving (default uses built-in)
        """
        try:
            from google.colab import output
            
            if callback_func is None:
                callback_func = self._default_save_callback
            
            output.register_callback('notebook.save_image', callback_func)
            self.callback_registered = True
            print("Save callback registered successfully")
            
        except ImportError:
            print("Google Colab not detected. Save callback not registered.")
    
    def _default_save_callback(self, data_url: str, filename: str = "drawing.png"):
        """
        Default callback for saving drawings.
        
        Args:
            data_url: Base64 encoded image data URL
            filename: Output filename
        """
        try:
            header, encoded = data_url.split(",", 1)
            decoded_data = base64.b64decode(encoded)
            
            image = Image.open(io.BytesIO(decoded_data))
            image.save(filename)
            
            print(f"Successfully saved drawing as '{filename}'!")
            print("Look for it in the file browser.")
            
        except Exception as e:
            print(f"Error saving image: {e}")
    
    def load_image_from_file(self, filepath: str) -> Image.Image:
        """
        Load an image from file for processing.
        
        Args:
            filepath: Path to image file
            
        Returns:
            PIL Image object
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Image file not found: {filepath}")
        
        return Image.open(filepath).convert("RGB")
    
    def get_canvas_info(self) -> dict:
        """
        Get information about the drawing canvas configuration.
        
        Returns:
            Dictionary with canvas information
        """
        return {
            "canvas_width": self.canvas_width,
            "canvas_height": self.canvas_height,
            "background_color": self.background_color,
            "default_brush_color": self.default_brush_color,
            "default_brush_size": self.default_brush_size,
            "callback_registered": self.callback_registered
        }