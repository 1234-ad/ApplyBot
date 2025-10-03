# 🧪 Testing Guide

This document explains how to run tests for the ApplyBot application.

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run all tests:**
   ```bash
   python run_tests.py
   ```

## 📁 Test Structure

- `conftest.py` - Pytest configuration with fixtures and mocks
- `test_integration_simple.py` - Integration tests for API endpoints
- `run_tests.py` - Test runner script with different options
- `TESTING.md` - This documentation file

## 🔧 Environment Setup

### Environment Variables

Tests automatically load environment variables from `.env` file. Required variables:

```bash
# Database
DATABASE_URL=sqlite:///test.db

# AI Services
OPENAI_API_KEY=your-openai-key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# Optional - will use test defaults if not provided
REDIS_URL=redis://localhost:6379/1
REED_API_KEY=your-reed-key
ADZUNA_APP_ID=your-adzuna-id
ADZUNA_APP_KEY=your-adzuna-key
```

### Test Environment Variables

If environment variables are not set, `conftest.py` automatically provides test defaults:

- `DATABASE_URL`: `sqlite:///test.db`
- `REDIS_URL`: `redis://localhost:6379/1`
- `OPENAI_API_KEY`: `test-openai-key`
- `SUPABASE_URL`: `https://test.supabase.co`
- `SUPABASE_KEY`: `test-supabase-key`
- `ENVIRONMENT`: `test`

## 🎯 Running Tests

### Using the Test Runner

```bash
# Run all tests
python run_tests.py

# Run only integration tests
python run_tests.py integration

# Run with coverage report
python run_tests.py coverage

# Test environment variable loading
python run_tests.py env

# Show help
python run_tests.py --help
```

### Using Pytest Directly

```bash
# Run all tests with verbose output
pytest -v

# Run specific test file
pytest test_integration_simple.py -v

# Run specific test class
pytest test_integration_simple.py::TestHealthEndpoint -v

# Run specific test method
pytest test_integration_simple.py::TestHealthEndpoint::test_health_check -v

# Run with coverage
pytest --cov=app --cov-report=html
```

## 🔍 Test Categories

### Integration Tests (`test_integration_simple.py`)

Tests API endpoints with mocked external dependencies:

- **Health Check**: Basic server health endpoint
- **Job Endpoints**: Job fetching, filtering, and sources
- **Project Matching**: Project-to-job matching algorithms
- **Resume Generation**: PDF resume creation with AI
- **Cover Letter Generation**: AI-powered cover letter creation
- **Cache Endpoints**: Redis cache statistics
- **Environment Variables**: Proper loading and defaults

### Mocked Dependencies

Tests use mocks for external services to avoid:
- Real API calls to OpenAI, Reed, Adzuna
- Database connections (uses test database)
- Redis connections (mocked)
- File system operations

## 🛠️ Fixtures Available

From `conftest.py`:

- `mock_openai_client` - Mocked OpenAI API client
- `mock_supabase_client` - Mocked Supabase client
- `mock_redis_client` - Mocked Redis client
- `mock_external_apis` - Mocked job API responses
- `sample_job_data` - Sample job data for testing
- `sample_user_data` - Sample user data for testing
- `sample_project_data` - Sample project data for testing

## 📊 Coverage Reports

Generate HTML coverage reports:

```bash
python run_tests.py coverage
```

View the report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure you're in the project root
   cd /path/to/ApplyBot
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Environment Variable Issues**
   ```bash
   # Test environment loading specifically
   python run_tests.py env
   ```

3. **API Server Not Running**
   - Integration tests will skip if the API server isn't running
   - Start the server: `python start_server.py`
   - Or run tests without server dependency

4. **Database Issues**
   ```bash
   # Tests use SQLite by default
   # Make sure DATABASE_URL is set correctly
   export DATABASE_URL="sqlite:///test.db"
   ```

### Debug Mode

Run tests with more verbose output:

```bash
pytest -v -s --tb=long
```

## 🔄 Continuous Integration

For CI/CD pipelines, use:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with JUnit XML output
pytest --junitxml=test-results.xml

# Run with coverage for CI
pytest --cov=app --cov-report=xml --cov-report=term
```

## 📝 Writing New Tests

### Test File Naming
- Integration tests: `test_integration_*.py`
- Unit tests: `test_unit_*.py`
- Specific feature tests: `test_feature_*.py`

### Example Test Structure

```python
import pytest
from unittest.mock import patch

class TestNewFeature:
    \"\"\"Test new feature functionality.\"\"\"
    
    def test_basic_functionality(self, sample_data):
        \"\"\"Test basic feature works.\"\"\"
        # Arrange
        input_data = sample_data
        
        # Act
        result = your_function(input_data)
        
        # Assert
        assert result is not None
        assert result["status"] == "success"
    
    @patch('external.service.call')
    def test_with_mocked_service(self, mock_service):
        \"\"\"Test with mocked external service.\"\"\"
        # Setup mock
        mock_service.return_value = {"data": "test"}
        
        # Test your code
        result = function_that_calls_service()
        
        # Verify
        assert mock_service.called
        assert result["data"] == "test"
```

## 🎯 Best Practices

1. **Use Fixtures**: Leverage existing fixtures for common test data
2. **Mock External Services**: Always mock external API calls
3. **Test Edge Cases**: Include error conditions and edge cases
4. **Clear Test Names**: Use descriptive test method names
5. **Arrange-Act-Assert**: Structure tests clearly
6. **Independent Tests**: Each test should be independent
7. **Clean Up**: Use fixtures for setup/teardown when needed

---

For more information, see the main [README.md](README.md) and [API_DOCUMENTATION.md](API_DOCUMENTATION.md).