# Daily Report Pipeline

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-12%20passing-green.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-54%25-yellow.svg)](tests/)

Automated daily report generation system with Oracle database integration.

## Features

- Automated daily processing
- Oracle database integration  
- Email notifications
- FTP/SFTP transfers
- Comprehensive testing
- Detailed logging

## Installation
```bash
git clone https://github.com/Ezcareaga/daily-report-pipeline.git
cd daily-report-pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

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
```

## Usage
```python
from src.core.config import ConfigManager
from src.core.database import DatabaseManager

config = ConfigManager("config/config.ini")
with DatabaseManager(config) as db:
    results = db.execute_query("SELECT * FROM reports")
```

## Testing
```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=src
```

## Project Structure
```
├── src/
│   ├── core/          # Core modules
│   ├── reports/       # Report processors
│   └── utils/         # Utilities
├── tests/             # Test suite
├── config/            # Configuration
└── docs/              # Documentation
```

## License

MIT
