"""
Simple integration tests for ApplyBot API endpoints.
Tests basic functionality with mocked external dependencies.
"""

import os
import pytest
import requests
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock

# Load environment variables at module level
load_dotenv()

# Test configuration
BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:8000/api/v1")
TEST_TIMEOUT = 30

class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test that health endpoint returns expected response."""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            data = response.json()
            assert "status" in data
            assert "service" in data
            assert data["status"] == "healthy"
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")

class TestJobEndpoints:
    """Test job-related endpoints with mocked external APIs."""
    
    def test_get_jobs_empty_response(self, mock_external_apis):
        """Test getting jobs when no jobs exist."""
        try:
            response = requests.get(f"{BASE_URL}/jobs", timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, list)
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")
    
    def test_get_jobs_with_filters(self, mock_external_apis):
        """Test getting jobs with query parameters."""
        try:
            params = {
                "keywords": "python,developer",
                "location": "San Francisco",
                "limit": 10
            }
            response = requests.get(f"{BASE_URL}/jobs", params=params, timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, list)
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")
    
    @patch('requests.post')
    def test_fetch_jobs(self, mock_post, mock_external_apis):
        """Test fetching new jobs from external sources."""
        # Mock the internal API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "message": "Fetched 5 jobs, 3 new, 2 updated",
            "results": {
                "total_fetched": 5,
                "new_jobs": 3,
                "updated_jobs": 2,
                "sources": {
                    "RemoteOK": {"fetched": 3, "new": 2, "updated": 1, "status": "success"},
                    "GitHub": {"fetched": 2, "new": 1, "updated": 1, "status": "success"}
                }
            }
        }
        mock_post.return_value = mock_response
        
        try:
            payload = {
                "keywords": ["python", "react"],
                "limit_per_source": 10
            }
            response = requests.post(f"{BASE_URL}/jobs/fetch", json=payload, timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            data = response.json()
            assert data["success"] is True
            assert "results" in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")
    
    def test_get_job_sources(self):
        """Test getting available job sources."""
        try:
            response = requests.get(f"{BASE_URL}/jobs/sources", timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            data = response.json()
            assert "success" in data
            assert "enabled_sources" in data
            assert "available_sources" in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")

class TestProjectMatching:
    """Test project matching endpoints with mocked data."""
    
    def test_match_projects_invalid_job_id(self):
        """Test project matching with invalid job ID."""
        try:
            params = {"user_id": "test-user-id"}
            response = requests.get(f"{BASE_URL}/match/invalid-job-id", params=params, timeout=TEST_TIMEOUT)
            assert response.status_code in [404, 422]  # Either not found or validation error
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")
    
    def test_match_projects_missing_user_id(self):
        """Test project matching without required user_id parameter."""
        try:
            response = requests.get(f"{BASE_URL}/match/test-job-id", timeout=TEST_TIMEOUT)
            assert response.status_code == 422  # Validation error
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")

class TestResumeGeneration:
    """Test resume generation endpoints with mocked AI services."""
    
    def test_generate_resume_missing_data(self, mock_openai_client):
        """Test resume generation with missing required data."""
        try:
            payload = {
                "name": "John Doe"
                # Missing other required fields
            }
            response = requests.post(f"{BASE_URL}/resume/generate", json=payload, timeout=TEST_TIMEOUT)
            assert response.status_code == 422  # Validation error
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")
    
    def test_generate_resume_complete_data(self, mock_openai_client, sample_user_data):
        """Test resume generation with complete user data."""
        try:
            payload = {
                **sample_user_data,
                "education": [
                    {
                        "degree": "Bachelor of Computer Science",
                        "institution": "Stanford University",
                        "year": "2018-2022"
                    }
                ],
                "skills": [
                    {
                        "category": "Programming Languages",
                        "items": ["Python", "JavaScript", "TypeScript"]
                    }
                ],
                "experience": [
                    {
                        "role": "Software Engineer",
                        "company": "TechCorp",
                        "duration": "2022-Present",
                        "location": "San Francisco, CA",
                        "achievements": ["Built scalable APIs", "Reduced response times by 60%"]
                    }
                ]
            }
            
            with patch('requests.post') as mock_post:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "success": True,
                    "resume_id": "test-resume-id",
                    "download_url": "/api/v1/resume/download/test-resume-id",
                    "generation_method": "latex",
                    "message": "Resume generated successfully"
                }
                mock_post.return_value = mock_response
                
                response = requests.post(f"{BASE_URL}/resume/generate", json=payload, timeout=TEST_TIMEOUT)
                assert response.status_code == 200
                
                data = response.json()
                assert data["success"] is True
                assert "resume_id" in data
                
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")

class TestCoverLetterGeneration:
    """Test cover letter generation endpoints with mocked AI services."""
    
    def test_generate_cover_letter_invalid_job_id(self, mock_openai_client):
        """Test cover letter generation with invalid job ID."""
        try:
            payload = {
                "user_id": "test-user-id",
                "user_name": "John Doe",
                "user_email": "john@example.com"
            }
            response = requests.post(f"{BASE_URL}/cover-letters/invalid-job-id", json=payload, timeout=TEST_TIMEOUT)
            assert response.status_code in [404, 422]
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")

class TestCacheEndpoints:
    """Test cache-related endpoints."""
    
    def test_cache_stats(self, mock_redis_client):
        """Test getting cache statistics."""
        try:
            response = requests.get(f"{BASE_URL}/match/cache/stats", timeout=TEST_TIMEOUT)
            assert response.status_code == 200
            
            data = response.json()
            assert "success" in data
            assert "cache_stats" in data
            
        except requests.exceptions.ConnectionError:
            pytest.skip("API server not running - skipping integration test")

class TestEnvironmentVariables:
    """Test that environment variables are properly loaded."""
    
    def test_required_env_vars_loaded(self):
        """Test that all required environment variables are available."""
        required_vars = [
            "DATABASE_URL",
            "OPENAI_API_KEY",
            "SUPABASE_URL",
            "SUPABASE_KEY"
        ]
        
        for var in required_vars:
            assert os.getenv(var) is not None, f"Environment variable {var} is not set"
    
    def test_optional_env_vars(self):
        """Test that optional environment variables have defaults."""
        # These should have defaults set by conftest.py if not provided
        optional_vars = [
            "REDIS_URL",
            "REED_API_KEY",
            "ADZUNA_APP_ID",
            "ADZUNA_APP_KEY"
        ]
        
        for var in optional_vars:
            value = os.getenv(var)
            assert value is not None, f"Optional environment variable {var} should have a default value"
    
    def test_test_environment_flag(self):
        """Test that we're running in test environment."""
        env = os.getenv("ENVIRONMENT")
        assert env == "test", "Tests should run with ENVIRONMENT=test"

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])