"""
Pytest configuration and fixtures
Handles environment variable loading for tests
"""

import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from dotenv import load_dotenv


def pytest_configure(config):
    """
    Pytest hook that runs before test collection
    Loads environment variables from .env file
    """
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print("\n⚠️  Warning: .env file not found. Using environment variables or defaults.")
        print("   Create a .env file with GEMINI_API_KEY and RAPIDAPI_KEY for testing.")


@pytest.fixture
def mock_streamlit_secrets():
    """
    Fixture that provides mocked Streamlit secrets
    Loads from environment variables
    """
    secrets = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY', 'test-gemini-key'),
        'RAPIDAPI_KEY': os.getenv('RAPIDAPI_KEY', 'test-rapidapi-key')
    }
    
    with patch('streamlit.secrets', secrets):
        yield secrets


@pytest.fixture
def mock_pdf_file():
    """Fixture that provides a mock PDF file"""
    mock_file = Mock()
    mock_file.name = "test_resume.pdf"
    return mock_file


@pytest.fixture
def sample_resume_text():
    """Fixture that provides sample resume text"""
    return """
    JOHN DOE
    john.doe@email.com | (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Experienced Software Engineer with 5 years of expertise.
    
    TECHNICAL SKILLS
    Languages: Python, JavaScript, Java
    Frameworks: React, Node.js, Django
    
    PROFESSIONAL EXPERIENCE
    Senior Software Engineer | Tech Corp | Jan 2021 - Present
    - Led development of microservices architecture
    - Improved API performance by 40%
    """


@pytest.fixture
def sample_resume_analysis():
    """Fixture that provides sample resume analysis response"""
    return {
        "Primary job role": "Software Engineer",
        "Key skills": ["Python", "JavaScript", "React"],
        "Years of experience": "5 years",
        "Key achievements": ["Led team", "Shipped product"],
        "Preferred job titles": ["Senior Developer", "Tech Lead"]
    }


@pytest.fixture
def sample_job_listing():
    """Fixture that provides sample job listing"""
    return {
        "job_id": "12345",
        "job_title": "Senior Python Developer",
        "employer_name": "Tech Corp",
        "job_city": "San Francisco",
        "job_country": "USA",
        "job_employment_type": "FULLTIME",
        "job_min_salary": 120000,
        "job_max_salary": 180000,
        "job_description": "We are looking for...",
        "job_apply_link": "https://example.com/apply",
        "job_posted_at_datetime_utc": "2024-01-20T10:00:00Z"
    }


@pytest.fixture
def sample_job_listings(sample_job_listing):
    """Fixture that provides multiple job listings"""
    listings = []
    for i in range(5):
        job = sample_job_listing.copy()
        job["job_id"] = str(1000 + i)
        job["job_title"] = f"Position {i+1}"
        listings.append(job)
    return listings
