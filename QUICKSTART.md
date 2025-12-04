# 🚀 Inicio Rápido - Sistema de Control de Plantas

## ⚡ Ejecución Inmediata

### Opción 1: Docker Compose (Más Fácil)
```bash
docker-compose up --build
```
Los servicios estarán disponibles en:
- Plantas: http://localhost:5001
- Cuidados: http://localhost:5002

### Opción 2: Ejecución Local

**Instalar dependencias (solo primera vez)**:
```bash
cd plantas-service
pip install -r requirements.txt
cd ../cuidados-service
pip install -r requirements.txt
cd ..
```

**Ejecutar servicios** (en terminales separadas):
```bash
# Terminal 1
cd plantas-service
python app.py

# Terminal 2
cd cuidados-service
python app.py
```

---

## 🧪 Ejecutar Pruebas

```bash
# Windows
.\run_tests.ps1

# Linux/Mac
./run_tests.sh

# Manual
cd plantas-service && pytest tests/ -v
cd ../cuidados-service && pytest tests/ -v
```

---

## 📡 Probar la API

### Con curl:
```bash
# Health check
curl http://localhost:5001/health
curl http://localhost:5002/health

# Crear planta
curl -X POST http://localhost:5001/api/plantas \
  -H "Content-Type: application/json" \
  -d "{\"nombre\":\"Monstera\",\"tipo\":\"Interior\",\"ubicacion\":\"Sala\",\"frecuencia_riego_dias\":7}"

# Listar plantas
curl http://localhost:5001/api/plantas

# Registrar riego
curl -X POST http://localhost:5002/api/cuidados/riego \
  -H "Content-Type: application/json" \
  -d "{\"planta_id\":1,\"cantidad_ml\":500,\"notas\":\"Riego regular\"}"
```

### Con Postman/Thunder Client:
Ver `API_EXAMPLES.md` para todos los endpoints disponibles.

---

## 📦 Estructura del Proyecto

```
PythonProject/
├── plantas-service/          # Microservicio de Plantas
│   ├── app.py               # API REST
│   ├── models.py            # Modelos de datos
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       └── test_plantas.py  # 13 pruebas
│
├── cuidados-service/         # Microservicio de Cuidados
│   ├── app.py
│   ├── models.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── tests/
│       └── test_cuidados.py # 18 pruebas
│
├── docker-compose.yml        # Orquestación de servicios
├── render.yaml              # Configuración para Render
├── README.md                # Documentación general
├── DOCUMENTATION.md         # Documentación técnica completa
├── DEPLOYMENT.md            # Guía de despliegue
└── API_EXAMPLES.md          # Ejemplos de uso de la API
```

---

## ✅ Checklist de Requisitos

- [x] API REST funcionando
- [x] Endpoints probados (ver API_EXAMPLES.md)
- [x] Arquitectura de microservicios (2 servicios separados)
- [x] Docker (Dockerfile para cada servicio)
- [x] Docker Compose (orquestación)
- [x] Despliegue en la nube (Render - ver DEPLOYMENT.md)
- [x] Pruebas unitarias automáticas (31 pruebas en total)
- [x] Lenguaje: Python con Flask
- [x] Formato JSON en respuestas
- [x] Verbos HTTP correctos (GET, POST, PUT, DELETE)
- [x] Documentación completa

---

## 📚 Documentación Adicional

- **README.md** - Visión general del proyecto
- **DOCUMENTATION.md** - Documentación técnica completa
- **API_EXAMPLES.md** - Ejemplos de uso de todos los endpoints
- **DEPLOYMENT.md** - Guía de despliegue en Render

---

## 🎯 Endpoints Principales

### Servicio de Plantas (5001)
- `GET /api/plantas` - Listar plantas
- `POST /api/plantas` - Crear planta
- `PUT /api/plantas/{id}` - Actualizar planta
- `DELETE /api/plantas/{id}` - Eliminar planta

### Servicio de Cuidados (5002)
- `GET /api/cuidados` - Listar cuidados
- `POST /api/cuidados/riego` - Registrar riego
- `POST /api/cuidados/fertilizacion` - Registrar fertilización
- `POST /api/cuidados/general` - Registrar cuidado general

---

## 💡 Resultados de Pruebas

```
Servicio de Plantas: 13 pruebas pasadas ✅
Servicio de Cuidados: 18 pruebas pasadas ✅
Total: 31 pruebas pasadas ✅
```

---

## 🔗 Despliegue en Render

1. Conecta tu repositorio GitHub a Render
2. Render detectará automáticamente `render.yaml`
3. Los servicios se desplegarán automáticamente

Ver `DEPLOYMENT.md` para instrucciones detalladas.

---

## 👨‍💻 Desarrollo

**Profesor**: Arle Morales Ortiz  
**Programa**: Ingeniería de Software  
**Tema**: API REST con Microservicios y DevOps  
**Proyecto**: Control de Plantas - Riegos, Fertilización y Cuidados

