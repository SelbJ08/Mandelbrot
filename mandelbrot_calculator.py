"""
Modul zur Berechnung der Mandelbrot-Menge.
"""

import numpy as np
from numba import jit


@jit(nopython=True)
def calculate_mandelbrot(min_real, max_real, min_imag, max_imag, 
                        width, height, max_iterations):
    """
    Berechnet die Mandelbrot-Menge für einen gegebenen Bereich.
    
    Args:
        min_real, max_real: Bereich der reellen Achse
        min_imag, max_imag: Bereich der imaginären Achse
        width, height: Auflösung des Bildes
        max_iterations: Maximale Anzahl von Iterationen
    
    Returns:
        2D numpy-Array mit Iterationswerten für jeden Pixel
    """
    # Initialisiere das Output-Array
    mandelbrot_set = np.zeros((height, width))
    
    # Schrittgröße für Real- und Imaginärteil
    real_step = (max_real - min_real) / width
    imag_step = (max_imag - min_imag) / height
    
    # Iteriere über jeden Pixel
    for y in range(height):
        imag = min_imag + y * imag_step
        for x in range(width):
            real = min_real + x * real_step
            
            # Berechne die Anzahl der Iterationen für diesen Pixel
            mandelbrot_set[y, x] = mandelbrot_iteration(real, imag, max_iterations)
    
    return mandelbrot_set


@jit(nopython=True)
def mandelbrot_iteration(real, imag, max_iterations):
    """
    Berechnet die Anzahl der Iterationen bis zur Divergenz für einen Punkt.
    
    Args:
        real: Reeller Teil der komplexen Zahl c
        imag: Imaginärer Teil der komplexen Zahl c
        max_iterations: Maximale Anzahl von Iterationen
    
    Returns:
        int: Anzahl der Iterationen bis zur Divergenz
    """
    c = complex(real, imag)
    z = 0j
    
    for n in range(max_iterations):
        if abs(z) > 2:
            return n
        z = z * z + c
    
    return max_iterations


class MandelbrotCalculator:
    """Wrapper-Klasse für Mandelbrot-Berechnungen mit verschiedenen Zoom-Stufen."""
    
    # Vordefinierte Zoom-Bereiche für interessante Regionen
    ZOOM_LEVELS = {
        'full': {
            'min_real': -2.5,
            'max_real': 1.0,
            'min_imag': -1.25,
            'max_imag': 1.25,
            'description': 'Vollständige Mandelbrot-Menge'
        },
        'seahorse_valley': {
            'min_real': -0.75,
            'max_real': -0.735,
            'min_imag': 0.095,
            'max_imag': 0.11,
            'description': 'Seahorse Valley'
        },
        'spiral': {
            'min_real': -0.8,
            'max_real': -0.4,
            'min_imag': -0.2,
            'max_imag': 0.2,
            'description': 'Spirale Region'
        },
        'elephant_valley': {
            'min_real': 0.25,
            'max_real': 0.26,
            'min_imag': 0.02,
            'max_imag': 0.03,
            'description': 'Elephant Valley'
        }
    }
    
    @staticmethod
    def compute(min_real, max_real, min_imag, max_imag, 
                width=800, height=600, max_iterations=256):
        """Berechnet die Mandelbrot-Menge."""
        return calculate_mandelbrot(min_real, max_real, min_imag, max_imag,
                                   width, height, max_iterations)
    
    @staticmethod
    def get_zoom_level(name):
        """Gibt die Koordinaten eines vordefinierten Zoom-Levels zurück."""
        return MandelbrotCalculator.ZOOM_LEVELS.get(name)
    
    @staticmethod
    def list_zoom_levels():
        """Listet alle verfügbaren vordefiniert Zoom-Level auf."""
        return list(MandelbrotCalculator.ZOOM_LEVELS.keys())
