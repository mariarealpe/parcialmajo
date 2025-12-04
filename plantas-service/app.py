"""
Microservicio de Plantas
Gestiona el CRUD de plantas del sistema
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import PlantaManager
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Inicializar el gestor de plantas
planta_manager = PlantaManager()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'plantas-service',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/plantas', methods=['GET'])
def get_plantas():
    """
    GET /api/plantas
    Obtiene la lista de todas las plantas
    """
    plantas = planta_manager.get_all()
    return jsonify({
        'success': True,
        'data': plantas,
        'count': len(plantas)
    }), 200

@app.route('/api/plantas/<int:planta_id>', methods=['GET'])
def get_planta(planta_id):
    """
    GET /api/plantas/{id}
    Obtiene una planta específica por ID
    """
    planta = planta_manager.get_by_id(planta_id)
    if planta:
        return jsonify({
            'success': True,
            'data': planta
        }), 200
    return jsonify({
        'success': False,
        'message': f'Planta con ID {planta_id} no encontrada'
    }), 404

@app.route('/api/plantas', methods=['POST'])
def create_planta():
    """
    POST /api/plantas
    Crea una nueva planta
    Body: {
        "nombre": "Nombre de la planta",
        "tipo": "Interior/Exterior",
        "ubicacion": "Ubicación",
        "frecuencia_riego_dias": 7
    }
    """
    try:
        data = request.get_json()

        # Validar campos requeridos
        required_fields = ['nombre', 'tipo', 'ubicacion', 'frecuencia_riego_dias']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido faltante: {field}'
                }), 400

        # Validar frecuencia de riego
        if not isinstance(data['frecuencia_riego_dias'], int) or data['frecuencia_riego_dias'] <= 0:
            return jsonify({
                'success': False,
                'message': 'frecuencia_riego_dias debe ser un número entero positivo'
            }), 400

        planta = planta_manager.create(data)
        return jsonify({
            'success': True,
            'message': 'Planta creada exitosamente',
            'data': planta
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al crear planta: {str(e)}'
        }), 500

@app.route('/api/plantas/<int:planta_id>', methods=['PUT'])
def update_planta(planta_id):
    """
    PUT /api/plantas/{id}
    Actualiza una planta existente
    """
    try:
        data = request.get_json()

        # Validar que la planta existe
        if not planta_manager.get_by_id(planta_id):
            return jsonify({
                'success': False,
                'message': f'Planta con ID {planta_id} no encontrada'
            }), 404

        # Validar frecuencia de riego si se proporciona
        if 'frecuencia_riego_dias' in data:
            if not isinstance(data['frecuencia_riego_dias'], int) or data['frecuencia_riego_dias'] <= 0:
                return jsonify({
                    'success': False,
                    'message': 'frecuencia_riego_dias debe ser un número entero positivo'
                }), 400

        planta = planta_manager.update(planta_id, data)
        return jsonify({
            'success': True,
            'message': 'Planta actualizada exitosamente',
            'data': planta
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al actualizar planta: {str(e)}'
        }), 500

@app.route('/api/plantas/<int:planta_id>', methods=['DELETE'])
def delete_planta(planta_id):
    """
    DELETE /api/plantas/{id}
    Elimina una planta
    """
    if planta_manager.delete(planta_id):
        return jsonify({
            'success': True,
            'message': f'Planta con ID {planta_id} eliminada exitosamente'
        }), 200
    return jsonify({
        'success': False,
        'message': f'Planta con ID {planta_id} no encontrada'
    }), 404

@app.route('/')
def index():
    """Ruta raíz: muestra información básica y endpoints del servicio"""
    return jsonify({
        'service': 'plantas-service',
        'success': True,
        'message': 'Servicio de Plantas - endpoints disponibles',
        'endpoints': {
            'health': '/health',
            'listar_plantas': '/api/plantas',
            'obtener_planta': '/api/plantas/{id}',
            'crear_planta': '/api/plantas (POST)'
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Error interno del servidor'
    }), 500

if __name__ == '__main__':
    import os

    # Crear algunas plantas de ejemplo
    planta_manager.create({
        'nombre': 'Monstera Deliciosa',
        'tipo': 'Interior',
        'ubicacion': 'Sala',
        'frecuencia_riego_dias': 7
    })
    planta_manager.create({
        'nombre': 'Suculenta',
        'tipo': 'Interior',
        'ubicacion': 'Ventana',
        'frecuencia_riego_dias': 14
    })

    # Puerto: usa PORT de variable de entorno o 5001 por defecto
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'

    print(f"🌱 Servicio de Plantas iniciado en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
