"""
Modul zur Visualisierung der Mandelbrot-Menge mit moderner UI.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
import numpy as np
from matplotlib.widgets import Button, TextBox, Slider
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
    """Interaktive Visualisierung der Mandelbrot-Menge mit moderner UI."""
    
    def __init__(self, width=1200, height=800, max_iterations=256):
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
        
        # Moderne Farbpalette
        self.bg_color = '#0f0f0f'
        self.panel_color = '#1a1a1a'
        self.accent_color = '#00d4ff'
        self.button_color = '#0088cc'
        self.button_hover = '#00b3ff'
        self.text_color = '#ffffff'
        
        # Erstelle die Figur mit dunklem Theme
        self.fig = plt.figure(figsize=(14, 10), facecolor=self.bg_color)
        self.fig.patch.set_facecolor(self.bg_color)
        
        # Layout mit GridSpec für bessere Kontrolle
        gs = self.fig.add_gridspec(4, 3, left=0.05, right=0.95, top=0.95, bottom=0.05,
                                    hspace=0.4, wspace=0.3)
        
        self.ax_mandelbrot = self.fig.add_subplot(gs[0:3, 0:2])
        self.ax_mandelbrot.set_facecolor(self.panel_color)
        
        self.im = None
        
        # Erstelle die Rainbow-Colormap
        self.rainbow_cmap = create_rainbow_colormap()
        
        self.setup_ui(gs)
    
    def setup_ui(self, gs):
        """Erstellt die moderne Benutzeroberfläche."""
        
        # === ZOOM-BUTTONS (Oben) ===
        zoom_buttons = [
            ('Vollständig', 'full', 0.05, 0.88),
            ('Seahorse 🐴', 'seahorse_valley', 0.25, 0.88),
            ('Spirale 🌀', 'spiral', 0.45, 0.88),
            ('Elephant 🐘', 'elephant_valley', 0.65, 0.88),
        ]
        
        for label, level, x, y in zoom_buttons:
            ax_btn = plt.axes([x, y, 0.17, 0.06])
            ax_btn.set_facecolor(self.panel_color)
            btn = Button(ax_btn, label, color=self.button_color, hovercolor=self.button_hover)
            btn.label.set_color(self.text_color)
            btn.label.set_fontsize(10)
            btn.label.set_weight('bold')
            btn.on_clicked(lambda event, l=level: self.zoom_to_level(l))
        
        # === INPUT-FELDER (Links Seite) ===
        input_y_start = 0.75
        input_spacing = 0.11
        
        # Reelle Achse Label
        self.fig.text(0.05, input_y_start + 0.02, '📍 Reelle Achse', 
                     color=self.accent_color, fontsize=11, weight='bold')
        
        ax_min_real = plt.axes([0.05, input_y_start - 0.03, 0.17, 0.04])
        ax_min_real.set_facecolor(self.panel_color)
        self.textbox_min_real = TextBox(ax_min_real, 'Min:', initial=str(self.min_real),
                                       color_bg=self.panel_color, color_fg=self.text_color)
        self.textbox_min_real.label.set_color(self.accent_color)
        
        ax_max_real = plt.axes([0.05, input_y_start - 0.08, 0.17, 0.04])
        ax_max_real.set_facecolor(self.panel_color)
        self.textbox_max_real = TextBox(ax_max_real, 'Max:', initial=str(self.max_real),
                                       color_bg=self.panel_color, color_fg=self.text_color)
        self.textbox_max_real.label.set_color(self.accent_color)
        
        # Imaginäre Achse Label
        self.fig.text(0.05, input_y_start - 0.15, '📍 Imaginäre Achse', 
                     color=self.accent_color, fontsize=11, weight='bold')
        
        ax_min_imag = plt.axes([0.05, input_y_start - 0.2, 0.17, 0.04])
        ax_min_imag.set_facecolor(self.panel_color)
        self.textbox_min_imag = TextBox(ax_min_imag, 'Min:', initial=str(self.min_imag),
                                       color_bg=self.panel_color, color_fg=self.text_color)
        self.textbox_min_imag.label.set_color(self.accent_color)
        
        ax_max_imag = plt.axes([0.05, input_y_start - 0.25, 0.17, 0.04])
        ax_max_imag.set_facecolor(self.panel_color)
        self.textbox_max_imag = TextBox(ax_max_imag, 'Max:', initial=str(self.max_imag),
                                       color_bg=self.panel_color, color_fg=self.text_color)
        self.textbox_max_imag.label.set_color(self.accent_color)
        
        # === HAUPT-AKTIONS-BUTTONS (Rechts unten) ===
        ax_compute = plt.axes([0.6, 0.08, 0.18, 0.08])
        ax_compute.set_facecolor(self.panel_color)
        btn_compute = Button(ax_compute, '⚡ BERECHNEN', color='#00aa00', hovercolor='#00dd00')
        btn_compute.label.set_color(self.text_color)
        btn_compute.label.set_fontsize(11)
        btn_compute.label.set_weight('bold')
        btn_compute.on_clicked(self.on_compute_clicked)
        
        ax_save = plt.axes([0.8, 0.08, 0.15, 0.08])
        ax_save.set_facecolor(self.panel_color)
        btn_save = Button(ax_save, '💾 PNG', color='#9900cc', hovercolor='#cc00ff')
        btn_save.label.set_color(self.text_color)
        btn_save.label.set_fontsize(11)
        btn_save.label.set_weight('bold')
        btn_save.on_clicked(self.save_image)
        
        # === INFORMATIONS-PANEL (Unten) ===
        self.fig.text(0.05, 0.02, 'Status: Bereit', color=self.accent_color, 
                     fontsize=10, weight='bold', family='monospace')
        self.status_text = self.fig.text(0.3, 0.02, '', color=self.text_color, 
                                        fontsize=9, family='monospace')
    
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
            print("❌ Fehler: Bitte geben Sie gültige Zahlen ein!")
    
    def compute_and_display(self):
        """Berechnet die Mandelbrot-Menge und zeigt sie an."""
        print(f"\n⏳ Berechne Mandelbrot-Menge ({self.width}x{self.height})...")
        self.status_text.set_text(f'⏳ Berechne... ({self.width}x{self.height})')
        self.fig.canvas.draw_idle()
        
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
        self.status_text.set_text(f'✓ Set #{self.current_set_id} berechnet und gespeichert')
        
        # Visualisiere
        self.display()
    
    def display(self):
        """Zeigt die Mandelbrot-Menge an."""
        if self.mandelbrot_set is None:
            return
        
        self.ax_mandelbrot.clear()
        
        # Verwende logarithmische Skalierung für bessere Farbverteilung
        norm = colors.PowerNorm(gamma=0.3, vmin=0, vmax=self.max_iterations)
        
        # Zeige das Bild mit Rainbow-Colormap an
        self.im = self.ax_mandelbrot.imshow(
            self.mandelbrot_set,
            extent=[self.min_real, self.max_real, self.min_imag, self.max_imag],
            cmap=self.rainbow_cmap,
            origin='lower',
            norm=norm,
            interpolation='bilinear'
        )
        
        # Styling
        self.ax_mandelbrot.set_xlabel('Reelle Achse', color=self.accent_color, fontsize=11, weight='bold')
        self.ax_mandelbrot.set_ylabel('Imaginäre Achse', color=self.accent_color, fontsize=11, weight='bold')
        self.ax_mandelbrot.set_title(f'Mandelbrot-Menge | Set #{self.current_set_id}', 
                                    color=self.text_color, fontsize=13, weight='bold', pad=20)
        
        # Achsen-Styling
        self.ax_mandelbrot.spines['bottom'].set_color(self.accent_color)
        self.ax_mandelbrot.spines['left'].set_color(self.accent_color)
        self.ax_mandelbrot.spines['top'].set_visible(False)
        self.ax_mandelbrot.spines['right'].set_visible(False)
        self.ax_mandelbrot.tick_params(colors=self.text_color, labelsize=9)
        self.ax_mandelbrot.set_facecolor(self.panel_color)
        
        # Colorbar
        cbar = plt.colorbar(self.im, ax=self.ax_mandelbrot, label='Iterationen', pad=0.02)
        cbar.set_label('Iterationen bis Divergenz', color=self.accent_color, fontsize=10, weight='bold')
        cbar.ax.tick_params(colors=self.text_color)
        
        plt.draw()
    
    def save_image(self, event):
        """Speichert das aktuelle Bild als PNG."""
        if self.mandelbrot_set is None:
            print("❌ Keine Mandelbrot-Menge zu speichern!")
            self.status_text.set_text('❌ Bitte zuerst berechnen!')
            return
        
        filename = f"mandelbrot_{self.current_set_id}.png"
        self.fig.savefig(filename, dpi=150, bbox_inches='tight', facecolor=self.bg_color)
        print(f"✓ Bild gespeichert als: {filename}")
        self.status_text.set_text(f'✓ PNG gespeichert: {filename}')
    
    def show(self):
        """Zeigt die interaktive Visualisierung an."""
        print("\n" + "="*60)
        print("🌀 MANDELBROT-MENGE VISUALIZER (Moderne UI)")
        print("="*60)
        
        # Berechne initial die Vollständige Menge
        self.compute_and_display()
        plt.show()
    
    def __del__(self):
        """Cleanup bei Objektzerstörung."""
        self.db.close()


def main():
    """Hauptfunktion."""
    visualizer = MandelbrotVisualizer(width=1200, height=800, max_iterations=256)
    visualizer.show()


if __name__ == '__main__':
    main()
