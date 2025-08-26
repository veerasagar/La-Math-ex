"""
Data downloading utilities for La-Math-ex.

This module provides functionality to download and extract mathematical
datasets, particularly the MathWriting dataset.
"""

import os
import tarfile
import requests
from typing import Optional
import shutil
from pathlib import Path


class DataDownloader:
    """
    Utility class for downloading and managing mathematical datasets.
    """
    
    MATHWRITING_URL = "https://storage.googleapis.com/mathwriting_data/mathwriting-2024.tgz"
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data downloader.
        
        Args:
            data_dir: Directory to store downloaded data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def download_mathwriting_dataset(self, force_download: bool = False) -> str:
        """
        Download and extract the MathWriting 2024 dataset.
        
        Args:
            force_download: Whether to re-download if already exists
            
        Returns:
            Path to the extracted dataset directory
            
        Raises:
            requests.RequestException: If download fails
            tarfile.TarError: If extraction fails
        """
        dataset_dir = self.data_dir / "mathwriting-2024"
        archive_path = self.data_dir / "mathwriting-2024.tgz"
        
        # Check if dataset already exists
        if dataset_dir.exists() and not force_download:
            print(f"MathWriting dataset already exists at: {dataset_dir}")
            return str(dataset_dir)
        
        # Download the dataset
        print("Downloading MathWriting dataset...")
        try:
            response = requests.get(self.MATHWRITING_URL, stream=True)
            response.raise_for_status()
            
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            print(f"Downloaded dataset to: {archive_path}")
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to download dataset: {e}")
        
        # Extract the dataset
        print("Extracting dataset...")
        try:
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(path=self.data_dir)
            print(f"Extracted dataset to: {dataset_dir}")
            
        except tarfile.TarError as e:
            raise tarfile.TarError(f"Failed to extract dataset: {e}")
        
        # Clean up archive file
        if archive_path.exists():
            os.remove(archive_path)
            print("Cleaned up archive file")
        
        return str(dataset_dir)
    
    def list_dataset_contents(self, dataset_path: Optional[str] = None) -> dict:
        """
        List the contents of a dataset directory.
        
        Args:
            dataset_path: Path to dataset directory (uses default if None)
            
        Returns:
            Dictionary with dataset structure information
        """
        if dataset_path is None:
            dataset_path = self.data_dir / "mathwriting-2024"
        else:
            dataset_path = Path(dataset_path)
        
        if not dataset_path.exists():
            return {"error": f"Dataset path does not exist: {dataset_path}"}
        
        contents = {}
        for item in dataset_path.iterdir():
            if item.is_dir():
                contents[item.name] = {
                    "type": "directory",
                    "count": len(list(item.iterdir())) if item.is_dir() else 0
                }
            else:
                contents[item.name] = {
                    "type": "file",
                    "size": item.stat().st_size
                }
        
        return contents
    
    def get_sample_files(self, dataset_path: Optional[str] = None, 
                        subdirectory: str = "symbols", 
                        limit: int = 10) -> list:
        """
        Get a list of sample files from the dataset.
        
        Args:
            dataset_path: Path to dataset directory
            subdirectory: Subdirectory to sample from
            limit: Maximum number of files to return
            
        Returns:
            List of file paths
        """
        if dataset_path is None:
            dataset_path = self.data_dir / "mathwriting-2024"
        else:
            dataset_path = Path(dataset_path)
        
        subdir_path = dataset_path / subdirectory
        if not subdir_path.exists():
            return []
        
        files = list(subdir_path.glob("*.inkml"))[:limit]
        return [str(f) for f in files]
    
    def cleanup_data(self):
        """Remove all downloaded data."""
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)
            print(f"Cleaned up data directory: {self.data_dir}")
    
    @staticmethod
    def get_dataset_info() -> dict:
        """
        Get information about available datasets.
        
        Returns:
            Dictionary with dataset information
        """
        return {
            "mathwriting-2024": {
                "url": DataDownloader.MATHWRITING_URL,
                "description": "Handwritten mathematical expressions dataset",
                "size": "~2.88GB",
                "contents": ["symbols", "synthetic", "train", "test", "valid"]
            }
        }