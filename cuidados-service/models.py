"""
Modelos de datos para el servicio de Cuidados (SQLite)
"""
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'cuidados.db')

class CuidadoManager:
    """Gestor de cuidados usando SQLite"""

    def __init__(self):
        self._ensure_db()

    def _get_conn(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_db(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS cuidados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                planta_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                cantidad_ml REAL,
                tipo_fertilizante TEXT,
                cantidad TEXT,
                descripcion TEXT,
                notas TEXT,
                fecha TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def _row_to_dict(self, row) -> dict:
        if row is None:
            return None
        return {k: row[k] for k in row.keys()}

    def registrar_riego(self, planta_id: int, cantidad_ml: float, notas: str = "") -> dict:
        now = datetime.now().isoformat()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO cuidados (planta_id, tipo, cantidad_ml, notas, fecha)
            VALUES (?, 'riego', ?, ?, ?)
        ''', (planta_id, cantidad_ml, notas, now))
        conn.commit()
        last_id = cur.lastrowid
        cur.execute('SELECT * FROM cuidados WHERE id = ?', (last_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_dict(row)

    def registrar_fertilizacion(self, planta_id: int, tipo_fertilizante: str,
                                cantidad: str, notas: str = "") -> dict:
        now = datetime.now().isoformat()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO cuidados (planta_id, tipo, tipo_fertilizante, cantidad, notas, fecha)
            VALUES (?, 'fertilizacion', ?, ?, ?, ?)
        ''', (planta_id, tipo_fertilizante, cantidad, notas, now))
        conn.commit()
        last_id = cur.lastrowid
        cur.execute('SELECT * FROM cuidados WHERE id = ?', (last_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_dict(row)

    def registrar_cuidado_general(self, planta_id: int, descripcion: str,
                                  notas: str = "") -> dict:
        now = datetime.now().isoformat()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO cuidados (planta_id, tipo, descripcion, notas, fecha)
            VALUES (?, 'general', ?, ?, ?)
        ''', (planta_id, descripcion, notas, now))
        conn.commit()
        last_id = cur.lastrowid
        cur.execute('SELECT * FROM cuidados WHERE id = ?', (last_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_dict(row)

    def get_all(self) -> List[dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM cuidados ORDER BY id')
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]

    def get_by_id(self, cuidado_id: int) -> Optional[dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM cuidados WHERE id = ?', (cuidado_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_dict(row)

    def get_by_planta(self, planta_id: int) -> List[dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM cuidados WHERE planta_id = ? ORDER BY id', (planta_id,))
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]

    def delete(self, cuidado_id: int) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM cuidados WHERE id = ?', (cuidado_id,))
        conn.commit()
        affected = cur.rowcount
        conn.close()
        return affected > 0
