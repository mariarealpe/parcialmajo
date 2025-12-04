"""
Script para inicializar y poblar la base de datos de Cuidados (ejecútalo después de crear plantas)
"""
from models import CuidadoManager

if __name__ == '__main__':
    cm = CuidadoManager()
    # Agregar algunos cuidados de ejemplo (suponer planta_id 1 y 2 existen)
    cm.registrar_riego(planta_id=1, cantidad_ml=300, notas='Riego inicial')
    cm.registrar_fertilizacion(planta_id=1, tipo_fertilizante='Orgánico', cantidad='10ml', notas='Fertilizante mensual')
    cm.registrar_cuidado_general(planta_id=2, descripcion='Trasplante a maceta 12cm', notas='Usar sustrato nuevo')
    print('Base de datos de cuidados inicializada con datos de ejemplo.')

