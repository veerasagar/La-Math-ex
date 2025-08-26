"""
Visualization module for La-Math-ex.

This module provides functionality to visualize InkML data and mathematical
expressions in various formats.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpl_patches
from typing import Tuple, Optional, Union, List
import numpy as np
from ..data.ink_processor import Ink


class InkVisualizer:
    """
    Visualizer class for ink data and mathematical expressions.
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        pass
    
    @staticmethod
    def display_ink(ink: Ink, 
                   figsize: Tuple[int, int] = (15, 10),
                   linewidth: int = 2,
                   color: Optional[str] = None,
                   title: Optional[str] = None,
                   show_annotations: bool = True) -> plt.Figure:
        """
        Simple display for a single ink.
        
        Args:
            ink: Ink object to display
            figsize: Figure size (width, height)
            linewidth: Line width for strokes
            color: Color for strokes (None for default)
            title: Custom title (None for auto-generated)
            show_annotations: Whether to show annotation information
            
        Returns:
            matplotlib Figure object
        """
        fig = plt.figure(figsize=figsize)
        
        if not ink.strokes:
            plt.text(0.5, 0.5, 'No strokes to display', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes, fontsize=16)
            if title:
                plt.title(title)
            return fig
        
        # Plot each stroke
        for stroke in ink.strokes:
            plt.plot(stroke[0], stroke[1], linewidth=linewidth, color=color)
        
        # Generate title from annotations or use custom title
        if title is None and show_annotations:
            title_parts = []
            if 'sampleId' in ink.annotations:
                title_parts.append(ink.annotations['sampleId'])
            if 'splitTagOriginal' in ink.annotations:
                title_parts.append(ink.annotations['splitTagOriginal'])
            if 'normalizedLabel' in ink.annotations:
                title_parts.append(ink.annotations['normalizedLabel'])
            elif 'label' in ink.annotations:
                title_parts.append(ink.annotations['label'])
            
            title = " -- ".join(title_parts) if title_parts else "Ink Visualization"
        
        if title:
            plt.title(title)
        
        plt.gca().invert_yaxis()  # Invert y-axis for standard ink coordinate system
        plt.gca().axis('equal')   # Equal aspect ratio
        plt.xlabel('X')
        plt.ylabel('Y')
        
        return fig
    
    @staticmethod
    def display_multiple_inks(inks: List[Ink], 
                             cols: int = 3,
                             figsize: Tuple[int, int] = (15, 10),
                             linewidth: int = 2) -> plt.Figure:
        """
        Display multiple inks in a grid layout.
        
        Args:
            inks: List of Ink objects to display
            cols: Number of columns in the grid
            figsize: Figure size (width, height)
            linewidth: Line width for strokes
            
        Returns:
            matplotlib Figure object
        """
        if not inks:
            fig = plt.figure(figsize=figsize)
            plt.text(0.5, 0.5, 'No inks to display', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes, fontsize=16)
            return fig
        
        rows = (len(inks) + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        
        # Handle single row case
        if rows == 1:
            axes = [axes] if cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, ink in enumerate(inks):
            ax = axes[i] if len(inks) > 1 else plt.gca()
            
            # Plot strokes
            for stroke in ink.strokes:
                ax.plot(stroke[0], stroke[1], linewidth=linewidth)
            
            # Set title from annotations
            title = ink.annotations.get('label', f'Ink {i+1}')
            ax.set_title(title, fontsize=10)
            ax.invert_yaxis()
            ax.axis('equal')
        
        # Hide empty subplots
        for i in range(len(inks), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_stroke_statistics(inks: List[Ink]) -> plt.Figure:
        """
        Plot statistics about stroke data.
        
        Args:
            inks: List of Ink objects to analyze
            
        Returns:
            matplotlib Figure object
        """
        if not inks:
            fig = plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'No data to analyze', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes, fontsize=16)
            return fig
        
        stroke_counts = [len(ink.strokes) for ink in inks]
        point_counts = [sum(stroke.shape[1] for stroke in ink.strokes) for ink in inks]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Stroke count histogram
        ax1.hist(stroke_counts, bins=20, alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Number of Strokes')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Stroke Counts')
        ax1.grid(True, alpha=0.3)
        
        # Point count histogram
        ax2.hist(point_counts, bins=20, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Number of Points')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Point Counts')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_bounding_boxes(inks: List[Ink], 
                           figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """
        Visualize bounding boxes of multiple inks.
        
        Args:
            inks: List of Ink objects
            figsize: Figure size (width, height)
            
        Returns:
            matplotlib Figure object
        """
        from ..data.ink_processor import InkProcessor
        
        fig = plt.figure(figsize=figsize)
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(inks)))
        
        for i, ink in enumerate(inks):
            bbox = InkProcessor.get_bounding_box(ink)
            if bbox is None:
                continue
                
            min_x, min_y, max_x, max_y = bbox
            width = max_x - min_x
            height = max_y - min_y
            
            # Create rectangle
            rect = mpl_patches.Rectangle((min_x, min_y), width, height,
                                       linewidth=2, edgecolor=colors[i],
                                       facecolor='none', alpha=0.7,
                                       label=f'Ink {i+1}')
            plt.gca().add_patch(rect)
            
            # Add label
            plt.text(min_x + width/2, min_y + height/2, f'Ink {i+1}',
                    ha='center', va='center', fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Bounding Boxes of Ink Objects')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        return fig
    
    @staticmethod
    def save_visualization(fig: plt.Figure, 
                          filename: str, 
                          dpi: int = 300,
                          bbox_inches: str = 'tight'):
        """
        Save a visualization to file.
        
        Args:
            fig: matplotlib Figure object
            filename: Output filename
            dpi: Resolution for raster formats
            bbox_inches: Bounding box mode for saving
        """
        fig.savefig(filename, dpi=dpi, bbox_inches=bbox_inches)
        print(f"Visualization saved to: {filename}")