# Mandelbrot-Menge Visualizer

Ein vollständiges Python-Programm zur grafischen Veranschaulichung der Mandelbrot-Menge mit interaktiver Visualisierung und SQLite-Datenbank-Speicherung.

## 📋 Features

- **Interaktive Visualisierung**: Erkunden Sie die Mandelbrot-Menge mit Zoom und benutzerdefinierten Bereichen
- **SQLite-Datenbank**: Alle Berechnungen und Pixel-Daten werden automatisch gespeichert
- **Vordefinierte Zoom-Level**: Seahorse Valley, Spirale, Elephant Valley und mehr
- **Optimierte Berechnung**: Nutzt Numba JIT-Compilation für schnelle Berechnungen
- **Datenanalyse**: Statistiken, Export und Visualisierung gespeicherter Daten

## 🚀 Installation

### Voraussetzungen
- Python 3.8+
- pip oder conda

### Setup

```bash
# 1. Repository klonen
git clone https://github.com/SelbJ08/Mandelbrot.git
cd Mandelbrot

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# Alternativ mit numba für beschleunigte Berechnung:
pip install -r requirements.txt numba
```

## 📚 Verwendung

### 1. Interaktiver Visualizer starten

```bash
python visualizer.py
```

**Bedienung:**
- **Vordefinierte Zoom-Level**: Klicken Sie auf die Buttons (Vollständig, Seahorse, Spirale, Elephant)
- **Benutzerdefinierte Bereiche**: Geben Sie Werte ein und klicken Sie "Berechnen und Speichern"
- **Bild speichern**: Klicken Sie "Als PNG Speichern" um das Bild zu exportieren

### 2. Daten analysieren

```bash
# Alle gespeicherten Mandelbrot-Sets auflisten
python data_manager.py list

# Statistiken für ein Set anzeigen (z.B. Set #1)
python data_manager.py stats 1

# Ein gespeichertes Set visualisieren
python data_manager.py view 1

# Ein Set als numpy-Datei exportieren
python data_manager.py export 1 mein_set.npy
```

## 📊 Projektstruktur

```
Mandelbrot/
├── visualizer.py              # Hauptinteraktives GUI
├── mandelbrot_calculator.py   # Berechnungsmodul
├── database.py                # SQLite-Datenbank-Manager
├── data_manager.py            # Datenanalyse und Export
├── requirements.txt           # Python-Abhängigkeiten
└── README.md                  # Diese Datei
```

## 🗄️ Datenbankstruktur

Die SQLite-Datenbank speichert:

### Tabelle: `mandelbrot_sets`
- `id`: Eindeutige ID des Sets
- `created_at`: Zeitstempel der Erstellung
- `min_real, max_real, min_imag, max_imag`: Bereichsgrenzen
- `width, height`: Auflösung
- `max_iterations`: Maximale Iterationen
- `description`: Beschreibung des Sets

### Tabelle: `pixel_data`
- `mandelbrot_set_id`: Referenz zum Set
- `x, y`: Pixel-Koordinaten
- `iterations`: Anzahl Iterationen bis zur Divergenz

## 🎨 Farben und Visualisierung

- **Heiße Farben** (Hot Colormap): Dunkles Rot für die Mandelbrot-Menge, helle Farben für schnelle Divergenz
- **Logarithmische Skalierung**: Bessere Farbverteilung für detailreiche Visualisierung

## 📐 Mathematik

Die Mandelbrot-Menge wird definiert durch die iterative Funktion:

```
z_{n+1} = z_n² + c
z_0 = 0
```

Wobei `c` eine komplexe Zahl ist. Ein Punkt gehört zur Mandelbrot-Menge, wenn die Folge nicht gegen Unendlich divergiert.

**Divergenz-Kriterium**: |z| > 2

## 💡 Beispiele

### Beispiel 1: Vollständige Menge erkunden
```python
python visualizer.py
# Klicke "Vollständig" um die gesamte Mandelbrot-Menge zu sehen
```

### Beispiel 2: Spezifischen Bereich berechnen
```python
# Gebe folgende Werte ein:
# Min Real: -0.75
# Max Real: -0.735
# Min Imag: 0.095
# Max Imag: 0.11
# Klicke "Berechnen und Speichern"
```

### Beispiel 3: Gespeicherte Daten analysieren
```bash
python data_manager.py list
# Output zeigt alle Sets

python data_manager.py stats 1
# Zeigt detaillierte Statistiken
```

## ⚙️ Performance-Tipps

- **Auflösung**: Niedrigere Auflösungen (z.B. 640x480) für schnellere Berechnungen
- **Max-Iterationen**: Niedrigere Werte für schnellere Ergebnisse (64-128 statt 256)
- **Numba**: Mit JIT-Compiler deutlich schneller (~100x) als reine Python

## 📖 Weiterführende Ressourcen

- [Wikipedia: Mandelbrot-Menge](https://de.wikipedia.org/wiki/Mandelbrot-Menge)
- [Mandelbrot Set Interactive Explorer](https://www.fractalexplorer.app/)
- [Numba Documentation](https://numba.readthedocs.io/)

## 📝 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## 👨‍💻 Autor

Erstellt als interaktives Lernprojekt zur Visualisierung mathematischer Konzepte.

---

**Viel Spaß beim Erkunden der Mandelbrot-Menge!** 🌀
