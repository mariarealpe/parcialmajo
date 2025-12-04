"""
Pruebas unitarias para el Servicio de Cuidados
"""
import pytest
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models import CuidadoManager

@pytest.fixture
def client():
    """Fixture para el cliente de pruebas"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def cuidado_manager():
    """Fixture para el gestor de cuidados"""
    return CuidadoManager()

class TestCuidadoManager:
    """Pruebas para CuidadoManager"""

    def test_registrar_riego(self, cuidado_manager):
        """Test: Registrar un riego"""
        cuidado = cuidado_manager.registrar_riego(
            planta_id=1,
            cantidad_ml=500,
            notas="Riego regular"
        )

        assert cuidado['id'] == 1
        assert cuidado['tipo'] == 'riego'
        assert cuidado['planta_id'] == 1
        assert cuidado['cantidad_ml'] == 500
        assert cuidado['notas'] == "Riego regular"

    def test_registrar_fertilizacion(self, cuidado_manager):
        """Test: Registrar una fertilización"""
        cuidado = cuidado_manager.registrar_fertilizacion(
            planta_id=1,
            tipo_fertilizante="Orgánico",
            cantidad="10ml",
            notas="Fertilizante líquido"
        )

        assert cuidado['id'] == 1
        assert cuidado['tipo'] == 'fertilizacion'
        assert cuidado['tipo_fertilizante'] == "Orgánico"
        assert cuidado['cantidad'] == "10ml"

    def test_registrar_cuidado_general(self, cuidado_manager):
        """Test: Registrar un cuidado general"""
        cuidado = cuidado_manager.registrar_cuidado_general(
            planta_id=1,
            descripcion="Poda de hojas secas",
            notas="Podadas 3 hojas"
        )

        assert cuidado['id'] == 1
        assert cuidado['tipo'] == 'general'
        assert cuidado['descripcion'] == "Poda de hojas secas"

    def test_obtener_todos_los_cuidados(self, cuidado_manager):
        """Test: Obtener todos los cuidados"""
        cuidado_manager.registrar_riego(1, 300, "Riego 1")
        cuidado_manager.registrar_riego(2, 400, "Riego 2")
        cuidado_manager.registrar_fertilizacion(1, "Químico", "5ml", "Fertilización")

        cuidados = cuidado_manager.get_all()
        assert len(cuidados) == 3

    def test_obtener_cuidado_por_id(self, cuidado_manager):
        """Test: Obtener cuidado por ID"""
        cuidado = cuidado_manager.registrar_riego(1, 500, "Riego test")

        encontrado = cuidado_manager.get_by_id(cuidado['id'])
        assert encontrado is not None
        assert encontrado['cantidad_ml'] == 500

    def test_obtener_cuidados_por_planta(self, cuidado_manager):
        """Test: Obtener cuidados de una planta específica"""
        cuidado_manager.registrar_riego(1, 300, "Riego planta 1")
        cuidado_manager.registrar_riego(1, 350, "Otro riego planta 1")
        cuidado_manager.registrar_riego(2, 400, "Riego planta 2")

        cuidados_planta_1 = cuidado_manager.get_by_planta(1)
        assert len(cuidados_planta_1) == 2

        cuidados_planta_2 = cuidado_manager.get_by_planta(2)
        assert len(cuidados_planta_2) == 1

    def test_eliminar_cuidado(self, cuidado_manager):
        """Test: Eliminar registro de cuidado"""
        cuidado = cuidado_manager.registrar_riego(1, 500, "Riego temporal")

        resultado = cuidado_manager.delete(cuidado['id'])
        assert resultado is True

        eliminado = cuidado_manager.get_by_id(cuidado['id'])
        assert eliminado is None

class TestCuidadosAPI:
    """Pruebas para los endpoints de la API"""

    def test_health_check(self, client):
        """Test: Health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'cuidados-service'

    def test_get_cuidados_vacio(self, client):
        """Test: Obtener cuidados cuando la lista está vacía"""
        response = client.get('/api/cuidados')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)

    def test_registrar_riego_exitoso(self, client):
        """Test: Registrar riego exitosamente"""
        riego = {
            'planta_id': 1,
            'cantidad_ml': 500,
            'notas': 'Riego matutino'
        }

        response = client.post('/api/cuidados/riego', json=riego)
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['tipo'] == 'riego'
        assert data['data']['cantidad_ml'] == 500

    def test_registrar_riego_sin_planta_id(self, client):
        """Test: Registrar riego sin planta_id"""
        riego = {
            'cantidad_ml': 500
        }

        response = client.post('/api/cuidados/riego', json=riego)
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_registrar_fertilizacion_exitoso(self, client):
        """Test: Registrar fertilización exitosamente"""
        fertilizacion = {
            'planta_id': 1,
            'tipo_fertilizante': 'Orgánico',
            'cantidad': '15ml',
            'notas': 'Fertilizante de compost'
        }

        response = client.post('/api/cuidados/fertilizacion', json=fertilizacion)
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['tipo'] == 'fertilizacion'
        assert data['data']['tipo_fertilizante'] == 'Orgánico'

    def test_registrar_cuidado_general_exitoso(self, client):
        """Test: Registrar cuidado general exitosamente"""
        cuidado = {
            'planta_id': 1,
            'descripcion': 'Trasplante a maceta más grande',
            'notas': 'Usada tierra orgánica'
        }

        response = client.post('/api/cuidados/general', json=cuidado)
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['tipo'] == 'general'
        assert data['data']['descripcion'] == 'Trasplante a maceta más grande'

    def test_obtener_cuidado_por_id(self, client):
        """Test: Obtener cuidado específico por ID"""
        # Primero crear un cuidado
        riego = {
            'planta_id': 1,
            'cantidad_ml': 400,
            'notas': 'Riego test'
        }
        create_response = client.post('/api/cuidados/riego', json=riego)
        cuidado_id = create_response.get_json()['data']['id']

        # Luego obtenerlo
        response = client.get(f'/api/cuidados/{cuidado_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['cantidad_ml'] == 400

    def test_obtener_cuidados_por_planta(self, client):
        """Test: Obtener todos los cuidados de una planta"""
        # Crear varios cuidados para la misma planta
        client.post('/api/cuidados/riego', json={
            'planta_id': 5,
            'cantidad_ml': 300,
            'notas': 'Riego 1'
        })
        client.post('/api/cuidados/fertilizacion', json={
            'planta_id': 5,
            'tipo_fertilizante': 'Químico',
            'cantidad': '10ml',
            'notas': 'Fertilización 1'
        })

        response = client.get('/api/cuidados/planta/5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['count'] == 2
        assert data['planta_id'] == 5

    def test_eliminar_cuidado(self, client):
        """Test: Eliminar registro de cuidado"""
        # Crear cuidado
        riego = {
            'planta_id': 1,
            'cantidad_ml': 500,
            'notas': 'Riego temporal'
        }
        create_response = client.post('/api/cuidados/riego', json=riego)
        cuidado_id = create_response.get_json()['data']['id']

        # Eliminar
        response = client.delete(f'/api/cuidados/{cuidado_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

        # Verificar que ya no existe
        get_response = client.get(f'/api/cuidados/{cuidado_id}')
        assert get_response.status_code == 404

    def test_obtener_cuidado_inexistente(self, client):
        """Test: Obtener cuidado que no existe"""
        response = client.get('/api/cuidados/9999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False

    def test_validacion_cantidad_ml_negativa(self, client):
        """Test: Validar que cantidad_ml no puede ser negativa"""
        riego = {
            'planta_id': 1,
            'cantidad_ml': -100,
            'notas': 'Riego inválido'
        }

        response = client.post('/api/cuidados/riego', json=riego)
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

