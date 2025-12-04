"""
Script para inicializar y poblar la base de datos de Plantas (ejecútalo una vez)
"""
from models import PlantaManager

if __name__ == '__main__':
    pm = PlantaManager()
    # Borrar tablas existentes si quieres (no implementado para seguridad)

    # Crear algunas plantas de ejemplo
    pm.create({
        'nombre': 'Monstera Deliciosa',
        'tipo': 'Interior',
        'ubicacion': 'Sala',
        'frecuencia_riego_dias': 7
    })
    pm.create({
        'nombre': 'Suculenta',
        'tipo': 'Interior',
        'ubicacion': 'Ventana',
        'frecuencia_riego_dias': 14
    })
    print('Bases de datos de plantas inicializada con datos de ejemplo.')

