"""
Microservicio de Cuidados
Gestiona riegos, fertilización y cuidados generales de las plantas
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import CuidadoManager
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Inicializar el gestor de cuidados
cuidado_manager = CuidadoManager()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'cuidados-service',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/cuidados', methods=['GET'])
def get_cuidados():
    """
    GET /api/cuidados
    Obtiene todos los registros de cuidados
    """
    cuidados = cuidado_manager.get_all()
    return jsonify({
        'success': True,
        'data': cuidados,
        'count': len(cuidados)
    }), 200

@app.route('/api/cuidados/<int:cuidado_id>', methods=['GET'])
def get_cuidado(cuidado_id):
    """
    GET /api/cuidados/{id}
    Obtiene un registro de cuidado específico
    """
    cuidado = cuidado_manager.get_by_id(cuidado_id)
    if cuidado:
        return jsonify({
            'success': True,
            'data': cuidado
        }), 200
    return jsonify({
        'success': False,
        'message': f'Cuidado con ID {cuidado_id} no encontrado'
    }), 404

@app.route('/api/cuidados/planta/<int:planta_id>', methods=['GET'])
def get_cuidados_by_planta(planta_id):
    """
    GET /api/cuidados/planta/{planta_id}
    Obtiene todos los cuidados de una planta específica
    """
    cuidados = cuidado_manager.get_by_planta(planta_id)
    return jsonify({
        'success': True,
        'data': cuidados,
        'count': len(cuidados),
        'planta_id': planta_id
    }), 200

@app.route('/api/cuidados/riego', methods=['POST'])
def registrar_riego():
    """
    POST /api/cuidados/riego
    Registra un riego
    Body: {
        "planta_id": 1,
        "cantidad_ml": 500,
        "notas": "Opcional"
    }
    """
    try:
        data = request.get_json()

        # Validar campos requeridos
        if 'planta_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo requerido: planta_id'
            }), 400

        if 'cantidad_ml' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo requerido: cantidad_ml'
            }), 400

        # Validar tipos de datos
        if not isinstance(data['planta_id'], int) or data['planta_id'] <= 0:
            return jsonify({
                'success': False,
                'message': 'planta_id debe ser un número entero positivo'
            }), 400

        if not isinstance(data['cantidad_ml'], (int, float)) or data['cantidad_ml'] <= 0:
            return jsonify({
                'success': False,
                'message': 'cantidad_ml debe ser un número positivo'
            }), 400

        cuidado = cuidado_manager.registrar_riego(
            planta_id=data['planta_id'],
            cantidad_ml=data['cantidad_ml'],
            notas=data.get('notas', '')
        )

        return jsonify({
            'success': True,
            'message': 'Riego registrado exitosamente',
            'data': cuidado
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al registrar riego: {str(e)}'
        }), 500

@app.route('/api/cuidados/fertilizacion', methods=['POST'])
def registrar_fertilizacion():
    """
    POST /api/cuidados/fertilizacion
    Registra una fertilización
    Body: {
        "planta_id": 1,
        "tipo_fertilizante": "Orgánico",
        "cantidad": "10ml",
        "notas": "Opcional"
    }
    """
    try:
        data = request.get_json()

        # Validar campos requeridos
        required_fields = ['planta_id', 'tipo_fertilizante', 'cantidad']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo requerido: {field}'
                }), 400

        # Validar planta_id
        if not isinstance(data['planta_id'], int) or data['planta_id'] <= 0:
            return jsonify({
                'success': False,
                'message': 'planta_id debe ser un número entero positivo'
            }), 400

        cuidado = cuidado_manager.registrar_fertilizacion(
            planta_id=data['planta_id'],
            tipo_fertilizante=data['tipo_fertilizante'],
            cantidad=data['cantidad'],
            notas=data.get('notas', '')
        )

        return jsonify({
            'success': True,
            'message': 'Fertilización registrada exitosamente',
            'data': cuidado
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al registrar fertilización: {str(e)}'
        }), 500

@app.route('/api/cuidados/general', methods=['POST'])
def registrar_cuidado_general():
    """
    POST /api/cuidados/general
    Registra un cuidado general (poda, trasplante, etc.)
    Body: {
        "planta_id": 1,
        "descripcion": "Descripción del cuidado",
        "notas": "Opcional"
    }
    """
    try:
        data = request.get_json()

        # Validar campos requeridos
        if 'planta_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo requerido: planta_id'
            }), 400

        if 'descripcion' not in data:
            return jsonify({
                'success': False,
                'message': 'Campo requerido: descripcion'
            }), 400

        # Validar planta_id
        if not isinstance(data['planta_id'], int) or data['planta_id'] <= 0:
            return jsonify({
                'success': False,
                'message': 'planta_id debe ser un número entero positivo'
            }), 400

        cuidado = cuidado_manager.registrar_cuidado_general(
            planta_id=data['planta_id'],
            descripcion=data['descripcion'],
            notas=data.get('notas', '')
        )

        return jsonify({
            'success': True,
            'message': 'Cuidado general registrado exitosamente',
            'data': cuidado
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al registrar cuidado: {str(e)}'
        }), 500

@app.route('/api/cuidados/<int:cuidado_id>', methods=['DELETE'])
def delete_cuidado(cuidado_id):
    """
    DELETE /api/cuidados/{id}
    Elimina un registro de cuidado
    """
    if cuidado_manager.delete(cuidado_id):
        return jsonify({
            'success': True,
            'message': f'Cuidado con ID {cuidado_id} eliminado exitosamente'
        }), 200
    return jsonify({
        'success': False,
        'message': f'Cuidado con ID {cuidado_id} no encontrado'
    }), 404

@app.route('/')
def index():
    """Ruta raíz: muestra información básica y endpoints del servicio"""
    return jsonify({
        'service': 'cuidados-service',
        'success': True,
        'message': 'Servicio de Cuidados - endpoints disponibles',
        'endpoints': {
            'health': '/health',
            'listar_cuidados': '/api/cuidados',
            'obtener_cuidado': '/api/cuidados/{id}',
            'cuidados_por_planta': '/api/cuidados/planta/{planta_id}',
            'registrar_riego': '/api/cuidados/riego (POST)',
            'registrar_fertilizacion': '/api/cuidados/fertilizacion (POST)'
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

    # Puerto: usa PORT de variable de entorno o 5002 por defecto
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV') != 'production'

    print(f"💧 Servicio de Cuidados iniciado en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
