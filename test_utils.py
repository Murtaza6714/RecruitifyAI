"""
Utility functions and fixtures for API testing
Provides helper functions, mock data, and test fixtures
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any


class MockDataGenerator:
    """Generate realistic mock data for testing"""
    
    @staticmethod
    def generate_resume_analysis() -> Dict[str, Any]:
        """Generate a sample resume analysis response"""
        return {
            "Primary job role": "Software Engineer",
            "Key skills": [
                "Python",
                "JavaScript",
                "React",
                "Node.js",
                "PostgreSQL",
                "AWS"
            ],
            "Years of experience": "5 years",
            "Key achievements": [
                "Led development of microservices architecture",
                "Improved API performance by 40%",
                "Mentored 3 junior developers",
                "Shipped 15+ features to production"
            ],
            "Preferred job titles": [
                "Senior Software Engineer",
                "Full Stack Developer",
                "Tech Lead",
                "Engineering Manager"
            ]
        }
    
    @staticmethod
    def generate_job_listing() -> Dict[str, Any]:
        """Generate a sample job listing"""
        return {
            "job_id": "12345",
            "job_title": "Senior Python Developer",
            "employer_name": "Tech Innovation Corp",
            "job_city": "San Francisco",
            "job_state": "CA",
            "job_country": "USA",
            "job_employment_type": "FULLTIME",
            "job_min_salary": 150000,
            "job_max_salary": 200000,
            "job_description": "We are looking for an experienced Python developer to join our team...",
            "job_highlights": {
                "Qualifications": [
                    "5+ years of Python experience",
                    "Experience with AWS",
                    "Strong problem-solving skills"
                ],
                "Benefits": [
                    "Competitive salary",
                    "Health insurance",
                    "Remote work options"
                ]
            },
            "job_apply_link": "https://example.com/apply/12345",
            "job_posted_at_datetime_utc": datetime.now().isoformat() + "Z"
        }
    
    @staticmethod
    def generate_job_listings(count: int = 5) -> List[Dict[str, Any]]:
        """Generate multiple job listings"""
        listings = []
        for i in range(count):
            job = MockDataGenerator.generate_job_listing()
            job["job_id"] = str(1000 + i)
            job["job_title"] = f"Position {i+1}"
            job["job_min_salary"] = 100000 + (i * 10000)
            job["job_max_salary"] = 150000 + (i * 10000)
            listings.append(job)
        return listings
    
    @staticmethod
    def generate_resume_text() -> str:
        """Generate sample resume text"""
        return """
        JOHN DOE
        john.doe@email.com | (555) 123-4567 | LinkedIn.com/in/johndoe
        
        PROFESSIONAL SUMMARY
        Experienced Software Engineer with 5 years of expertise in full-stack development.
        Proficient in Python, JavaScript, and cloud technologies. Strong track record of
        delivering scalable solutions and leading cross-functional teams.
        
        TECHNICAL SKILLS
        Languages: Python, JavaScript, Java, SQL
        Frameworks: React, Node.js, Django, Flask
        Databases: PostgreSQL, MongoDB, Redis
        Cloud: AWS, Google Cloud Platform
        Tools: Git, Docker, Kubernetes, Jenkins
        
        PROFESSIONAL EXPERIENCE
        
        Senior Software Engineer | Tech Corp | Jan 2021 - Present
        - Led development of microservices architecture serving 1M+ users
        - Improved API response time by 40% through optimization
        - Mentored team of 3 junior developers
        - Implemented CI/CD pipeline reducing deployment time by 60%
        
        Software Engineer | StartUp Inc | Jun 2019 - Dec 2020
        - Developed full-stack web application using React and Node.js
        - Designed and implemented PostgreSQL database schema
        - Collaborated with product team to deliver 15+ features
        
        Junior Developer | Web Solutions | Jan 2019 - May 2019
        - Built responsive web interfaces using React
        - Wrote unit tests achieving 85% code coverage
        - Participated in code reviews and team meetings
        
        EDUCATION
        Bachelor of Science in Computer Science
        State University | Graduated: May 2018
        
        CERTIFICATIONS
        - AWS Certified Solutions Architect
        - Google Cloud Professional Data Engineer
        """
    
    @staticmethod
    def generate_error_response(error_type: str = "generic") -> Dict[str, Any]:
        """Generate error responses for testing"""
        errors = {
            "generic": {"error": "An error occurred", "code": 500},
            "auth": {"error": "Unauthorized", "code": 401},
            "not_found": {"error": "Resource not found", "code": 404},
            "rate_limit": {"error": "Rate limit exceeded", "code": 429},
            "timeout": {"error": "Request timeout", "code": 504}
        }
        return errors.get(error_type, errors["generic"])


class TestDataValidator:
    """Validate test data and API responses"""
    
    @staticmethod
    def validate_resume_analysis(data: Dict[str, Any]) -> bool:
        """Validate resume analysis response structure"""
        required_fields = [
            "Primary job role",
            "Key skills",
            "Years of experience",
            "Key achievements",
            "Preferred job titles"
        ]
        
        if not isinstance(data, dict):
            return False
        
        for field in required_fields:
            if field not in data:
                return False
        
        if not isinstance(data["Key skills"], list):
            return False
        
        if not isinstance(data["Key achievements"], list):
            return False
        
        if not isinstance(data["Preferred job titles"], list):
            return False
        
        return True
    
    @staticmethod
    def validate_job_listing(data: Dict[str, Any]) -> bool:
        """Validate job listing response structure"""
        required_fields = [
            "job_id",
            "job_title",
            "employer_name",
            "job_country"
        ]
        
        if not isinstance(data, dict):
            return False
        
        for field in required_fields:
            if field not in data:
                return False
        
        return True
    
    @staticmethod
    def validate_job_listings(data: Dict[str, Any]) -> bool:
        """Validate job listings response structure"""
        if not isinstance(data, dict):
            return False
        
        if "data" not in data:
            return False
        
        if not isinstance(data["data"], list):
            return False
        
        for job in data["data"]:
            if not TestDataValidator.validate_job_listing(job):
                return False
        
        return True


class APITestHelper:
    """Helper functions for API testing"""
    
    @staticmethod
    def create_mock_response(status_code: int = 200, json_data: Dict = None):
        """Create a mock response object"""
        from unittest.mock import Mock
        
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data or {}
        
        if status_code >= 400:
            mock_response.raise_for_status.side_effect = Exception(f"HTTP {status_code}")
        else:
            mock_response.raise_for_status.return_value = None
        
        return mock_response
    
    @staticmethod
    def assert_valid_api_key(api_key: str) -> bool:
        """Validate API key format"""
        if not api_key:
            return False
        if len(api_key) < 10:
            return False
        return True
    
    @staticmethod
    def measure_response_time(func, *args, **kwargs) -> tuple:
        """Measure function execution time"""
        import time
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        return result, elapsed
    
    @staticmethod
    def simulate_network_delay(seconds: float = 0.1):
        """Simulate network delay for testing"""
        import time
        time.sleep(seconds)


class TestScenarios:
    """Pre-built test scenarios for common use cases"""
    
    @staticmethod
    def scenario_successful_resume_analysis():
        """Scenario: User uploads resume and gets analysis"""
        return {
            "resume_text": MockDataGenerator.generate_resume_text(),
            "expected_analysis": MockDataGenerator.generate_resume_analysis(),
            "description": "User uploads valid resume and receives analysis"
        }
    
    @staticmethod
    def scenario_job_search_with_results():
        """Scenario: User searches for jobs and gets results"""
        return {
            "job_title": "Senior Python Developer",
            "location": "San Francisco",
            "expected_jobs": MockDataGenerator.generate_job_listings(5),
            "description": "User searches for jobs and receives multiple results"
        }
    
    @staticmethod
    def scenario_job_search_no_results():
        """Scenario: User searches for jobs with no results"""
        return {
            "job_title": "Extremely Niche Job Title XYZ",
            "location": "Nowhere",
            "expected_jobs": [],
            "description": "User searches for non-existent job and receives empty results"
        }
    
    @staticmethod
    def scenario_api_error_handling():
        """Scenario: API returns error"""
        return {
            "error_type": "auth",
            "expected_behavior": "Graceful error handling",
            "description": "API authentication fails and app handles error gracefully"
        }
    
    @staticmethod
    def scenario_malformed_response():
        """Scenario: API returns malformed data"""
        return {
            "response": "Not valid JSON",
            "expected_behavior": "Error handling and fallback",
            "description": "API returns invalid JSON and app handles gracefully"
        }


class PerformanceBenchmark:
    """Performance benchmarking utilities"""
    
    TARGETS = {
        "pdf_extraction": 2.0,      # seconds
        "resume_analysis": 5.0,     # seconds
        "job_search": 3.0,          # seconds
        "complete_workflow": 10.0   # seconds
    }
    
    @staticmethod
    def check_performance(operation: str, elapsed_time: float) -> bool:
        """Check if operation meets performance target"""
        target = PerformanceBenchmark.TARGETS.get(operation)
        if target is None:
            return True
        return elapsed_time <= target
    
    @staticmethod
    def get_performance_report(operation: str, elapsed_time: float) -> str:
        """Generate performance report"""
        target = PerformanceBenchmark.TARGETS.get(operation, "N/A")
        status = "✅ PASS" if PerformanceBenchmark.check_performance(operation, elapsed_time) else "❌ FAIL"
        return f"{status} | {operation}: {elapsed_time:.2f}s (target: {target}s)"


# Example usage functions for documentation
def example_mock_data():
    """Example: Generate mock data"""
    resume_analysis = MockDataGenerator.generate_resume_analysis()
    print("Resume Analysis:", json.dumps(resume_analysis, indent=2))
    
    job_listing = MockDataGenerator.generate_job_listing()
    print("Job Listing:", json.dumps(job_listing, indent=2))


def example_validation():
    """Example: Validate data"""
    data = MockDataGenerator.generate_resume_analysis()
    is_valid = TestDataValidator.validate_resume_analysis(data)
    print(f"Resume analysis valid: {is_valid}")


def example_test_scenarios():
    """Example: Use test scenarios"""
    scenario = TestScenarios.scenario_successful_resume_analysis()
    print("Scenario:", scenario["description"])
    print("Resume text length:", len(scenario["resume_text"]))


if __name__ == "__main__":
    print("Test Utilities Module")
    print("=" * 60)
    print("\nAvailable Classes:")
    print("- MockDataGenerator: Generate realistic mock data")
    print("- TestDataValidator: Validate API responses")
    print("- APITestHelper: Helper functions for testing")
    print("- TestScenarios: Pre-built test scenarios")
    print("- PerformanceBenchmark: Performance testing utilities")
