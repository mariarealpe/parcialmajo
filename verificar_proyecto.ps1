# Script de Verificación Pre-Presentación
# Ejecutar este script antes de presentar al profesor

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VERIFICACIÓN PRE-PRESENTACIÓN" -ForegroundColor Cyan
Write-Host "Sistema de Control de Plantas" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# 1. Verificar estructura de archivos
Write-Host "1. Verificando estructura de archivos..." -ForegroundColor Yellow
$requiredFiles = @(
    "README.md",
    "DOCUMENTATION.md",
    "API_EXAMPLES.md",
    "DEPLOYMENT.md",
    "QUICKSTART.md",
    "RESUMEN_PROYECTO.md",
    "GUIA_PRESENTACION.md",
    "docker-compose.yml",
    "render.yaml",
    "plantas-service\app.py",
    "plantas-service\models.py",
    "plantas-service\Dockerfile",
    "plantas-service\requirements.txt",
    "plantas-service\tests\test_plantas.py",
    "cuidados-service\app.py",
    "cuidados-service\models.py",
    "cuidados-service\Dockerfile",
    "cuidados-service\requirements.txt",
    "cuidados-service\tests\test_cuidados.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file - FALTANTE" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""

# 2. Verificar dependencias instaladas
Write-Host "2. Verificando dependencias de Python..." -ForegroundColor Yellow
try {
    pip show Flask | Out-Null
    Write-Host "  ✅ Flask instalado" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Flask no instalado" -ForegroundColor Red
    $allGood = $false
}

try {
    pip show pytest | Out-Null
    Write-Host "  ✅ pytest instalado" -ForegroundColor Green
} catch {
    Write-Host "  ❌ pytest no instalado" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# 3. Ejecutar pruebas
Write-Host "3. Ejecutando pruebas unitarias..." -ForegroundColor Yellow
Write-Host ""

Write-Host "  Pruebas de Plantas Service..." -ForegroundColor Cyan
Set-Location plantas-service
$plantasResult = pytest tests/ -v --tb=short 2>&1
$plantasExit = $LASTEXITCODE
Set-Location ..

if ($plantasExit -eq 0) {
    Write-Host "  ✅ Pruebas de Plantas: PASADAS" -ForegroundColor Green
} else {
    Write-Host "  ❌ Pruebas de Plantas: FALLARON" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""
Write-Host "  Pruebas de Cuidados Service..." -ForegroundColor Cyan
Set-Location cuidados-service
$cuidadosResult = pytest tests/ -v --tb=short 2>&1
$cuidadosExit = $LASTEXITCODE
Set-Location ..

if ($cuidadosExit -eq 0) {
    Write-Host "  ✅ Pruebas de Cuidados: PASADAS" -ForegroundColor Green
} else {
    Write-Host "  ❌ Pruebas de Cuidados: FALLARON" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# 4. Verificar Docker
Write-Host "4. Verificando Docker..." -ForegroundColor Yellow
try {
    docker --version | Out-Null
    Write-Host "  ✅ Docker instalado" -ForegroundColor Green

    # Verificar si Docker está corriendo
    $dockerRunning = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Docker está corriendo" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Docker no está corriendo - iniciar Docker Desktop" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠️  Docker no encontrado - necesario para demostración con contenedores" -ForegroundColor Yellow
}

Write-Host ""

# 5. Verificar git (opcional)
Write-Host "5. Verificando Git..." -ForegroundColor Yellow
try {
    git --version | Out-Null
    Write-Host "  ✅ Git instalado" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Git no instalado - necesario para deploy en Render" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RESUMEN DE VERIFICACIÓN" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($allGood) {
    Write-Host "✅ TODO LISTO PARA LA PRESENTACIÓN" -ForegroundColor Green
    Write-Host ""
    Write-Host "Próximos pasos:" -ForegroundColor Cyan
    Write-Host "1. Revisar GUIA_PRESENTACION.md" -ForegroundColor White
    Write-Host "2. Iniciar servicios: docker-compose up (o python app.py en cada carpeta)" -ForegroundColor White
    Write-Host "3. Tener Postman/Thunder Client listo" -ForegroundColor White
    Write-Host "4. Revisar API_EXAMPLES.md para ejemplos de uso" -ForegroundColor White
    Write-Host ""
    Write-Host "🌱 ¡Buena suerte en tu presentación! 🌱" -ForegroundColor Green
} else {
    Write-Host "❌ HAY PROBLEMAS QUE RESOLVER" -ForegroundColor Red
    Write-Host ""
    Write-Host "Revisa los errores arriba y corrígelos antes de presentar." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Resumen de métricas
Write-Host ""
Write-Host "📊 MÉTRICAS DEL PROYECTO:" -ForegroundColor Cyan
Write-Host "  - Microservicios: 2" -ForegroundColor White
Write-Host "  - Endpoints: 14" -ForegroundColor White
Write-Host "  - Pruebas: 31 (13 + 18)" -ForegroundColor White
Write-Host "  - Archivos de documentación: 7" -ForegroundColor White
Write-Host "  - Dockerfiles: 2" -ForegroundColor White
Write-Host ""

exit $(if ($allGood) { 0 } else { 1 })

