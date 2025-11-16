# Daily Report Pipeline

[![CI](https://github.com/Ezcareaga/daily-report-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Ezcareaga/daily-report-pipeline/actions)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-66%20passing-success.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-84%25-yellow.svg)](tests/)

**[🇪🇸 Leer en Español](README.es.md)**

Professional automated report generation system with comprehensive testing and CI/CD pipeline.

## Features

- Automated daily/monthly report processing
- Oracle database integration with connection pooling
- Email notifications with attachments
- FTP/SFTP file transfers
- Excel generation with custom formatting
- Comprehensive test suite (84% coverage)
- Professional logging with rotation
- CI/CD with GitHub Actions

## Architecture

Modular design with separation of concerns:
```
src/
├── core/              # Core components
│   ├── config.py      # Configuration management
│   ├── database.py    # Database operations
│   ├── email.py       # Email notifications
│   ├── excel.py       # Excel generation
│   ├── ftp.py         # File transfers
│   └── logger.py      # Logging setup
├── reports/           # Report processors
│   └── processor.py   # Main orchestrator
└── utils/             # Utilities
    └── reprocessor.py # Batch reprocessing
```

## Quick Start

### Installation
```bash
git clone https://github.com/Ezcareaga/daily-report-pipeline.git
cd daily-report-pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

1. Copy example config:
```bash
cp config/config.example.ini config/config.ini
```

2. Update with your credentials:
```ini
[DATABASE]
host = your_oracle_host
port = 1521
user = your_user
password = your_password

[EMAIL]
habilitado = true
servidor_smtp = smtp.gmail.com
puerto_smtp = 587
```

### Basic Usage
```python
from datetime import datetime
from src.core.config import ConfigManager
from src.core.database import DatabaseManager
from src.core.email import EmailManager
from src.core.excel import ExcelGenerator
from src.reports.processor import ReportProcessor

# Initialize components
config = ConfigManager("config/config.ini")
excel = ExcelGenerator(config)
email = EmailManager(config)

with DatabaseManager(config) as db:
    processor = ReportProcessor(config, db, email, excel)
    
    # Generate report
    result = processor.process(
        date=datetime.now(),
        output_path=Path("output/report.xlsx"),
        headers=['ID', 'Name', 'Amount']
    )
    
    print(f"Processed {result.records_processed} records")
```

## Testing
```bash
# Run all tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_processor.py -v
```
## Development Scripts

### Using Make (Linux/Mac)
```bash
make install-dev  # Install all dependencies
make test         # Run tests
make demo         # Run demo
```

### Using Python scripts (Cross-platform)
```bash
python scripts/dev.py install-dev
python scripts/dev.py test
python scripts/dev.py demo
```

### Manual commands
```bash
pip install -r requirements.txt
pytest tests/ -v
python demo/demo_report.py
```

## Metrics

- **Test Coverage**: 84%
- **Unit Tests**: 66 passing
- **Modules**: 9 complete components
- **Lines of Code**: 450+

## Development

Built with professional software engineering practices:

- Test-Driven Development (TDD)
- Feature branch workflow
- Pull Request reviews
- Continuous Integration
- Type hints throughout
- Comprehensive documentation

## Project Structure
```
daily-report-pipeline/
├── .github/
│   └── workflows/     # CI/CD pipelines
├── src/               # Source code
├── tests/             # Test suite
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
├── config/            # Configuration files
├── logs/              # Log files (gitignored)
├── output/            # Generated reports (gitignored)
└── requirements.txt   # Dependencies
```

## Contributing

This is a personal portfolio project, but feedback is welcome! Feel free to open an issue.

## About This Project

This system was developed as a personal initiative to automate manual reporting processes at my current workplace. What previously took hours of manual work now runs automatically, reducing processing time by 90% and eliminating human errors.

The codebase has been refactored and generalized for portfolio purposes, removing any company-specific information while maintaining the professional architecture and best practices.

### Real-World Impact
- ⏱Processing time: 2 hours → 10 minutes
- Error rate: ~5% → 0%
- Frequency: Daily automated execution
- Users: Finance and operations teams

## License

MIT License - feel free to use this code for learning purposes.

## Author

**Alberto Careaga**
- GitHub: [@Ezcareaga](https://github.com/Ezcareaga)

---

If you find this project useful, consider giving it a star!