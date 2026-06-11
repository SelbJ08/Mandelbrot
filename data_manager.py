"""
Modul zum Verwalten und Analysieren gespeicherter Mandelbrot-Daten.
"""

import numpy as np
from database import MandelbrotDatabase
import matplotlib.pyplot as plt


class MandelbrotDataManager:
    """Verwaltet die Abfrage und Analyse von gespeicherten Mandelbrot-Daten."""
    
    def __init__(self, db_path="mandelbrot_data.db"):
        """Initialisiert den Data Manager."""
        self.db = MandelbrotDatabase(db_path)
    
    def list_all_sets(self):
        """Listet alle gespeicherten Mandelbrot-Sets auf."""
        sets = self.db.list_sets()
        if not sets:
            print("Keine Mandelbrot-Sets gespeichert.")
            return
        
        print("\n" + "=" * 100)
        print("GESPEICHERTE MANDELBROT-SETS")
        print("=" * 100)
        print(f"{'ID':<5} {'Erstellt am':<20} {'Größe':<12} {'Iterationen':<12} {'Beschreibung':<50}")
        print("-" * 100)
        
        for set_info in sets:
            set_id, created_at, width, height, max_iter, desc = set_info
            size = f"{width}x{height}"
            desc = desc[:47] + "..." if desc and len(desc) > 50 else desc
            print(f"{set_id:<5} {created_at:<20} {size:<12} {max_iter:<12} {desc:<50}")
        
        print("=" * 100)
    
    def get_set_statistics(self, set_id):
        """Berechnet Statistiken für ein gespeichertes Set."""
        set_info = self.db.get_mandelbrot_set(set_id)
        if not set_info:
            print(f"Set mit ID {set_id} nicht gefunden!")
            return
        
        set_id, created_at, min_real, max_real, min_imag, max_imag, width, height, max_iter, desc = set_info
        
        # Rufe Pixel-Daten ab
        pixels = self.db.get_pixel_data(set_id)
        
        if not pixels:
            print(f"Keine Pixel-Daten für Set {set_id} gefunden!")
            return
        
        # Konvertiere zu numpy-Array für Analyse
        iterations = np.array([p[2] for p in pixels])
        
        print("\n" + "=" * 60)
        print(f"STATISTIKEN FÜR SET #{set_id}")
        print("=" * 60)
        print(f"Erstellt:        {created_at}")
        print(f"Auflösung:       {width}x{height} ({width*height:,} Pixel)")
        print(f"Max Iterationen: {max_iter}")
        print(f"Bereich (Real):  [{min_real:.6f}, {max_real:.6f}]")
        print(f"Bereich (Imag):  [{min_imag:.6f}, {max_imag:.6f}]")
        print()
        print("Divergenz-Statistiken:")
        print(f"  - Durchschnittliche Iterationen: {iterations.mean():.2f}")
        print(f"  - Minimum: {iterations.min()}")
        print(f"  - Maximum: {iterations.max()}")
        print(f"  - Standardabweichung: {iterations.std():.2f}")
        print(f"  - Im Set (max_iter): {np.sum(iterations == max_iter):,} Pixel ({100*np.sum(iterations == max_iter)/len(iterations):.2f}%)")
        print(f"  - Divergent: {np.sum(iterations < max_iter):,} Pixel ({100*np.sum(iterations < max_iter)/len(iterations):.2f}%)")
        print("=" * 60)
    
    def visualize_set(self, set_id):
        """Visualisiert ein gespeichertes Set."""
        set_info = self.db.get_mandelbrot_set(set_id)
        if not set_info:
            print(f"Set mit ID {set_id} nicht gefunden!")
            return
        
        set_id, created_at, min_real, max_real, min_imag, max_imag, width, height, max_iter, desc = set_info
        
        # Rufe Pixel-Daten ab
        pixels = self.db.get_pixel_data(set_id)
        if not pixels:
            print(f"Keine Pixel-Daten für Set {set_id} gefunden!")
            return
        
        # Rekonstruiere das 2D-Array
        mandelbrot_array = np.zeros((height, width))
        for x, y, iterations in pixels:
            mandelbrot_array[y, x] = iterations
        
        # Visualisiere
        fig, ax = plt.subplots(figsize=(12, 9))
        im = ax.imshow(
            mandelbrot_array,
            extent=[min_real, max_real, min_imag, max_imag],
            cmap='hot',
            origin='lower',
            interpolation='bilinear'
        )
        ax.set_xlabel('Reelle Achse')
        ax.set_ylabel('Imaginäre Achse')
        ax.set_title(f'Mandelbrot-Menge (ID: {set_id})\n{desc}')
        plt.colorbar(im, ax=ax, label='Iterationen bis Divergenz')
        plt.tight_layout()
        plt.show()
    
    def export_to_numpy(self, set_id, filename=None):
        """Exportiert ein Set als numpy-Datei."""
        set_info = self.db.get_mandelbrot_set(set_id)
        if not set_info:
            print(f"Set mit ID {set_id} nicht gefunden!")
            return
        
        set_id, _, _, _, _, _, width, height, _, _ = set_info
        
        pixels = self.db.get_pixel_data(set_id)
        if not pixels:
            print(f"Keine Pixel-Daten für Set {set_id} gefunden!")
            return
        
        # Rekonstruiere das 2D-Array
        mandelbrot_array = np.zeros((height, width))
        for x, y, iterations in pixels:
            mandelbrot_array[y, x] = iterations
        
        if filename is None:
            filename = f"mandelbrot_set_{set_id}.npy"
        
        np.save(filename, mandelbrot_array)
        print(f"✓ Exportiert nach: {filename}")
    
    def close(self):
        """Schließt die Datenbankverbindung."""
        self.db.close()


def main():
    """Hauptfunktion für die CLI."""
    import sys
    
    manager = MandelbrotDataManager()
    
    print("\n" + "=" * 60)
    print("MANDELBROT DATA MANAGER")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'list':
            manager.list_all_sets()
        
        elif command == 'stats' and len(sys.argv) > 2:
            try:
                set_id = int(sys.argv[2])
                manager.get_set_statistics(set_id)
            except ValueError:
                print("Fehler: Set-ID muss eine Ganzzahl sein!")
        
        elif command == 'view' and len(sys.argv) > 2:
            try:
                set_id = int(sys.argv[2])
                manager.visualize_set(set_id)
            except ValueError:
                print("Fehler: Set-ID muss eine Ganzzahl sein!")
        
        elif command == 'export' and len(sys.argv) > 2:
            try:
                set_id = int(sys.argv[2])
                filename = sys.argv[3] if len(sys.argv) > 3 else None
                manager.export_to_numpy(set_id, filename)
            except ValueError:
                print("Fehler: Set-ID muss eine Ganzzahl sein!")
        
        else:
            print_help()
    else:
        print_help()
    
    manager.close()


def print_help():
    """Zeigt die Hilfe an."""
    help_text = """
Verwendung: python data_manager.py [COMMAND] [ARGS]

Verfügbare Befehle:
  list              Listet alle gespeicherten Mandelbrot-Sets auf
  stats <set_id>    Zeigt Statistiken für ein Set an
  view <set_id>     Visualisiert ein gespeichertes Set
  export <set_id> [filename]  Exportiert ein Set als numpy-Datei

Beispiele:
  python data_manager.py list
  python data_manager.py stats 1
  python data_manager.py view 1
  python data_manager.py export 1 myset.npy
"""
    print(help_text)


if __name__ == '__main__':
    main()
