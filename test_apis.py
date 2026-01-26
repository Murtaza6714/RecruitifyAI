import pytest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO
import PyPDF2
import requests
from dotenv import load_dotenv

import sys
sys.path.insert(0, 'd:\\jobhuntai')

load_dotenv()


class TestPDFExtraction:
    """Test cases for PDF text extraction"""
    
    @patch('PyPDF2.PdfReader')
    def test_extract_text_from_pdf_single_page(self, mock_pdf_reader):
        """Test extracting text from single page PDF"""
        from main import extract_text_from_pdf
        
        mock_page = Mock()
        mock_page.extract_text.return_value = "Sample resume text"
        mock_pdf_reader.return_value.pages = [mock_page]
        
        mock_file = Mock()
        result = extract_text_from_pdf(mock_file)
        
        assert result == "Sample resume text"
        mock_page.extract_text.assert_called_once()
    
    @patch('PyPDF2.PdfReader')
    def test_extract_text_from_pdf_multiple_pages(self, mock_pdf_reader):
        """Test extracting text from multi-page PDF"""
        from main import extract_text_from_pdf
        
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1 content "
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2 content"
        
        mock_pdf_reader.return_value.pages = [mock_page1, mock_page2]
        
        mock_file = Mock()
        result = extract_text_from_pdf(mock_file)
        
        assert result == "Page 1 content Page 2 content"
        assert mock_page1.extract_text.called
        assert mock_page2.extract_text.called
    
    @patch('PyPDF2.PdfReader')
    def test_extract_text_from_empty_pdf(self, mock_pdf_reader):
        """Test extracting text from empty PDF"""
        from main import extract_text_from_pdf
        
        mock_pdf_reader.return_value.pages = []
        
        mock_file = Mock()
        result = extract_text_from_pdf(mock_file)
        
        assert result == ""
    
    @patch('PyPDF2.PdfReader')
    def test_extract_text_pdf_with_special_characters(self, mock_pdf_reader):
        """Test extracting text with special characters"""
        from main import extract_text_from_pdf
        
        mock_page = Mock()
        mock_page.extract_text.return_value = "Python, C++, C# & Java\nSalary: $100,000-$150,000"
        mock_pdf_reader.return_value.pages = [mock_page]
        
        mock_file = Mock()
        result = extract_text_from_pdf(mock_file)
        
        assert "Python" in result
        assert "$" in result
        assert "&" in result


class TestGeminiAPI:
    """Test cases for Gemini API resume analysis"""
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_analyze_resume_valid_response(self, mock_configure, mock_model_class, mock_streamlit_secrets):
        """Test resume analysis with valid JSON response"""
        from main import analyze_resume
        
        mock_response = Mock()
        mock_response.text = json.dumps({
            "Primary job role": "Software Engineer",
            "Key skills": ["Python", "JavaScript", "React"],
            "Years of experience": "5 years",
            "Key achievements": ["Led team of 5", "Shipped product"],
            "Preferred job titles": ["Senior Developer", "Tech Lead"]
        })
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = analyze_resume("Sample resume text")
        
        assert result["Primary job role"] == "Software Engineer"
        assert "Python" in result["Key skills"]
        assert len(result["Key achievements"]) == 2
        mock_configure.assert_called_once_with(api_key=mock_streamlit_secrets['GEMINI_API_KEY'])
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_analyze_resume_json_with_code_blocks(self, mock_configure, mock_model_class, mock_streamlit_secrets):
        """Test resume analysis with JSON wrapped in code blocks"""
        from main import analyze_resume
        
        json_data = {
            "Primary job role": "Data Scientist",
            "Key skills": ["Python", "SQL", "TensorFlow"],
            "Years of experience": "3 years",
            "Key achievements": ["Built ML model"],
            "Preferred job titles": ["ML Engineer"]
        }
        
        mock_response = Mock()
        mock_response.text = f"```json\n{json.dumps(json_data)}\n```"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = analyze_resume("Sample resume")
        
        assert result["Primary job role"] == "Data Scientist"
        assert "TensorFlow" in result["Key skills"]
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_analyze_resume_invalid_json_response(self, mock_configure, mock_model_class, mock_streamlit_secrets):
        """Test resume analysis with invalid JSON response"""
        from main import analyze_resume
        
        mock_response = Mock()
        mock_response.text = "This is not valid JSON"
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = analyze_resume("Sample resume")
        
        assert result == {}
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_analyze_resume_api_error(self, mock_configure, mock_model_class, mock_streamlit_secrets):
        """Test resume analysis when API throws exception"""
        from main import analyze_resume
        
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model
        
        result = analyze_resume("Sample resume")
        
        assert result == {}
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_analyze_resume_empty_text(self, mock_configure, mock_model_class, mock_streamlit_secrets):
        """Test resume analysis with empty resume text"""
        from main import analyze_resume
        
        mock_response = Mock()
        mock_response.text = json.dumps({
            "Primary job role": "",
            "Key skills": [],
            "Years of experience": "",
            "Key achievements": [],
            "Preferred job titles": []
        })
        
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        result = analyze_resume("")
        
        assert isinstance(result, dict)
        assert result["Key skills"] == []


class TestRapidAPIJSearch:
    """Test cases for RapidAPI JSearch job search"""
    
    @patch('requests.get')
    def test_fetch_jobs_valid_response(self, mock_get, mock_streamlit_secrets):
        """Test fetching jobs with valid API response"""
        from main import fetch_jobs_rapidapi
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "job_id": "1",
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
            ]
        }
        mock_get.return_value = mock_response
        
        result = fetch_jobs_rapidapi("Python Developer", "San Francisco")
        
        assert len(result["data"]) == 1
        assert result["data"][0]["job_title"] == "Senior Python Developer"
        assert result["data"][0]["job_min_salary"] == 120000
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_fetch_jobs_with_location(self, mock_get, mock_streamlit_secrets):
        """Test fetching jobs with location parameter"""
        from main import fetch_jobs_rapidapi
        
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response
        
        fetch_jobs_rapidapi("Data Scientist", "New York")
        
        call_args = mock_get.call_args
        assert call_args[1]['params']['query'] == "Data Scientist in New York"
    
    @patch('requests.get')
    def test_fetch_jobs_without_location(self, mock_get, mock_streamlit_secrets):
        """Test fetching jobs without location parameter"""
        from main import fetch_jobs_rapidapi
        
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response
        
        fetch_jobs_rapidapi("Frontend Developer")
        
        call_args = mock_get.call_args
        assert call_args[1]['params']['query'] == "Frontend Developer"
    
    @patch('requests.get')
    def test_fetch_jobs_pagination(self, mock_get, mock_streamlit_secrets):
        """Test fetching jobs with pagination"""
        from main import fetch_jobs_rapidapi
        
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response
        
        fetch_jobs_rapidapi("DevOps Engineer", page=2)
        
        call_args = mock_get.call_args
        assert call_args[1]['params']['page'] == "2"
    
    @patch('requests.get')
    def test_fetch_jobs_empty_response(self, mock_get, mock_streamlit_secrets):
        """Test fetching jobs with empty response"""
        from main import fetch_jobs_rapidapi
        
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response
        
        result = fetch_jobs_rapidapi("Niche Job Title")
        
        assert result["data"] == []
    
    @patch('requests.get')
    def test_fetch_jobs_multiple_results(self, mock_get, mock_streamlit_secrets):
        """Test fetching multiple job results"""
        from main import fetch_jobs_rapidapi
        
        jobs_data = [
            {
                "job_id": str(i),
                "job_title": f"Job {i}",
                "employer_name": f"Company {i}",
                "job_city": "City",
                "job_country": "Country",
                "job_employment_type": "FULLTIME"
            }
            for i in range(5)
        ]
        
        mock_response = Mock()
        mock_response.json.return_value = {"data": jobs_data}
        mock_get.return_value = mock_response
        
        result = fetch_jobs_rapidapi("Generic Role")
        
        assert len(result["data"]) == 5
        assert result["data"][0]["job_title"] == "Job 0"
        assert result["data"][4]["job_title"] == "Job 4"
    
    @patch('requests.get')
    def test_fetch_jobs_api_error(self, mock_get, mock_streamlit_secrets):
        """Test fetching jobs when API returns error"""
        from main import fetch_jobs_rapidapi
        
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        result = fetch_jobs_rapidapi("Any Job")
        
        assert result == {"data": []}
    
    @patch('requests.get')
    def test_fetch_jobs_http_error(self, mock_get, mock_streamlit_secrets):
        """Test fetching jobs when API returns HTTP error"""
        from main import fetch_jobs_rapidapi
        
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_get.return_value = mock_response
        
        result = fetch_jobs_rapidapi("Any Job")
        
        assert result == {"data": []}
    
    @patch('requests.get')
    def test_fetch_jobs_correct_headers(self, mock_get, mock_streamlit_secrets):
        """Test that correct headers are sent to RapidAPI"""
        from main import fetch_jobs_rapidapi
        
        mock_response = Mock()
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response
        
        fetch_jobs_rapidapi("Test Job")
        
        call_args = mock_get.call_args
        headers = call_args[1]['headers']
        assert headers['X-RapidAPI-Key'] == mock_streamlit_secrets['RAPIDAPI_KEY']
        assert headers['X-RapidAPI-Host'] == 'jsearch.p.rapidapi.com'


class TestIntegration:
    """Integration tests for complete workflow"""
    
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    @patch('requests.get')
    @patch('PyPDF2.PdfReader')
    def test_complete_workflow(self, mock_pdf, mock_get, mock_configure, mock_model_class, mock_streamlit_secrets):
        """Test complete workflow: PDF extraction -> Resume analysis -> Job search"""
        from main import extract_text_from_pdf, analyze_resume, fetch_jobs_rapidapi
        
        mock_page = Mock()
        mock_page.extract_text.return_value = "Python Developer with 5 years experience"
        mock_pdf.return_value.pages = [mock_page]
        
        mock_file = Mock()
        resume_text = extract_text_from_pdf(mock_file)
        assert "Python" in resume_text
        
        mock_response = Mock()
        mock_response.text = json.dumps({
            "Primary job role": "Software Engineer",
            "Key skills": ["Python"],
            "Years of experience": "5 years",
            "Key achievements": [],
            "Preferred job titles": ["Senior Developer"]
        })
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model
        
        analysis = analyze_resume(resume_text)
        assert analysis["Primary job role"] == "Software Engineer"
        
        mock_job_response = Mock()
        mock_job_response.json.return_value = {
            "data": [{"job_title": "Senior Developer", "employer_name": "Tech Corp"}]
        }
        mock_get.return_value = mock_job_response
        
        jobs = fetch_jobs_rapidapi(analysis["Primary job role"])
        assert len(jobs["data"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
