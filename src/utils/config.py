"""
Configuration module for La-Math-ex.

This module provides configuration settings and constants used throughout
the package.
"""

import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration class for La-Math-ex settings."""
    
    # Default model configurations
    DEFAULT_MODELS = {
        "handwritten_math": "fhswf/TrOCR_Math_handwritten",
        "printed_math": "microsoft/trocr-base-printed",
        "handwritten_text": "microsoft/trocr-base-handwritten"
    }
    
    # Dataset configurations
    DATASETS = {
        "mathwriting_2024": {
            "url": "https://storage.googleapis.com/mathwriting_data/mathwriting-2024.tgz",
            "size": "~2.88GB",
            "description": "Handwritten mathematical expressions dataset"
        }
    }
    
    # Image processing defaults
    IMAGE_DEFAULTS = {
        "target_size": (384, 384),
        "background_color": "white",
        "max_file_size_mb": 10,
        "supported_formats": ["PNG", "JPEG", "JPG", "BMP", "TIFF"]
    }
    
    # Drawing interface defaults
    DRAWING_DEFAULTS = {
        "canvas_width": 800,
        "canvas_height": 400,
        "background_color": "white",
        "brush_color": "black",
        "brush_size": 3
    }
    
    # Visualization defaults
    VISUALIZATION_DEFAULTS = {
        "figure_size": (15, 10),
        "line_width": 2,
        "dpi": 300,
        "color_scheme": "tab10"
    }
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Optional path to configuration file
        """
        self._config = self._load_default_config()
        
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration settings."""
        return {
            "models": self.DEFAULT_MODELS.copy(),
            "datasets": self.DATASETS.copy(),
            "image": self.IMAGE_DEFAULTS.copy(),
            "drawing": self.DRAWING_DEFAULTS.copy(),
            "visualization": self.VISUALIZATION_DEFAULTS.copy(),
            "paths": {
                "data_dir": "data",
                "models_dir": "models",
                "output_dir": "output",
                "cache_dir": ".cache"
            }
        }
    
    def _load_config_file(self, config_file: str):
        """
        Load configuration from file.
        
        Args:
            config_file: Path to configuration file (JSON or YAML)
        """
        import json
        
        with open(config_file, 'r') as f:
            if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                try:
                    import yaml
                    file_config = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML required for YAML config files")
            else:
                file_config = json.load(f)
        
        # Update configuration
        self._deep_update(self._config, file_config)
    
    def _deep_update(self, base_dict: dict, update_dict: dict):
        """Recursively update nested dictionary."""
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict:
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'models.handwritten_math')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'models.handwritten_math')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_config(self, filepath: str):
        """
        Save current configuration to file.
        
        Args:
            filepath: Output file path
        """
        import json
        
        with open(filepath, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def create_directories(self):
        """Create necessary directories."""
        for dir_key in ['data_dir', 'models_dir', 'output_dir', 'cache_dir']:
            dir_path = Path(self.get(f'paths.{dir_key}'))
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @property
    def data_dir(self) -> str:
        """Get data directory path."""
        return self.get('paths.data_dir')
    
    @property
    def models_dir(self) -> str:
        """Get models directory path."""
        return self.get('paths.models_dir')
    
    @property
    def output_dir(self) -> str:
        """Get output directory path."""
        return self.get('paths.output_dir')
    
    @property
    def cache_dir(self) -> str:
        """Get cache directory path."""
        return self.get('paths.cache_dir')


# Global configuration instance
config = Config()