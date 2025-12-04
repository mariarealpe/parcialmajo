# Colección de Postman para API de Control de Plantas

## Servicio de Plantas (Puerto 5001)

### 1. Health Check
```
GET http://localhost:5001/health
```

### 2. Listar todas las plantas
```
GET http://localhost:5001/api/plantas
```

### 3. Obtener planta específica
```
GET http://localhost:5001/api/plantas/1
```

### 4. Crear nueva planta
```
POST http://localhost:5001/api/plantas
Content-Type: application/json

{
  "nombre": "Monstera Deliciosa",
  "tipo": "Interior",
  "ubicacion": "Sala",
  "frecuencia_riego_dias": 7
}
```

### 5. Actualizar planta
```
PUT http://localhost:5001/api/plantas/1
Content-Type: application/json

{
  "ubicacion": "Oficina",
  "frecuencia_riego_dias": 5
}
```

### 6. Eliminar planta
```
DELETE http://localhost:5001/api/plantas/1
```

---

## Servicio de Cuidados (Puerto 5002)

### 1. Health Check
```
GET http://localhost:5002/health
```

### 2. Listar todos los cuidados
```
GET http://localhost:5002/api/cuidados
```

### 3. Obtener cuidado específico
```
GET http://localhost:5002/api/cuidados/1
```

### 4. Obtener cuidados de una planta
```
GET http://localhost:5002/api/cuidados/planta/1
```

### 5. Registrar riego
```
POST http://localhost:5002/api/cuidados/riego
Content-Type: application/json

{
  "planta_id": 1,
  "cantidad_ml": 500,
  "notas": "Riego matutino regular"
}
```

### 6. Registrar fertilización
```
POST http://localhost:5002/api/cuidados/fertilizacion
Content-Type: application/json

{
  "planta_id": 1,
  "tipo_fertilizante": "Orgánico",
  "cantidad": "10ml",
  "notas": "Fertilizante líquido de compost"
}
```

### 7. Registrar cuidado general
```
POST http://localhost:5002/api/cuidados/general
Content-Type: application/json

{
  "planta_id": 1,
  "descripcion": "Poda de hojas secas",
  "notas": "Se podaron 3 hojas amarillas"
}
```

### 8. Eliminar cuidado
```
DELETE http://localhost:5002/api/cuidados/1
```

---

## Ejemplos de Respuestas

### Respuesta exitosa (POST Planta):
```json
{
  "success": true,
  "message": "Planta creada exitosamente",
  "data": {
    "id": 1,
    "nombre": "Monstera Deliciosa",
    "tipo": "Interior",
    "ubicacion": "Sala",
    "frecuencia_riego_dias": 7,
    "fecha_creacion": "2025-12-04T10:30:00",
    "fecha_actualizacion": "2025-12-04T10:30:00"
  }
}
```

### Respuesta de error (400):
```json
{
  "success": false,
  "message": "Campo requerido faltante: nombre"
}
```

