"""
Modelos de datos para el servicio de Plantas (SQLite)
"""
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'plantas.db')

class PlantaManager:
    """Gestor de plantas usando SQLite"""

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
            CREATE TABLE IF NOT EXISTS plantas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                frecuencia_riego_dias INTEGER NOT NULL,
                fecha_creacion TEXT NOT NULL,
                fecha_actualizacion TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def _row_to_dict(self, row) -> dict:
        if row is None:
            return None
        return {k: row[k] for k in row.keys()}

    def create(self, data: dict) -> dict:
        """Crea una nueva planta y devuelve el objeto creado"""
        now = datetime.now().isoformat()
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO plantas (nombre, tipo, ubicacion, frecuencia_riego_dias, fecha_creacion, fecha_actualizacion)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['nombre'], data['tipo'], data['ubicacion'], data['frecuencia_riego_dias'], now, now))
        conn.commit()
        last_id = cur.lastrowid
        cur.execute('SELECT * FROM plantas WHERE id = ?', (last_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_dict(row)

    def get_all(self) -> List[dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM plantas ORDER BY id')
        rows = cur.fetchall()
        conn.close()
        return [self._row_to_dict(r) for r in rows]

    def get_by_id(self, planta_id: int) -> Optional[dict]:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM plantas WHERE id = ?', (planta_id,))
        row = cur.fetchone()
        conn.close()
        return self._row_to_dict(row)

    def update(self, planta_id: int, data: dict) -> Optional[dict]:
        if not self.get_by_id(planta_id):
            return None
        fields = []
        values = []
        allowed = ['nombre', 'tipo', 'ubicacion', 'frecuencia_riego_dias']
        for field in allowed:
            if field in data:
                fields.append(f"{field} = ?")
                values.append(data[field])
        if not fields:
            return self.get_by_id(planta_id)
        values.append(datetime.now().isoformat())
        values.append(planta_id)
        set_clause = ', '.join(fields) + ', fecha_actualizacion = ?'
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(f'UPDATE plantas SET {set_clause} WHERE id = ?', tuple(values))
        conn.commit()
        conn.close()
        return self.get_by_id(planta_id)

    def delete(self, planta_id: int) -> bool:
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM plantas WHERE id = ?', (planta_id,))
        conn.commit()
        affected = cur.rowcount
        conn.close()
        return affected > 0

    def exists(self, planta_id: int) -> bool:
        return self.get_by_id(planta_id) is not None
