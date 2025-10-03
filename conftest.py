"""
Pytest configuration file for ApplyBot tests.
Handles environment variable loading and mock configurations.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment with mock configurations."""
    # Set test environment variables if not already set
    test_env_vars = {
        "DATABASE_URL": "sqlite:///test.db",
        "REDIS_URL": "redis://localhost:6379/1",
        "OPENAI_API_KEY": "test-openai-key",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_KEY": "test-supabase-key",
        "REED_API_KEY": "test-reed-key",
        "ADZUNA_APP_ID": "test-adzuna-id",
        "ADZUNA_APP_KEY": "test-adzuna-key",
        "ENVIRONMENT": "test"
    }
    
    for key, value in test_env_vars.items():
        if not os.getenv(key):
            os.environ[key] = value

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch('openai.OpenAI') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        # Mock chat completions
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Mock AI response"))]
        )
        
        yield mock_instance

@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing."""
    with patch('supabase.create_client') as mock_create:
        mock_client = MagicMock()
        mock_create.return_value = mock_client
        
        # Mock table operations
        mock_client.table.return_value.select.return_value.execute.return_value = MagicMock(
            data=[]
        )
        mock_client.table.return_value.insert.return_value.execute.return_value = MagicMock(
            data=[{"id": "test-id"}]
        )
        
        yield mock_client

@pytest.fixture
def mock_redis_client():
    """Mock Redis client for testing."""
    with patch('redis.Redis') as mock_redis:
        mock_instance = MagicMock()
        mock_redis.return_value = mock_instance
        
        # Mock Redis operations
        mock_instance.get.return_value = None
        mock_instance.set.return_value = True
        mock_instance.ping.return_value = True
        
        yield mock_instance

@pytest.fixture
def mock_external_apis():
    """Mock external job APIs (Reed, Adzuna, etc.)."""
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "test-job-1",
                    "title": "Test Developer",
                    "company": "Test Company",
                    "location": "Test Location",
                    "description": "Test job description"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        yield mock_get

@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        "id": "test-job-uuid",
        "title": "Senior Python Developer",
        "company": "TechCorp",
        "description": "We are looking for a senior Python developer...",
        "location": "San Francisco, CA",
        "salary_range": "$120k - $150k",
        "requirements": ["Python", "FastAPI", "PostgreSQL"],
        "source": "RemoteOK",
        "posted_date": "2024-01-15T10:30:00Z"
    }

@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "user_id": "test-user-uuid",
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1(555) 123-4567",
        "location": "San Francisco, CA",
        "experience_years": "5+",
        "primary_skills": ["Python", "React", "AWS"]
    }

@pytest.fixture
def sample_project_data():
    """Sample project data for testing."""
    return {
        "project_id": "test-project-uuid",
        "title": "E-commerce Platform",
        "description": "Built a full-stack e-commerce platform using Python, FastAPI, and React",
        "technologies": ["Python", "FastAPI", "React", "PostgreSQL"],
        "user_id": "test-user-uuid"
    }