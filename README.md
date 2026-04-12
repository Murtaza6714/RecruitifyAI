# RecruitifyAI

An AI-powered job search assistant that analyzes your resume and finds matching job listings. Upload a PDF resume, get an AI-generated profile summary via Google Gemini, and browse live job postings fetched from the JSearch API.

---

## Prerequisites

- Python 3.9 or higher
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- A [RapidAPI key](https://rapidapi.com/) with access to the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/RecruitifyAI.git
   cd RecruitifyAI
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**

   Create the file `.streamlit/secrets.toml` in the project root with the following content:

   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   RAPIDAPI_KEY  = "your_rapidapi_key_here"
   ```

   > **Note:** Never commit `secrets.toml` to version control. It is already listed in `.gitignore`.

---

## Running the App

```bash
streamlit run main.py
```

Streamlit will start a local development server and open the app in your default browser. The default URL is `http://localhost:8501`.

---

## Running Tests

The project uses `pytest`. You can run tests via the convenience runner script or directly with `pytest`.

### Using the runner script

```bash
# Run all tests
python run_tests.py --all

# Run a specific suite
python run_tests.py --pdf          # PDF extraction tests
python run_tests.py --gemini       # Gemini API tests
python run_tests.py --rapidapi     # RapidAPI / JSearch tests
python run_tests.py --integration  # Integration tests

# Additional options
python run_tests.py --verbose      # Verbose output
python run_tests.py --coverage     # Generate HTML coverage report
```

### Using pytest directly

```bash
# Run all tests
pytest test_apis.py -v

# Run with coverage
pytest test_apis.py --cov=main --cov-report=html --cov-report=term
```

---

## Project Structure

```
RecruitifyAI/
├── main.py              # Streamlit application entry point
├── requirements.txt     # Python dependencies
├── conftest.py          # pytest fixtures and configuration
├── test_apis.py         # API and integration tests
├── test_utils.py        # Utility/unit tests
├── run_tests.py         # Test runner helper script
└── .streamlit/
    └── secrets.toml     # API keys (not committed to version control)
```
