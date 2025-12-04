# Guía de Despliegue en Render

## Configuración para Plantas Service

### 1. Crear nuevo Web Service en Render
- Conecta tu repositorio de GitHub
- Selecciona la carpeta: `plantas-service`

### 2. Configuración del servicio
```
Name: plantas-service
Environment: Docker
Region: Oregon (US West) o el más cercano
Branch: main
Root Directory: plantas-service
```

### 3. Configuración de Docker
Render detectará automáticamente el Dockerfile.

### 4. Variables de entorno (opcional)
```
FLASK_APP=app.py
PYTHONUNBUFFERED=1
```

### 5. Plan
- Selecciona el plan Free (para desarrollo)

---

## Configuración para Cuidados Service

Repite el mismo proceso pero con:
```
Name: cuidados-service
Root Directory: cuidados-service
```

---

## Notas Importantes

1. **Puerto**: Render asigna automáticamente la variable `PORT`. Si quieres usar el puerto de Render en lugar del hardcodeado (5001/5002), modifica app.py:
   ```python
   import os
   port = int(os.environ.get('PORT', 5001))
   app.run(host='0.0.0.0', port=port, debug=False)
   ```

2. **Health Check**: Render utilizará `/health` para verificar que el servicio está funcionando.

3. **URLs**: Una vez desplegado, Render te proporcionará URLs como:
   - https://plantas-service.onrender.com
   - https://cuidados-service.onrender.com

4. **Base de datos**: Este proyecto usa almacenamiento en memoria. Para producción, considera usar una base de datos persistente.

---

## Testing antes del despliegue

Ejecuta las pruebas localmente:
```bash
cd plantas-service
pytest tests/ -v

cd ../cuidados-service
pytest tests/ -v
```

---

## Verificación Post-Despliegue

Prueba los endpoints:
```bash
# Health check
curl https://plantas-service.onrender.com/health
curl https://cuidados-service.onrender.com/health

# Crear planta
curl -X POST https://plantas-service.onrender.com/api/plantas \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Monstera","tipo":"Interior","ubicacion":"Sala","frecuencia_riego_dias":7}'

# Registrar riego
curl -X POST https://cuidados-service.onrender.com/api/cuidados/riego \
  -H "Content-Type: application/json" \
  -d '{"planta_id":1,"cantidad_ml":500,"notas":"Riego regular"}'
```

