# 🎓 GUÍA DE PRESENTACIÓN AL PROFESOR

## Sistema de Control de Plantas - Microservicios

---

## 📋 CHECKLIST ANTES DE LA PRESENTACIÓN

### Preparación Técnica
- [ ] Tener Docker Desktop iniciado (si se usa Docker)
- [ ] Tener los servicios corriendo
- [ ] Tener Postman o Thunder Client abierto
- [ ] Tener este documento abierto
- [ ] Tener terminal lista

### Archivos a Mostrar
- [ ] README.md (visión general)
- [ ] RESUMEN_PROYECTO.md (cumplimiento de requisitos)
- [ ] API_EXAMPLES.md (ejemplos de endpoints)
- [ ] Código fuente (app.py de ambos servicios)
- [ ] Pruebas (test_plantas.py y test_cuidados.py)

---

## 🎯 DEMOSTRACIÓN PASO A PASO

### PASO 1: Mostrar la Arquitectura (2 minutos)

**Explicar**:
- "Implementé 2 microservicios independientes"
- "Servicio de Plantas en puerto 5001 - gestiona el CRUD de plantas"
- "Servicio de Cuidados en puerto 5002 - gestiona riegos, fertilización y cuidados"
- "Cada servicio tiene su propia API REST y almacenamiento"

**Mostrar**: Diagrama en DOCUMENTATION.md

---

### PASO 2: Iniciar Servicios (3 minutos)

**Opción A - Con Docker (Recomendado)**:
```bash
cd C:\Users\MAJO\PycharmProjects\PythonProject
docker-compose up
```

**Opción B - Sin Docker**:
```bash
# Terminal 1
cd C:\Users\MAJO\PycharmProjects\PythonProject\plantas-service
python app.py

# Terminal 2
cd C:\Users\MAJO\PycharmProjects\PythonProject\cuidados-service
python app.py
```

**Verificar**:
- Consola muestra: "🌱 Servicio de Plantas iniciado"
- Consola muestra: "💧 Servicio de Cuidados iniciado"

---

### PASO 3: Demostrar API Funcionando (5 minutos)

#### 3.1 Health Checks
```bash
curl http://localhost:5001/health
curl http://localhost:5002/health
```

**Explicar**: "Cada servicio tiene un health check para monitoreo"

#### 3.2 Crear Planta (POST)
```bash
curl -X POST http://localhost:5001/api/plantas \
  -H "Content-Type: application/json" \
  -d "{\"nombre\":\"Monstera Deliciosa\",\"tipo\":\"Interior\",\"ubicacion\":\"Sala\",\"frecuencia_riego_dias\":7}"
```

**Mostrar**: Respuesta JSON con código 201 y datos de la planta creada

#### 3.3 Listar Plantas (GET)
```bash
curl http://localhost:5001/api/plantas
```

**Explicar**: "La API retorna JSON con todas las plantas y un contador"

#### 3.4 Obtener Planta Específica (GET)
```bash
curl http://localhost:5001/api/plantas/1
```

#### 3.5 Actualizar Planta (PUT)
```bash
curl -X PUT http://localhost:5001/api/plantas/1 \
  -H "Content-Type: application/json" \
  -d "{\"ubicacion\":\"Oficina\",\"frecuencia_riego_dias\":5}"
```

**Explicar**: "Actualización parcial - solo los campos enviados se modifican"

#### 3.6 Registrar Riego (POST)
```bash
curl -X POST http://localhost:5002/api/cuidados/riego \
  -H "Content-Type: application/json" \
  -d "{\"planta_id\":1,\"cantidad_ml\":500,\"notas\":\"Riego matutino\"}"
```

**Explicar**: "El servicio de cuidados registra riegos referenciando el ID de la planta"

#### 3.7 Registrar Fertilización (POST)
```bash
curl -X POST http://localhost:5002/api/cuidados/fertilizacion \
  -H "Content-Type: application/json" \
  -d "{\"planta_id\":1,\"tipo_fertilizante\":\"Orgánico\",\"cantidad\":\"10ml\",\"notas\":\"Fertilizante líquido\"}"
```

#### 3.8 Ver Todos los Cuidados de una Planta (GET)
```bash
curl http://localhost:5002/api/cuidados/planta/1
```

**Explicar**: "Endpoint especializado para ver el historial completo de cuidados de una planta"

#### 3.9 Demostrar Validaciones (POST con error)
```bash
curl -X POST http://localhost:5001/api/plantas \
  -H "Content-Type: application/json" \
  -d "{\"nombre\":\"Planta sin tipo\"}"
```

**Mostrar**: Respuesta 400 con mensaje de error claro

#### 3.10 Eliminar Cuidado (DELETE)
```bash
curl -X DELETE http://localhost:5002/api/cuidados/1
```

**Explicar**: "Confirmación exitosa con código 200"

---

### PASO 4: Demostrar Pruebas Unitarias (3 minutos)

```bash
cd C:\Users\MAJO\PycharmProjects\PythonProject
.\run_tests.ps1
```

O individual:
```bash
cd plantas-service
pytest tests/ -v

cd ../cuidados-service
pytest tests/ -v
```

**Explicar**:
- "31 pruebas automatizadas en total"
- "13 pruebas para el servicio de plantas"
- "18 pruebas para el servicio de cuidados"
- "Incluye pruebas de modelos y de API"
- "Cubre casos de éxito y casos de error"

**Mostrar**: Consola con todas las pruebas pasadas en verde

---

### PASO 5: Mostrar Docker (2 minutos)

#### Mostrar Dockerfiles
```bash
# Abrir en editor
code plantas-service/Dockerfile
code cuidados-service/Dockerfile
```

**Explicar**:
- "Cada servicio tiene su Dockerfile"
- "Basados en Python 3.11-slim"
- "Instalación de dependencias"
- "Puerto expuesto"

#### Mostrar Docker Compose
```bash
code docker-compose.yml
```

**Explicar**:
- "Orquestación de ambos servicios"
- "Red compartida para comunicación"
- "Puertos mapeados: 5001 y 5002"
- "Restart policy configurada"

---

### PASO 6: Mostrar Despliegue en la Nube (2 minutos)

#### Mostrar Configuración
```bash
code render.yaml
```

**Explicar**:
- "Configuración para despliegue automático en Render"
- "Cada servicio se despliega como Web Service independiente"
- "Health checks configurados"
- "Variables de entorno para producción"

#### Mostrar Documentación
```bash
code DEPLOYMENT.md
```

**Explicar**: "Instrucciones completas para desplegar en Render o cualquier otro proveedor"

---

### PASO 7: Mostrar Código Fuente (3 minutos)

#### Servicio de Plantas
```bash
code plantas-service/app.py
```

**Resaltar**:
- Endpoints claros con decoradores Flask
- Validación de datos
- Manejo de errores
- Respuestas JSON estructuradas
- Documentación en comentarios

#### Servicio de Cuidados
```bash
code cuidados-service/app.py
```

**Resaltar**:
- Diferentes tipos de cuidados (riego, fertilización, general)
- Validaciones específicas por tipo
- Endpoint para filtrar por planta

#### Modelos
```bash
code plantas-service/models.py
code cuidados-service/models.py
```

**Resaltar**:
- Separación de lógica de negocio
- Almacenamiento en memoria (PlantaManager, CuidadoManager)
- Métodos CRUD limpios

---

### PASO 8: Mostrar Documentación (1 minuto)

**Mostrar archivos**:
- `README.md` - Visión general
- `DOCUMENTATION.md` - Documentación técnica completa
- `API_EXAMPLES.md` - Todos los endpoints con ejemplos
- `QUICKSTART.md` - Guía de inicio rápido
- `RESUMEN_PROYECTO.md` - Cumplimiento de requisitos

**Explicar**: "Documentación completa para facilitar el uso y mantenimiento del proyecto"

---

## ❓ PREGUNTAS TÉCNICAS ESPERADAS Y RESPUESTAS

### P: ¿Por qué usaste microservicios?
**R**: "Para separar responsabilidades. El servicio de plantas gestiona la información básica, mientras que el servicio de cuidados se enfoca en el historial y seguimiento. Esto permite escalar, mantener y desplegar cada servicio de forma independiente."

### P: ¿Cómo se comunican los microservicios?
**R**: "En esta implementación, los servicios no se comunican directamente entre sí. El cliente (Postman, app frontend) coordina las peticiones. Por ejemplo, primero obtiene el ID de una planta del servicio de plantas, y luego usa ese ID para registrar un riego en el servicio de cuidados. En producción, se podría implementar comunicación mediante API Gateway o eventos."

### P: ¿Por qué no usas base de datos?
**R**: "Para simplificar la demostración, uso almacenamiento en memoria. Esto permite enfocarnos en la arquitectura de microservicios, Docker y las pruebas. En producción, cada servicio tendría su propia base de datos (por ejemplo, PostgreSQL) siguiendo el patrón 'database per service'."

### P: ¿Cómo manejas errores?
**R**: "Cada endpoint valida los datos de entrada, verifica que existan los recursos solicitados, y retorna códigos HTTP apropiados (200, 201, 400, 404, 500) junto con mensajes descriptivos en JSON. Las pruebas unitarias verifican todos estos casos."

### P: ¿Qué pruebas implementaste?
**R**: "31 pruebas automatizadas con pytest:
- Pruebas de modelos (lógica de negocio)
- Pruebas de API (endpoints HTTP)
- Casos de éxito y error
- Validaciones de datos
Todas las pruebas pasan al 100%."

### P: ¿Cómo desplegarías esto en producción?
**R**: "Tengo configuración lista para Render en el archivo render.yaml. Los pasos son:
1. Conectar repositorio GitHub a Render
2. Render detecta automáticamente la configuración
3. Construye imágenes Docker
4. Despliega cada servicio
También funciona en AWS, GCP, Azure o cualquier plataforma que soporte Docker."

### P: ¿Qué es el health check?
**R**: "Un endpoint (/health) que retorna el estado del servicio. Las plataformas de nube lo usan para verificar que el servicio está funcionando y para hacer restart automático si falla."

### P: ¿Por qué Flask y no otro framework?
**R**: "Flask es ligero, rápido de desarrollar y perfecto para microservicios. Para este proyecto de control de plantas, necesitaba algo simple pero robusto. Flask cumple perfectamente. También es una de las opciones permitidas en el curso."

---

## ✅ PUNTOS CLAVE A DESTACAR

1. **Arquitectura**: 2 microservicios completamente independientes
2. **API REST**: 14 endpoints con verbos HTTP correctos
3. **Docker**: Dockerfiles + Docker Compose funcionando
4. **Pruebas**: 31 pruebas automatizadas (100% pasadas)
5. **Despliegue**: Configuración lista para Render
6. **Documentación**: 5 archivos de documentación completa
7. **Código Limpio**: Validaciones, manejo de errores, respuestas estructuradas
8. **JSON**: Todas las respuestas en formato JSON
9. **Health Checks**: Implementados en ambos servicios
10. **Producción Ready**: Variables de entorno, logging, configuración flexible

---

## 🎯 RESUMEN FINAL (30 segundos)

"He desarrollado un sistema completo de control de plantas usando arquitectura de microservicios. Son 2 servicios independientes con 14 endpoints REST, totalmente dockerizados. Incluye 31 pruebas unitarias que pasan al 100%, y está listo para desplegar en la nube con Render. Todo el código está documentado y sigue las mejores prácticas de desarrollo."

---

## 📞 CONTACTO PARA DUDAS

Si el profesor tiene dudas adicionales:
- Mostrar código específico
- Ejecutar pruebas adicionales
- Demostrar casos de uso específicos
- Explicar decisiones de diseño

**¡Buena suerte en tu presentación! 🚀**

