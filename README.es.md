# Pipeline Automatizado de Reportes

[![CI](https://github.com/Ezcareaga/daily-report-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Ezcareaga/daily-report-pipeline/actions)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-66%20passing-success.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-84%25-yellow.svg)](tests/)

**[🇺🇸 Read in English](README.md)**

Sistema profesional de generación automatizada de reportes con suite completa de pruebas y pipeline de CI/CD.

## Características

- Procesamiento automatizado de reportes diarios/mensuales
- Integración con base de datos Oracle con pool de conexiones
- Notificaciones por email con archivos adjuntos
- Transferencias de archivos FTP/SFTP
- Generación de archivos Excel con formato personalizado
- Suite completa de pruebas (84% cobertura)
- Sistema de logging profesional con rotación
- CI/CD con GitHub Actions

## Sobre Este Proyecto

Este sistema fue desarrollado como iniciativa personal para automatizar procesos manuales de reportería en mi lugar de trabajo actual. Lo que antes tomaba horas de trabajo manual ahora se ejecuta automáticamente, reduciendo el tiempo de procesamiento en un 90% y eliminando errores humanos.

El código ha sido refactorizado y generalizado para propósitos de portfolio, removiendo información específica de la empresa mientras se mantiene la arquitectura profesional y las mejores prácticas.

### Impacto en el Mundo Real
- Tiempo de procesamiento: 2 horas → 10 minutos
- Tasa de error: ~5% → 0%
- Frecuencia: Ejecución diaria automatizada
- Usuarios: Equipos de finanzas y operaciones

## Arquitectura

Diseño modular con separación de responsabilidades:
```
src/
├── core/              # Componentes principales
│   ├── config.py      # Gestión de configuración
│   ├── database.py    # Operaciones de base de datos
│   ├── email.py       # Notificaciones por email
│   ├── excel.py       # Generación de Excel
│   ├── ftp.py         # Transferencia de archivos
│   └── logger.py      # Configuración de logging
├── reports/           # Procesadores de reportes
│   └── processor.py   # Orquestador principal
└── utils/             # Utilidades
    └── reprocessor.py # Reprocesamiento por lotes
```

## Inicio Rápido

### Instalación
```bash
git clone https://github.com/Ezcareaga/daily-report-pipeline.git
cd daily-report-pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuración

1. Copiar archivo de configuración ejemplo:
```bash
cp config/config.example.ini config/config.ini
```

2. Actualizar con tus credenciales:
```ini
[DATABASE]
host = tu_host_oracle
port = 1521
user = tu_usuario
password = tu_contraseña

[EMAIL]
habilitado = true
servidor_smtp = smtp.gmail.com
puerto_smtp = 587
```

### Uso Básico
```python
from datetime import datetime
from pathlib import Path
from src.core.config import ConfigManager
from src.core.database import DatabaseManager
from src.core.email import EmailManager
from src.core.excel import ExcelGenerator
from src.reports.processor import ReportProcessor

# Inicializar componentes
config = ConfigManager("config/config.ini")
excel = ExcelGenerator(config)
email = EmailManager(config)

with DatabaseManager(config) as db:
    processor = ReportProcessor(config, db, email, excel)
    
    # Generar reporte
    result = processor.process(
        date=datetime.now(),
        output_path=Path("output/reporte.xlsx"),
        headers=['ID', 'Nombre', 'Monto']
    )
    
    print(f"Procesados {result.records_processed} registros")
```

## Demostración

Para una evaluación rápida sin requerir Oracle ni servicios externos:
```bash
python demo/demo_report.py
```

Esto creará una base de datos SQLite en memoria, insertará datos de ejemplo y generará un archivo Excel profesional en `demo/output/`.

Ver [demo/README.md](demo/README.md) para más detalles.

## Pruebas
```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Con reporte de cobertura
pytest tests/ --cov=src --cov-report=html

# Ejecutar archivo de prueba específico
pytest tests/unit/test_processor.py -v
```

## Comandos de Desarrollo

### Usando Make (Linux/Mac)
```bash
make install-dev  # Instalar todas las dependencias
make test         # Ejecutar pruebas
make test-cov     # Ejecutar pruebas con cobertura
make demo         # Ejecutar demostración
make clean        # Limpiar archivos de caché
```

### Usando Scripts Python (Windows/Multiplataforma)
```bash
python scripts/dev.py install-dev
python scripts/dev.py test
python scripts/dev.py test-cov
python scripts/dev.py demo
```

### Comandos Manuales
Ver secciones individuales arriba para comandos manuales de pip/pytest.

## Métricas

- **Cobertura de Pruebas**: 84%
- **Pruebas Unitarias**: 66 pasando
- **Total de Statements**: 451
- **Módulos**: 9 componentes completos
- **Líneas de Código**: 450+

## Desarrollo

Construido con prácticas profesionales de ingeniería de software:

- Desarrollo Dirigido por Pruebas (TDD)
- Flujo de trabajo con ramas de features
- Revisiones mediante Pull Requests
- Integración Continua
- Type hints en todo el código
- Documentación comprehensiva

## Estructura del Proyecto
```
daily-report-pipeline/
├── .github/
│   └── workflows/     # Pipelines de CI/CD
├── src/               # Código fuente
├── tests/             # Suite de pruebas
│   ├── unit/          # Pruebas unitarias
│   └── integration/   # Pruebas de integración
├── config/            # Archivos de configuración
├── demo/              # Script de demostración
├── scripts/           # Scripts de desarrollo
├── logs/              # Archivos de log (gitignored)
├── output/            # Reportes generados (gitignored)
└── requirements.txt   # Dependencias
```

## Contribuciones

Este es un proyecto de portfolio personal, pero los comentarios son bienvenidos. No dudes en abrir un issue.

## Licencia

MIT License - siéntete libre de usar este código para propósitos de aprendizaje.

## Autor

**Alberto (Ezequiel) Careaga**
- GitHub: [@Ezcareaga](https://github.com/Ezcareaga)
- LinkedIn: [linkedin.com/in/ezcareaga](https://linkedin.com/in/ezcareaga)

---

Si encuentras útil este proyecto, ¡considera darle una estrella!