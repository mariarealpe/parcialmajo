# 🌱 Sistema de Control de Plantas - Microservicios

Sistema completo de gestión de plantas con control de riegos, fertilización y cuidados, implementado con arquitectura de microservicios, Docker y despliegue en la nube.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![Tests](https://img.shields.io/badge/Tests-31%20Passed-success.svg)

## 🎯 Características

✅ **API REST** completa con respuestas JSON  
✅ **Arquitectura de Microservicios** (2 servicios independientes)  
✅ **Dockerización** con Docker Compose  
✅ **Pruebas Unitarias** (31 pruebas automatizadas)  
✅ **Despliegue en la Nube** (Render)  
✅ **Documentación Completa** de API  
✅ **Código Limpio** y bien estructurado  

## 🏗️ Arquitectura

El proyecto consta de 2 microservicios independientes:

1. **Servicio de Plantas** (Puerto 5001): Gestión CRUD de plantas
2. **Servicio de Cuidados** (Puerto 5002): Gestión de riegos, fertilización y cuidados

## 🛠️ Tecnologías

- **Lenguaje**: Python 3.11+
- **Framework**: Flask 3.0.0
- **Testing**: pytest 7.4.3
- **Containerización**: Docker & Docker Compose
- **Despliegue**: Render (Web Services)
- **API**: REST con JSON

## Estructura del Proyecto

```
.
├── plantas-service/          # Microservicio de Plantas
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── cuidados-service/         # Microservicio de Cuidados
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Servicio de Plantas (Puerto 5001)

- `GET /api/plantas` - Listar todas las plantas
- `GET /api/plantas/{id}` - Obtener una planta específica
- `POST /api/plantas` - Crear nueva planta
- `PUT /api/plantas/{id}` - Actualizar planta
- `DELETE /api/plantas/{id}` - Eliminar planta
- `GET /health` - Health check

### Servicio de Cuidados (Puerto 5002)

- `GET /api/cuidados` - Listar todos los cuidados
- `GET /api/cuidados/{id}` - Obtener un cuidado específico
- `GET /api/cuidados/planta/{planta_id}` - Obtener cuidados de una planta
- `POST /api/cuidados/riego` - Registrar riego
- `POST /api/cuidados/fertilizacion` - Registrar fertilización
- `POST /api/cuidados/general` - Registrar cuidado general
- `DELETE /api/cuidados/{id}` - Eliminar registro de cuidado
- `GET /health` - Health check

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd PythonProject

# Iniciar servicios
docker-compose up --build
```

Servicios disponibles en:
- 🌱 Plantas: http://localhost:5001
- 💧 Cuidados: http://localhost:5002

### Opción 2: Ejecución Local

**Terminal 1 - Servicio de Plantas:**
```bash
cd plantas-service
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Servicio de Cuidados:**
```bash
cd cuidados-service
pip install -r requirements.txt
python app.py
```

## 🧪 Pruebas Unitarias

```bash
# Windows PowerShell
.\run_tests.ps1

# Linux/Mac
./run_tests.sh

# Manual
cd plantas-service && pytest tests/ -v
cd ../cuidados-service && pytest tests/ -v
```

**Resultados**: ✅ 31 pruebas pasadas (13 + 18)

## Ejemplos de Uso

### Crear una Planta
```bash
curl -X POST http://localhost:5001/api/plantas \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Monstera Deliciosa",
    "tipo": "Interior",
    "ubicacion": "Sala",
    "frecuencia_riego_dias": 7
  }'
```

### Registrar Riego
```bash
curl -X POST http://localhost:5002/api/cuidados/riego \
  -H "Content-Type: application/json" \
  -d '{
    "planta_id": 1,
    "cantidad_ml": 500,
    "notas": "Riego regular"
  }'
```

### Registrar Fertilización
```bash
curl -X POST http://localhost:5002/api/cuidados/fertilizacion \
  -H "Content-Type: application/json" \
  -d '{
    "planta_id": 1,
    "tipo_fertilizante": "Orgánico",
    "cantidad": "10ml",
    "notas": "Fertilizante líquido"
  }'
```

## 📡 Uso de la API

### Crear una Planta
```bash
curl -X POST http://localhost:5001/api/plantas \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Monstera Deliciosa",
    "tipo": "Interior",
    "ubicacion": "Sala",
    "frecuencia_riego_dias": 7
  }'
```

### Listar Plantas
```bash
curl http://localhost:5001/api/plantas
```

### Registrar Riego
```bash
curl -X POST http://localhost:5002/api/cuidados/riego \
  -H "Content-Type: application/json" \
  -d '{
    "planta_id": 1,
    "cantidad_ml": 500,
    "notas": "Riego matutino"
  }'
```

### Registrar Fertilización
```bash
curl -X POST http://localhost:5002/api/cuidados/fertilizacion \
  -H "Content-Type: application/json" \
  -d '{
    "planta_id": 1,
    "tipo_fertilizante": "Orgánico",
    "cantidad": "10ml",
    "notas": "Fertilizante líquido"
  }'
```

Ver **API_EXAMPLES.md** para todos los endpoints disponibles.

## ☁️ Despliegue en Render

El proyecto incluye configuración para despliegue automático en Render:

1. Conecta tu repositorio a Render
2. Render detectará el archivo `render.yaml`
3. Los servicios se desplegarán automáticamente

Ver **DEPLOYMENT.md** para instrucciones detalladas.

## 📚 Documentación

- **QUICKSTART.md** - Guía de inicio rápido
- **DOCUMENTATION.md** - Documentación técnica completa
- **API_EXAMPLES.md** - Ejemplos de todos los endpoints
- **DEPLOYMENT.md** - Guía de despliegue en Render

## 📋 Checklist del Proyecto

- [x] API REST funcionando con JSON
- [x] Arquitectura de microservicios (2 servicios)
- [x] Docker & Docker Compose
- [x] Pruebas unitarias (31 pruebas)
- [x] Despliegue en la nube (Render)
- [x] Verbos HTTP correctos (GET, POST, PUT, DELETE)
- [x] Endpoints documentados
- [x] Health checks implementados
- [x] Código limpio y estructurado

## 👨‍💻 Desarrollo

**Proyecto**: Control de Plantas - Riegos, Fertilización y Cuidados  
**Curso**: API REST con Microservicios y DevOps  
**Profesor**: Arle Morales Ortiz  
**Programa**: Ingeniería de Software  
**Año**: 2025

---

⭐ **Si te gusta este proyecto, dale una estrella!**

