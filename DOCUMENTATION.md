# Documentación Técnica - Sistema de Control de Plantas

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura](#arquitectura)
3. [Endpoints de la API](#endpoints-de-la-api)
4. [Modelos de Datos](#modelos-de-datos)
5. [Pruebas Unitarias](#pruebas-unitarias)
6. [Despliegue](#despliegue)
7. [Ejecución Local](#ejecución-local)

---

## 📖 Descripción General

Sistema de microservicios para la gestión y control de plantas, incluyendo:
- Registro y gestión de plantas
- Control de riegos
- Registro de fertilización
- Seguimiento de cuidados generales

### Tecnologías Utilizadas
- **Lenguaje**: Python 3.11+
- **Framework**: Flask 3.0.0
- **Testing**: pytest 7.4.3
- **Containerización**: Docker
- **Orquestación**: Docker Compose
- **Despliegue**: Render (Web Services)

---

## 🏗️ Arquitectura

### Arquitectura de Microservicios

```
┌─────────────────────────────────────────────────┐
│                   Cliente                        │
│            (Postman, curl, Browser)              │
└───────────────┬─────────────────┬───────────────┘
                │                 │
                │                 │
        ┌───────▼────────┐  ┌────▼──────────┐
        │  Servicio de   │  │  Servicio de  │
        │    Plantas     │  │   Cuidados    │
        │   (Puerto      │  │   (Puerto     │
        │    5001)       │  │    5002)      │
        └────────────────┘  └───────────────┘
             │                      │
             │                      │
        ┌────▼──────────────────────▼────┐
        │    Almacenamiento en Memoria    │
        │      (PlantaManager /           │
        │       CuidadoManager)           │
        └─────────────────────────────────┘
```

### Separación de Responsabilidades

**Servicio de Plantas**:
- Gestión del CRUD de plantas
- Información básica de cada planta
- Características y ubicación

**Servicio de Cuidados**:
- Registro de riegos
- Registro de fertilización
- Registro de cuidados generales
- Historial de cuidados por planta

### Comunicación

- Los servicios son **independientes** y no se comunican directamente
- Cada servicio tiene su propia API REST
- El cliente coordina la información entre servicios

---

## 🔌 Endpoints de la API

### Servicio de Plantas (Puerto 5001)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check del servicio |
| GET | `/api/plantas` | Listar todas las plantas |
| GET | `/api/plantas/{id}` | Obtener planta específica |
| POST | `/api/plantas` | Crear nueva planta |
| PUT | `/api/plantas/{id}` | Actualizar planta |
| DELETE | `/api/plantas/{id}` | Eliminar planta |

### Servicio de Cuidados (Puerto 5002)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check del servicio |
| GET | `/api/cuidados` | Listar todos los cuidados |
| GET | `/api/cuidados/{id}` | Obtener cuidado específico |
| GET | `/api/cuidados/planta/{planta_id}` | Obtener cuidados de una planta |
| POST | `/api/cuidados/riego` | Registrar riego |
| POST | `/api/cuidados/fertilizacion` | Registrar fertilización |
| POST | `/api/cuidados/general` | Registrar cuidado general |
| DELETE | `/api/cuidados/{id}` | Eliminar cuidado |

---

## 📊 Modelos de Datos

### Planta
```json
{
  "id": 1,
  "nombre": "Monstera Deliciosa",
  "tipo": "Interior",
  "ubicacion": "Sala",
  "frecuencia_riego_dias": 7,
  "fecha_creacion": "2025-12-04T10:30:00",
  "fecha_actualizacion": "2025-12-04T10:30:00"
}
```

### Cuidado - Riego
```json
{
  "id": 1,
  "planta_id": 1,
  "tipo": "riego",
  "cantidad_ml": 500,
  "notas": "Riego matutino",
  "fecha": "2025-12-04T08:00:00"
}
```

### Cuidado - Fertilización
```json
{
  "id": 2,
  "planta_id": 1,
  "tipo": "fertilizacion",
  "tipo_fertilizante": "Orgánico",
  "cantidad": "10ml",
  "notas": "Fertilizante líquido",
  "fecha": "2025-12-04T09:00:00"
}
```

### Cuidado - General
```json
{
  "id": 3,
  "planta_id": 1,
  "tipo": "general",
  "descripcion": "Poda de hojas secas",
  "notas": "3 hojas podadas",
  "fecha": "2025-12-04T10:00:00"
}
```

---

## 🧪 Pruebas Unitarias

### Cobertura de Pruebas

**Servicio de Plantas**: 13 pruebas
- Pruebas de modelo (PlantaManager)
- Pruebas de API (endpoints)
- Validaciones de datos
- Manejo de errores

**Servicio de Cuidados**: 18 pruebas
- Pruebas de modelo (CuidadoManager)
- Pruebas de API (endpoints)
- Validaciones de datos
- Manejo de errores

### Ejecutar Pruebas

**Windows (PowerShell)**:
```powershell
.\run_tests.ps1
```

**Linux/Mac**:
```bash
./run_tests.sh
```

**Individual**:
```bash
# Plantas
cd plantas-service
pytest tests/ -v

# Cuidados
cd cuidados-service
pytest tests/ -v
```

---

## 🚀 Despliegue

### Despliegue en Render

#### Opción 1: Blueprint (render.yaml)
1. Conecta el repositorio a Render
2. Render detectará automáticamente el archivo `render.yaml`
3. Los servicios se desplegarán automáticamente

#### Opción 2: Manual
1. Crear Web Service para `plantas-service`
   - Environment: Docker
   - Root Directory: `plantas-service`
   - Health Check Path: `/health`

2. Crear Web Service para `cuidados-service`
   - Environment: Docker
   - Root Directory: `cuidados-service`
   - Health Check Path: `/health`

### Variables de Entorno

Ambos servicios usan:
- `PORT`: Puerto asignado por Render (automático)
- `FLASK_APP`: `app.py`
- `PYTHONUNBUFFERED`: `1`
- `FLASK_ENV`: `production` (en producción)

---

## 💻 Ejecución Local

### Con Docker Compose (Recomendado)

```bash
# Construir y ejecutar
docker-compose up --build

# Solo ejecutar
docker-compose up

# En background
docker-compose up -d

# Detener
docker-compose down
```

### Sin Docker

**Terminal 1 - Servicio de Plantas**:
```bash
cd plantas-service
pip install -r requirements.txt
python app.py
```

**Terminal 2 - Servicio de Cuidados**:
```bash
cd cuidados-service
pip install -r requirements.txt
python app.py
```

---

## 📝 Buenas Prácticas Implementadas

### Arquitectura
✅ Separación clara de responsabilidades  
✅ Microservicios independientes  
✅ APIs RESTful bien estructuradas  
✅ Uso correcto de verbos HTTP  

### Código
✅ Código limpio y documentado  
✅ Validación de datos de entrada  
✅ Manejo de errores consistente  
✅ Respuestas JSON estructuradas  

### Testing
✅ Pruebas unitarias completas  
✅ Cobertura de casos de éxito y error  
✅ Fixtures reutilizables  
✅ Pruebas independientes  

### DevOps
✅ Dockerización de servicios  
✅ Docker Compose para orquestación  
✅ Health checks implementados  
✅ Variables de entorno configurables  
✅ Listo para CI/CD  

---

## 🔐 Seguridad y Mejoras Futuras

### Para Producción
- [ ] Implementar autenticación JWT
- [ ] Agregar rate limiting
- [ ] Usar base de datos persistente (PostgreSQL)
- [ ] Implementar logging centralizado
- [ ] Agregar métricas y monitoreo
- [ ] Implementar HTTPS
- [ ] Agregar validación de CORS más estricta
- [ ] Implementar paginación en listados

---

## 📞 Contacto y Soporte

Proyecto desarrollado como parte del examen de API REST con Microservicios y DevOps.

**Profesor**: Arle Morales Ortiz  
**Programa**: Ingeniería de Software

---

## 📄 Licencia

Proyecto educativo - 2025

