"""
Modul zur Verwaltung der SQLite-Datenbank für Mandelbrot-Daten.
"""

import sqlite3
import os
from datetime import datetime


class MandelbrotDatabase:
    """Verwaltet die SQLite-Datenbank für Mandelbrot-Berechnungen."""
    
    def __init__(self, db_path="mandelbrot_data.db"):
        """Initialisiert die Datenbankverbindung."""
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Erstellt die Datenbankverbindung und initialisiert Tabellen."""
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()
    
    def create_tables(self):
        """Erstellt die notwendigen Tabellen in der Datenbank."""
        cursor = self.conn.cursor()
        
        # Tabelle für berechnete Mandelbrot-Sets
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mandelbrot_sets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                min_real REAL NOT NULL,
                max_real REAL NOT NULL,
                min_imag REAL NOT NULL,
                max_imag REAL NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL,
                max_iterations INTEGER NOT NULL,
                description TEXT
            )
        ''')
        
        # Tabelle für Pixel-Daten (Iterationen bis zur Divergenz)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pixel_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mandelbrot_set_id INTEGER NOT NULL,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                iterations INTEGER NOT NULL,
                FOREIGN KEY (mandelbrot_set_id) REFERENCES mandelbrot_sets(id)
            )
        ''')
        
        self.conn.commit()
    
    def insert_mandelbrot_set(self, min_real, max_real, min_imag, max_imag, 
                             width, height, max_iterations, description=None):
        """
        Speichert Metadaten eines Mandelbrot-Sets in der Datenbank.
        
        Returns:
            int: Die ID des eingefügten Sets
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO mandelbrot_sets 
            (min_real, max_real, min_imag, max_imag, width, height, max_iterations, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (min_real, max_real, min_imag, max_imag, width, height, max_iterations, description))
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_pixel_data(self, mandelbrot_set_id, pixel_array):
        """
        Speichert Pixel-Daten (Iterationen) für ein Mandelbrot-Set.
        
        Args:
            mandelbrot_set_id: ID des Mandelbrot-Sets
            pixel_array: 2D-Array mit Iterationswerten
        """
        cursor = self.conn.cursor()
        height, width = pixel_array.shape
        
        data_tuples = []
        for y in range(height):
            for x in range(width):
                data_tuples.append((mandelbrot_set_id, x, y, int(pixel_array[y, x])))
        
        cursor.executemany('''
            INSERT INTO pixel_data (mandelbrot_set_id, x, y, iterations)
            VALUES (?, ?, ?, ?)
        ''', data_tuples)
        self.conn.commit()
    
    def get_mandelbrot_set(self, set_id):
        """Ruft Metadaten eines Mandelbrot-Sets ab."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM mandelbrot_sets WHERE id = ?
        ''', (set_id,))
        return cursor.fetchone()
    
    def get_pixel_data(self, set_id):
        """Ruft Pixel-Daten für ein Mandelbrot-Set ab."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT x, y, iterations FROM pixel_data WHERE mandelbrot_set_id = ?
            ORDER BY y, x
        ''', (set_id,))
        return cursor.fetchall()
    
    def list_sets(self):
        """Listet alle gespeicherten Mandelbrot-Sets auf."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, created_at, width, height, max_iterations, description 
            FROM mandelbrot_sets 
            ORDER BY created_at DESC
        ''')
        return cursor.fetchall()
    
    def close(self):
        """Schließt die Datenbankverbindung."""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context Manager Support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context Manager Support."""
        self.close()
