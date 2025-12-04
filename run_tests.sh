#!/bin/bash
# Script para ejecutar todas las pruebas del proyecto

echo "========================================"
echo "Ejecutando Pruebas de Microservicios"
echo "========================================"
echo ""

echo "🌱 Pruebas del Servicio de Plantas..."
cd plantas-service
pytest tests/ -v --tb=short
PLANTAS_EXIT=$?
cd ..

echo ""
echo "💧 Pruebas del Servicio de Cuidados..."
cd cuidados-service
pytest tests/ -v --tb=short
CUIDADOS_EXIT=$?
cd ..

echo ""
echo "========================================"
echo "Resumen de Pruebas"
echo "========================================"

if [ $PLANTAS_EXIT -eq 0 ] && [ $CUIDADOS_EXIT -eq 0 ]; then
    echo "✅ Todas las pruebas pasaron exitosamente"
    exit 0
else
    echo "❌ Algunas pruebas fallaron"
    exit 1
fi

