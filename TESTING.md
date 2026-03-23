# RIFFAI Testing Guide

## Setup Test Environment

```bash
cd backend

# Install test dependencies
pip install -r requirements.txt

# Create test database
docker exec -it docker-db-1 psql -U riffai -c "CREATE DATABASE riffai_test;"
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html to view coverage report
```

### Run specific test file
```bash
pytest tests/test_api/test_dashboard.py
```

### Run specific test
```bash
pytest tests/test_api/test_dashboard.py::test_dashboard_overview
```

### Run with verbose output
```bash
pytest -v -s
```

## Test Structure

```
tests/
├── conftest.py              # Pytest fixtures
├── test_api/
│   ├── test_dashboard.py    # Dashboard API tests
│   ├── test_prediction.py   # Prediction API tests
│   ├── test_alerts.py       # Alerts API tests
│   └── test_auth.py         # Authentication tests
├── test_services/
│   ├── test_ai_service.py   # AI service tests
│   ├── test_water_service.py
│   └── test_satellite_service.py
└── test_models/
    └── test_database.py     # Database model tests
```

## Database Migrations

### Initialize Alembic (already done)
```bash
alembic init alembic
```

### Create new migration
```bash
alembic revision --autogenerate -m "Add new column"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

### View migration history
```bash
alembic history
```

## CI/CD Integration

Tests run automatically on:
- Every push to `main` branch
- Every pull request
- Before deployment

## Test Coverage Goals

- Overall coverage: > 80%
- Critical paths: > 95%
- API endpoints: 100%
- Services: > 90%

## Writing New Tests

### API Test Example
```python
@pytest.mark.asyncio
async def test_my_endpoint(client: AsyncClient):
    response = await client.get("/api/my-endpoint")
    assert response.status_code == 200
    assert "data" in response.json()
```

### Service Test Example
```python
def test_my_service():
    service = MyService()
    result = service.process_data(input_data)
    assert result is not None
    assert result["status"] == "success"
```

## Troubleshooting

### Database connection errors
```bash
# Check if test database exists
docker exec -it docker-db-1 psql -U riffai -l

# Recreate test database
docker exec -it docker-db-1 psql -U riffai -c "DROP DATABASE IF EXISTS riffai_test;"
docker exec -it docker-db-1 psql -U riffai -c "CREATE DATABASE riffai_test;"
```

### Import errors
```bash
# Make sure you're in the backend directory
cd backend
export PYTHONPATH=$PYTHONPATH:$(pwd)
```
