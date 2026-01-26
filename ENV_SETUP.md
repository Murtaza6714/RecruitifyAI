# Environment Variables Setup Guide

## Overview
This guide explains how to set up environment variables for running tests and the application locally.

## Quick Start

### 1. Create `.env` File
Copy the example file and add your actual API keys:

```bash
cp .env.example .env
```

### 2. Edit `.env` File
Open `.env` and replace placeholder values with your actual API keys:

```env
GEMINI_API_KEY=your-actual-gemini-api-key-here
RAPIDAPI_KEY=your-actual-rapidapi-key-here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Tests
```bash
pytest test_apis.py -v
```

---

## Getting API Keys

### Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key
4. Paste into `.env` as `GEMINI_API_KEY`

### RapidAPI Key
1. Sign up at [RapidAPI](https://rapidapi.com/)
2. Go to your Dashboard
3. Click on "API Keys" or "Apps"
4. Copy your API key
5. Paste into `.env` as `RAPIDAPI_KEY`

---

## Environment Variable Loading

### For Tests
Tests automatically load from `.env` file via `conftest.py`:

```python
# conftest.py handles this automatically
load_dotenv()
```

### For Streamlit App (Local)
Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
RAPIDAPI_KEY = "your-rapidapi-key"
```

### For Streamlit Cloud Deployment
1. Go to your Streamlit Cloud app settings
2. Navigate to **Secrets** section
3. Add:
```toml
GEMINI_API_KEY = "your-gemini-api-key"
RAPIDAPI_KEY = "your-rapidapi-key"
```

---

## File Structure

```
jobhuntai/
├── .env                 # Local environment variables (GITIGNORED)
├── .env.example         # Template for .env file
├── .gitignore           # Ignores .env and .streamlit/
├── .streamlit/
│   └── secrets.toml     # Streamlit secrets (GITIGNORED)
├── conftest.py          # Pytest configuration with env loading
├── test_apis.py         # Test suite using fixtures
├── test_utils.py        # Test utilities and mock data
├── main.py              # Main Streamlit app
└── requirements.txt     # Python dependencies
```

---

## Running Tests with Environment Variables

### All Tests
```bash
pytest test_apis.py -v
```

### Specific Test Class
```bash
pytest test_apis.py::TestGeminiAPI -v
```

### With Coverage Report
```bash
pytest test_apis.py --cov=main --cov-report=html
```

### Using Test Runner Script
```bash
python run_tests.py --all
python run_tests.py --gemini
python run_tests.py --rapidapi
python run_tests.py --coverage
```

---

## How Environment Variables Are Used

### In Tests
Tests use the `mock_streamlit_secrets` fixture from `conftest.py`:

```python
def test_example(self, mock_streamlit_secrets):
    # mock_streamlit_secrets contains:
    # {'GEMINI_API_KEY': '...', 'RAPIDAPI_KEY': '...'}
    api_key = mock_streamlit_secrets['GEMINI_API_KEY']
```

### In Main App
The app uses Streamlit's secrets:

```python
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]
```

---

## Troubleshooting

### Issue: `KeyError: 'GEMINI_API_KEY'`
**Solution**: Ensure `.env` file exists and contains the key:
```bash
cat .env
```

### Issue: Tests fail with "No module named 'dotenv'"
**Solution**: Install dependencies:
```bash
pip install python-dotenv
```

### Issue: `.env` file not being loaded
**Solution**: Verify file is in project root:
```bash
ls -la .env
```

### Issue: Streamlit app can't find secrets
**Solution**: For local testing, create `.streamlit/secrets.toml`:
```bash
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "your-key"' > .streamlit/secrets.toml
echo 'RAPIDAPI_KEY = "your-key"' >> .streamlit/secrets.toml
```

---

## Security Best Practices

✅ **DO:**
- Store API keys in `.env` (local) or Streamlit Secrets (cloud)
- Add `.env` to `.gitignore` (already done)
- Use environment variables in code
- Rotate API keys periodically
- Use different keys for dev/prod

❌ **DON'T:**
- Commit `.env` to git
- Hardcode API keys in source code
- Share API keys in chat or email
- Use same key for multiple environments
- Log API keys in error messages

---

## Environment Variables Reference

| Variable | Purpose | Where to Get |
|----------|---------|--------------|
| `GEMINI_API_KEY` | Google Generative AI API | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `RAPIDAPI_KEY` | RapidAPI JSearch API | [RapidAPI Dashboard](https://rapidapi.com/dashboard) |

---

## Testing Without Real API Keys

Tests use mocked APIs, so you can run them with dummy keys:

```env
GEMINI_API_KEY=test-key-12345
RAPIDAPI_KEY=test-key-67890
```

The mocks will intercept API calls and return test data.

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest test_apis.py -v
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          RAPIDAPI_KEY: ${{ secrets.RAPIDAPI_KEY }}
```

---

## Next Steps

1. ✅ Copy `.env.example` to `.env`
2. ✅ Add your API keys to `.env`
3. ✅ Run `pip install -r requirements.txt`
4. ✅ Run `pytest test_apis.py -v`
5. ✅ Run `streamlit run main.py` to test locally

---

## Support

For issues with environment variables:
1. Check that `.env` file exists in project root
2. Verify API keys are correct
3. Ensure `python-dotenv` is installed
4. Check `.gitignore` includes `.env`
