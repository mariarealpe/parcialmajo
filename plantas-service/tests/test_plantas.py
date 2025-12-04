"""
Pruebas unitarias para el Servicio de Plantas
"""
import pytest
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import PlantaManager

@pytest.fixture
def client():
    """Fixture para el cliente de pruebas"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def planta_manager():
    """Fixture para el gestor de plantas"""
    return PlantaManager()

class TestPlantaManager:
    """Pruebas para PlantaManager"""

    def test_crear_planta(self, planta_manager):
        """Test: Crear una planta"""
        data = {
            'nombre': 'Monstera',
            'tipo': 'Interior',
            'ubicacion': 'Sala',
            'frecuencia_riego_dias': 7
        }
        planta = planta_manager.create(data)

        assert planta['id'] == 1
        assert planta['nombre'] == 'Monstera'
        assert planta['tipo'] == 'Interior'
        assert planta['frecuencia_riego_dias'] == 7

    def test_obtener_todas_las_plantas(self, planta_manager):
        """Test: Obtener todas las plantas"""
        planta_manager.create({
            'nombre': 'Planta 1',
            'tipo': 'Interior',
            'ubicacion': 'Sala',
            'frecuencia_riego_dias': 7
        })
        planta_manager.create({
            'nombre': 'Planta 2',
            'tipo': 'Exterior',
            'ubicacion': 'Jardín',
            'frecuencia_riego_dias': 3
        })

        plantas = planta_manager.get_all()
        assert len(plantas) == 2

    def test_obtener_planta_por_id(self, planta_manager):
        """Test: Obtener planta por ID"""
        planta = planta_manager.create({
            'nombre': 'Suculenta',
            'tipo': 'Interior',
            'ubicacion': 'Ventana',
            'frecuencia_riego_dias': 14
        })

        encontrada = planta_manager.get_by_id(planta['id'])
        assert encontrada is not None
        assert encontrada['nombre'] == 'Suculenta'

    def test_actualizar_planta(self, planta_manager):
        """Test: Actualizar planta"""
        planta = planta_manager.create({
            'nombre': 'Planta Original',
            'tipo': 'Interior',
            'ubicacion': 'Sala',
            'frecuencia_riego_dias': 7
        })

        actualizada = planta_manager.update(planta['id'], {
            'nombre': 'Planta Actualizada',
            'frecuencia_riego_dias': 10
        })

        assert actualizada['nombre'] == 'Planta Actualizada'
        assert actualizada['frecuencia_riego_dias'] == 10
        assert actualizada['tipo'] == 'Interior'  # No cambia

    def test_eliminar_planta(self, planta_manager):
        """Test: Eliminar planta"""
        planta = planta_manager.create({
            'nombre': 'Planta Temporal',
            'tipo': 'Interior',
            'ubicacion': 'Sala',
            'frecuencia_riego_dias': 7
        })

        resultado = planta_manager.delete(planta['id'])
        assert resultado is True

        eliminada = planta_manager.get_by_id(planta['id'])
        assert eliminada is None

class TestPlantasAPI:
    """Pruebas para los endpoints de la API"""

    def test_health_check(self, client):
        """Test: Health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'plantas-service'

    def test_get_plantas_vacio(self, client):
        """Test: Obtener plantas cuando la lista está vacía"""
        response = client.get('/api/plantas')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)

    def test_crear_planta_exitoso(self, client):
        """Test: Crear planta exitosamente"""
        nueva_planta = {
            'nombre': 'Pothos',
            'tipo': 'Interior',
            'ubicacion': 'Cocina',
            'frecuencia_riego_dias': 5
        }

        response = client.post('/api/plantas', json=nueva_planta)
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['nombre'] == 'Pothos'

    def test_crear_planta_sin_campos_requeridos(self, client):
        """Test: Crear planta sin campos requeridos"""
        planta_incompleta = {
            'nombre': 'Planta Incompleta'
        }

        response = client.post('/api/plantas', json=planta_incompleta)
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_obtener_planta_por_id(self, client):
        """Test: Obtener planta específica por ID"""
        # Primero crear una planta
        nueva_planta = {
            'nombre': 'Ficus',
            'tipo': 'Interior',
            'ubicacion': 'Oficina',
            'frecuencia_riego_dias': 7
        }
        create_response = client.post('/api/plantas', json=nueva_planta)
        planta_id = create_response.get_json()['data']['id']

        # Luego obtenerla
        response = client.get(f'/api/plantas/{planta_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['nombre'] == 'Ficus'

    def test_actualizar_planta(self, client):
        """Test: Actualizar planta existente"""
        # Crear planta
        nueva_planta = {
            'nombre': 'Cactus',
            'tipo': 'Interior',
            'ubicacion': 'Ventana',
            'frecuencia_riego_dias': 21
        }
        create_response = client.post('/api/plantas', json=nueva_planta)
        planta_id = create_response.get_json()['data']['id']

        # Actualizar
        actualizacion = {
            'ubicacion': 'Balcón',
            'frecuencia_riego_dias': 28
        }
        response = client.put(f'/api/plantas/{planta_id}', json=actualizacion)
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['ubicacion'] == 'Balcón'
        assert data['data']['frecuencia_riego_dias'] == 28

    def test_eliminar_planta(self, client):
        """Test: Eliminar planta"""
        # Crear planta
        nueva_planta = {
            'nombre': 'Planta Temporal',
            'tipo': 'Exterior',
            'ubicacion': 'Jardín',
            'frecuencia_riego_dias': 3
        }
        create_response = client.post('/api/plantas', json=nueva_planta)
        planta_id = create_response.get_json()['data']['id']

        # Eliminar
        response = client.delete(f'/api/plantas/{planta_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

        # Verificar que ya no existe
        get_response = client.get(f'/api/plantas/{planta_id}')
        assert get_response.status_code == 404

    def test_obtener_planta_inexistente(self, client):
        """Test: Obtener planta que no existe"""
        response = client.get('/api/plantas/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

