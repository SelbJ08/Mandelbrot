"""
Modul zur Visualisierung der Mandelbrot-Menge.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from matplotlib.widgets import Button, TextBox
from mandelbrot_calculator import MandelbrotCalculator
from database import MandelbrotDatabase


def create_rainbow_colormap():
    """
    Erstellt eine Custom Colormap mit 7 Farben (Regenbogen).
    Wechsel von: Dunkelblau → Cyan → Grün → Gelb → Orange → Rot → Violett
    """
    colors_list = [
        '#000033',  # Dunkelblau (0)
        '#0066FF',  # Blau
        '#00FFFF',  # Cyan
        '#00FF00',  # Grün
        '#FFFF00',  # Gelb
        '#FF6600',  # Orange
        '#FF0000',  # Rot
        '#8800FF',  # Violett (256)
    ]
    
    return LinearSegmentedColormap.from_list('mandelbrot_rainbow', colors_list)


class MandelbrotVisualizer:
    """Interaktive Visualisierung der Mandelbrot-Menge."""
    
    def __init__(self, width=1000, height=750, max_iterations=256):
        """Initialisiert den Visualizer."""
        self.width = width
        self.height = height
        self.max_iterations = max_iterations
        self.db = MandelbrotDatabase()
        
        # Standardbereich
        self.min_real = -2.5
        self.max_real = 1.0
        self.min_imag = -1.25
        self.max_imag = 1.25
        
        self.mandelbrot_set = None
        self.current_set_id = None
        
        # Erstelle die Figur und Achsen
        self.fig, self.ax = plt.subplots(figsize=(12, 9))
        self.im = None
        
        # Erstelle die Rainbow-Colormap
        self.rainbow_cmap = create_rainbow_colormap()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Erstellt die Benutzeroberfläche mit Buttons und Input-Feldern."""
        plt.subplots_adjust(bottom=0.35)
        
        # Buttons für vordefinierte Zoom-Level
        ax_full = plt.axes([0.2, 0.25, 0.1, 0.04])
        btn_full = Button(ax_full, 'Vollständig')
        btn_full.on_clicked(lambda event: self.zoom_to_level('full'))
        
        ax_seahorse = plt.axes([0.35, 0.25, 0.1, 0.04])
        btn_seahorse = Button(ax_seahorse, 'Seahorse')
        btn_seahorse.on_clicked(lambda event: self.zoom_to_level('seahorse_valley'))
        
        ax_spiral = plt.axes([0.5, 0.25, 0.1, 0.04])
        btn_spiral = Button(ax_spiral, 'Spirale')
        btn_spiral.on_clicked(lambda event: self.zoom_to_level('spiral'))
        
        ax_elephant = plt.axes([0.65, 0.25, 0.1, 0.04])
        btn_elephant = Button(ax_elephant, 'Elephant')
        btn_elephant.on_clicked(lambda event: self.zoom_to_level('elephant_valley'))
        
        # Input-Felder für benutzerdefinierte Bereiche
        ax_min_real = plt.axes([0.2, 0.18, 0.15, 0.04])
        self.textbox_min_real = TextBox(ax_min_real, 'Min Real:', initial=str(self.min_real))
        
        ax_max_real = plt.axes([0.2, 0.12, 0.15, 0.04])
        self.textbox_max_real = TextBox(ax_max_real, 'Max Real:', initial=str(self.max_real))
        
        ax_min_imag = plt.axes([0.55, 0.18, 0.15, 0.04])
        self.textbox_min_imag = TextBox(ax_min_imag, 'Min Imag:', initial=str(self.min_imag))
        
        ax_max_imag = plt.axes([0.55, 0.12, 0.15, 0.04])
        self.textbox_max_imag = TextBox(ax_max_imag, 'Max Imag:', initial=str(self.max_imag))
        
        # Button zum Berechnen
        ax_compute = plt.axes([0.4, 0.03, 0.15, 0.06])
        btn_compute = Button(ax_compute, 'Berechnen\nund Speichern')
        btn_compute.on_clicked(self.on_compute_clicked)
        
        # Button zum Speichern
        ax_save = plt.axes([0.6, 0.03, 0.15, 0.06])
        btn_save = Button(ax_save, 'Als PNG\nSpeichern')
        btn_save.on_clicked(self.save_image)
    
    def zoom_to_level(self, level_name):
        """Zoomt zu einem vordefinierten Level."""
        level = MandelbrotCalculator.get_zoom_level(level_name)
        if level:
            self.min_real = level['min_real']
            self.max_real = level['max_real']
            self.min_imag = level['min_imag']
            self.max_imag = level['max_imag']
            self.compute_and_display()
    
    def on_compute_clicked(self, event):
        """Event-Handler für Compute-Button."""
        try:
            self.min_real = float(self.textbox_min_real.text)
            self.max_real = float(self.textbox_max_real.text)
            self.min_imag = float(self.textbox_min_imag.text)
            self.max_imag = float(self.textbox_max_imag.text)
            self.compute_and_display()
        except ValueError:
            print("Fehler: Bitte geben Sie gültige Zahlen ein!")
    
    def compute_and_display(self):
        """Berechnet die Mandelbrot-Menge und zeigt sie an."""
        print(f"Berechne Mandelbrot-Menge... ({self.width}x{self.height})")
        
        # Berechne die Mandelbrot-Menge
        self.mandelbrot_set = MandelbrotCalculator.compute(
            self.min_real, self.max_real, self.min_imag, self.max_imag,
            self.width, self.height, self.max_iterations
        )
        
        # Speichere in der Datenbank
        description = f"Bereich: [{self.min_real:.6f}, {self.max_real:.6f}] x [{self.min_imag:.6f}, {self.max_imag:.6f}]"
        self.current_set_id = self.db.insert_mandelbrot_set(
            self.min_real, self.max_real, self.min_imag, self.max_imag,
            self.width, self.height, self.max_iterations, description
        )
        
        # Speichere die Pixel-Daten
        self.db.insert_pixel_data(self.current_set_id, self.mandelbrot_set)
        
        print(f"✓ Gespeichert mit ID: {self.current_set_id}")
        
        # Visualisiere
        self.display()
    
    def display(self):
        """Zeigt die Mandelbrot-Menge an."""
        if self.mandelbrot_set is None:
            return
        
        self.ax.clear()
        
        # Verwende logarithmische Skalierung für bessere Farbverteilung
        norm = colors.PowerNorm(gamma=0.3, vmin=0, vmax=self.max_iterations)
        
        # Zeige das Bild mit Rainbow-Colormap an
        self.im = self.ax.imshow(
            self.mandelbrot_set,
            extent=[self.min_real, self.max_real, self.min_imag, self.max_imag],
            cmap=self.rainbow_cmap,  # Verwendet jetzt die Rainbow-Colormap
            origin='lower',
            norm=norm,
            interpolation='bilinear'
        )
        
        self.ax.set_xlabel('Reelle Achse')
        self.ax.set_ylabel('Imaginäre Achse')
        self.ax.set_title(f'Mandelbrot-Menge (ID: {self.current_set_id})')
        
        plt.colorbar(self.im, ax=self.ax, label='Iterationen bis Divergenz')
        plt.draw()
    
    def save_image(self, event):
        """Speichert das aktuelle Bild als PNG."""
        if self.mandelbrot_set is None:
            print("Keine Mandelbrot-Menge zu speichern!")
            return
        
        filename = f"mandelbrot_{self.current_set_id}.png"
        self.fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Bild gespeichert als: {filename}")
    
    def show(self):
        """Zeigt die interaktive Visualisierung an."""
        # Berechne initial die Vollständige Menge
        self.compute_and_display()
        plt.show()
    
    def __del__(self):
        """Cleanup bei Objektzerstörung."""
        self.db.close()


def main():
    """Hauptfunktion."""
    print("=" * 60)
    print("MANDELBROT-MENGE VISUALIZER")
    print("=" * 60)
    print()
    print("Interaktive Visualisierung der Mandelbrot-Menge")
    print("- Wählen Sie vordefinierte Zoom-Level oder geben Sie eigene Bereiche ein")
    print("- Klicken Sie auf 'Berechnen und Speichern' um die Menge zu berechnen")
    print("- Alle Berechnungen werden in der SQLite-Datenbank gespeichert")
    print()
    
    visualizer = MandelbrotVisualizer(width=1000, height=750, max_iterations=256)
    visualizer.show()


if __name__ == '__main__':
    main()
