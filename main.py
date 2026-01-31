
import streamlit as st
import PyPDF2
import openai
import requests
import json
from datetime import datetime

RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]

if 'resume_analysis' not in st.session_state:
    st.session_state.resume_analysis = None
if 'jobs' not in st.session_state:
    st.session_state.jobs = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'all_jobs' not in st.session_state:
    st.session_state.all_jobs = []

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text):
    """Analyze resume using Gemini API."""
    import google.generativeai as genai
    
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    
    
    prompt = f"""You must respond with ONLY a valid JSON object, no other text.
    Analyze this resume and return a JSON object with exactly this structure:
    {{
        "Primary job role": "string" (don't add words like student or studying),
        "Key skills": ["string"],
        "Years of experience": "string",
        "Key achievements": ["string"],
        "Preferred job titles": ["string"]
    }}

    Resume text:
    {resume_text}
    """

    try:
        response = model.generate_content(prompt)
        
        
        
        
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        response_text = response_text.strip()
        
        parsed_response = json.loads(response_text)
        return parsed_response

    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON response: {str(e)}")
        st.write("Failed to parse response:", response_text)
        return {}
    except Exception as e:
        st.error(f"Error calling Gemini API: {str(e)}")
        return {}


def fetch_jobs_rapidapi(job_title, location=None, page=1):
    """Fetch jobs using RapidAPI JSearch"""
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    query = job_title
    if location:
        query += f" in {location}"

    params = {
        "query": query,
        "page": str(page),
        "num_pages": "1"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching jobs: {str(e)}")
        return {"data": []}

# def display_job_card(job):
#     """Display a single job posting in a card format"""
#     with st.container():
#         st.markdown("---")

#         # Job header
#         col1, col2 = st.columns([3, 1])

#         with col1:
#             st.markdown(f"### {job['job_title']}")
#             st.markdown(f"**Company:** {job['employer_name']}")
#             location_str = f"{job.get('job_city', '')}, {job.get('job_country', '')}"
#             st.markdown(f"**Location:** {location_str.strip(', ')}")

#             if job.get('job_min_salary') and job.get('job_max_salary'):
#                 st.markdown(f"**Salary Range:** ${job['job_min_salary']:,} - ${job['job_max_salary']:,}")

#         with col2:
#             st.markdown(f"**Type:** {job.get('job_employment_type', 'Not specified')}")
#             if job.get('job_posted_at_datetime_utc'):
#                 posted_date = datetime.strptime(job['job_posted_at_datetime_utc'][:10], '%Y-%m-%d')
#                 st.markdown(f"**Posted:** {posted_date.strftime('%Y-%m-%d')}")

#         # Job details
#         with st.expander("Show Job Description"):
#             st.markdown(job.get('job_description', 'No description available'))

#             # Highlights section
#             if job.get('job_highlights'):
#                 if 'Qualifications' in job['job_highlights']:
#                     st.markdown("**Required Qualifications:**")
#                     for qual in job['job_highlights']['Qualifications']:
#                         st.markdown(f"- {qual}")

#                 if 'Benefits' in job['job_highlights']:
#                     st.markdown("**Benefits:**")
#                     for benefit in job['job_highlights']['Benefits']:
#                         st.markdown(f"- {benefit}")

#         # Apply button
#         if job.get('job_apply_link'):
#             st.markdown(f"[Apply Now]({job['job_apply_link']})")

def display_job_card(job):
    """Display a single job posting in a modern clean card format"""
    
    st.markdown("""
    <style>
    .job-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    .job-title {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .job-company {
        color: #4a5568;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .employer-logo {
        width: 60px;
        height: 60px;
        object-fit: contain;
        border-radius: 10px;
        background: white;
        padding: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .employer-website {
        color: #4f46e5;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .employer-website:hover {
        color: #7c3aed;
        text-decoration: underline;
    }
    .job-detail {
        color: #718096;
        font-size: 1rem;
        margin: 0.3rem 0;
    }
    .salary-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 0.6rem 1.2rem;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        display: inline-block;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    .apply-btn {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        margin-top: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
    }
    .apply-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6);
        color: white !important;
        text-decoration: none;
    }
    .job-type {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        font-size: 0.9rem;
        font-weight: 600;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
        box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        # st.markdown('<div class="job-card">', unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<div class="job-title">{job["job_title"]}</div>', unsafe_allow_html=True)
            
            company_col1, company_col2 = st.columns([0.15, 0.85])
            with company_col1:
                if job.get("employer_logo"):
                    st.markdown(f'<img src="{job["employer_logo"]}" class="employer-logo" alt="Company Logo">', unsafe_allow_html=True)
            with company_col2:
                st.markdown(f'<div class="job-company">🏢 {job["employer_name"]}</div>', unsafe_allow_html=True)
                if job.get("employer_website"):
                    st.markdown(f'<a href="{job["employer_website"]}" target="_blank" class="employer-website">🌐 Visit Company Website</a>', unsafe_allow_html=True)
            
            location_str = f"{job.get('job_city', '')}, {job.get('job_country', '')}"
            if location_str.strip(', '):
                st.markdown(f'<div class="job-detail">📍 {location_str.strip(", ")}</div>', unsafe_allow_html=True)
            
            if job.get("job_min_salary") and job.get("job_max_salary"):
                st.markdown(f'<div class="salary-badge">💰 ${job["job_min_salary"]:,} - ${job["job_max_salary"]:,}</div>', unsafe_allow_html=True)

        with col2:
            if job.get("job_employment_type"):
                st.markdown(f'<div class="job-type">{job["job_employment_type"]}</div>', unsafe_allow_html=True)
            
            if job.get("job_posted_at_datetime_utc"):
                posted_date = datetime.strptime(job["job_posted_at_datetime_utc"][:10], "%Y-%m-%d")
                days_ago = (datetime.now() - posted_date).days
                date_text = "Today" if days_ago == 0 else ("Yesterday" if days_ago == 1 else f"{days_ago} days ago")
                st.markdown(f'<div class="job-detail">🕒 {date_text}</div>', unsafe_allow_html=True)

        with st.expander("📋 View Job Description & Details"):
            if job.get("employer_logo"):
                st.image(job["employer_logo"], width=100)
            
            if job.get("employer_website"):
                st.markdown(f"**Company Website:** [{job['employer_website']}]({job['employer_website']})")
            
            st.markdown("---")
            st.markdown(job.get("job_description", "No description available"))

            if job.get("job_highlights"):
                if "Qualifications" in job["job_highlights"]:
                    st.markdown("### 🎓 Required Qualifications")
                    for qual in job["job_highlights"]["Qualifications"]:
                        st.markdown(f"- {qual}")

                if "Benefits" in job["job_highlights"]:
                    st.markdown("### 🎁 Benefits")
                    for benefit in job["job_highlights"]["Benefits"]:
                        st.markdown(f"- {benefit}")

        if job.get("job_apply_link"):
            st.markdown(f"""
            <div style="text-align: center;">
                <a href="{job['job_apply_link']}" target="_blank" class="apply-btn">🚀 Apply Now</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
def main():
    st.markdown("""
    <style>
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Remove default streamlit styling */
    .stApp > header {
        background-color: transparent;
    }
    
    .stApp {
        background: #f7f9fc;
        min-height: 100vh;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        text-align: center;
        border: none;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.95);
        margin-bottom: 0;
    }
    
    /* Content sections */
    .content-section {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Upload section */
    .upload-section {
        background: white;
        color: #2d3748;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Resume analysis styling */
    .resume-section {
        background: white;
        color: #2d3748;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    .resume-card {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
        padding: 1.8rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #d1d9f0;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.08);
        transition: all 0.3s ease;
    }
    
    .resume-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
    }
    
    /* Section headings */
    .resume-section h2 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .resume-section h3 {
        color: #4f46e5;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .resume-card h3 {
        color: #4f46e5;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
    }
    
    /* Job search section */
    .job-search-section {
        background: white;
        color: #2d3748;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6);
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background: white;
        border: 2px dashed #4f46e5;
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #7c3aed;
        background: #f8f9ff;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
    }
    
    .stError {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8f9ff;
        border-radius: 10px;
        font-weight: 600;
        color: #4f46e5;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .content-section {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🎯 RecruitifyAI</h1>
        <p class="main-subtitle">Upload your resume and let AI find the perfect job matches for you!</p>
    </div>
    """, unsafe_allow_html=True)

    # st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📄 Upload Your Resume")
    st.markdown("Upload your PDF resume to get started with AI-powered job matching")
    uploaded_file = st.file_uploader("Choose your resume file", type="pdf", label_visibility="collapsed")
    
    st.markdown("### 📍 Location Preference")
    location = st.text_input("Enter your preferred job location (optional)", "", placeholder="e.g., New York, NY or Remote")
    # st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:
        with st.spinner("📑 Analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not st.session_state.resume_analysis:
                st.session_state.resume_analysis = analyze_resume(resume_text)

            st.markdown('<div class="resume-section">', unsafe_allow_html=True)
            st.markdown("## 📄 Resume Analysis Results")
            st.markdown("Here's what our AI discovered about your professional profile:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # st.markdown('<div class="resume-card">', unsafe_allow_html=True)
                st.markdown("### 🧑‍💼 Professional Profile")
                st.markdown(f"**Primary Role:** {st.session_state.resume_analysis['Primary job role']}")
                st.markdown(f"**Experience Level:** {st.session_state.resume_analysis['Years of experience']}")
                # st.markdown('</div>', unsafe_allow_html=True)
                
                # st.markdown('<div class="resume-card">', unsafe_allow_html=True)
                st.markdown("### 🛠️ Core Skills")
                skills = st.session_state.resume_analysis.get("Key skills", [])
                if skills:
                    for skill in skills[:6]:  # Limit to top 6 skills
                        st.markdown(f"• {skill}")
                    if len(skills) > 6:
                        st.markdown(f"*...and {len(skills) - 6} more skills*")
                else:
                    st.markdown("*No key skills extracted*")
                # st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                # st.markdown('<div class="resume-card">', unsafe_allow_html=True)
                st.markdown("### 🏆 Key Achievements")
                achievements = st.session_state.resume_analysis.get("Key achievements", [])
                if achievements:
                    for achievement in achievements[:4]:  # Limit to top 4 achievements
                        st.markdown(f"• {achievement}")
                    if len(achievements) > 4:
                        st.markdown(f"*...and {len(achievements) - 4} more achievements*")
                else:
                    st.markdown("*No achievements found*")
                # st.markdown('</div>', unsafe_allow_html=True)
                
                # st.markdown('<div class="resume-card">', unsafe_allow_html=True)
                st.markdown("### 🎯 Recommended Job Titles")
                job_titles = st.session_state.resume_analysis.get("Preferred job titles", [])
                if job_titles:
                    for title in job_titles[:4]:  # Limit to top 4 titles
                        st.markdown(f"• {title}")
                else:
                    st.markdown("*Based on your primary role*")
                # st.markdown('</div>', unsafe_allow_html=True)
            
            # st.markdown('</div>', unsafe_allow_html=True)

            # st.markdown('<div class="job-search-section">', unsafe_allow_html=True)
            st.markdown("## 🔍 Find Your Perfect Job Match")
            st.markdown("Customize your job search with the filters below:")

            col1, col2 = st.columns(2)
            with col1:
                employment_type = st.selectbox(
                    "📌 Employment Type",
                    ["All", "FULLTIME", "PARTTIME", "CONTRACTOR", "INTERN"]
                )
            with col2:
                date_posted = st.selectbox(
                    "📅 Date Posted",
                    ["All", "Today", "3 days", "Week", "Month"]
                )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                search_clicked = st.button("🚀 Find Matching Jobs", use_container_width=True)
            
            # st.markdown('</div>', unsafe_allow_html=True)

            if search_clicked:
                st.session_state.current_page = 1
                st.session_state.all_jobs = []
                st.session_state.employment_type_filter = employment_type
                st.session_state.location_filter = location
                st.session_state.search_initiated = True

            if st.session_state.get('search_initiated', False):
                with st.spinner("🔎 Searching for jobs..."):
                    jobs_response = fetch_jobs_rapidapi(
                        st.session_state.resume_analysis['Primary job role'],
                        st.session_state.get('location_filter', location),
                        page=st.session_state.current_page
                    )

                    if jobs_response and 'data' in jobs_response:
                        jobs = jobs_response['data']
                        
                        employment_type_filter = st.session_state.get('employment_type_filter', 'All')
                        if employment_type_filter != "All":
                            jobs = [
                                job for job in jobs
                                if employment_type_filter in job.get('job_employment_types', [])
                            ]

                        if jobs:
                            st.success(f"✅ Found {len(jobs)} matching jobs on page {st.session_state.current_page}")
                            
                            JOBS_PER_PAGE = 10
                            for job in jobs[:JOBS_PER_PAGE]:
                                display_job_card(job)

                            st.markdown("---")
                            
                            pagination_col1, pagination_col2, pagination_col3, pagination_col4, pagination_col5 = st.columns([1, 1, 1, 1, 1])
                            
                            with pagination_col1:
                                if st.session_state.current_page > 1:
                                    if st.button("⏮️ First", use_container_width=True):
                                        st.session_state.current_page = 1
                                        st.rerun()
                            
                            with pagination_col2:
                                if st.session_state.current_page > 1:
                                    if st.button("◀️ Previous", use_container_width=True):
                                        st.session_state.current_page -= 1
                                        st.rerun()
                            
                            with pagination_col3:
                                st.markdown(f"<div style='text-align: center; padding: 0.5rem; font-weight: 600; color: #4f46e5;'>Page {st.session_state.current_page}</div>", unsafe_allow_html=True)
                            
                            with pagination_col4:
                                if len(jobs) >= JOBS_PER_PAGE:
                                    if st.button("Next ▶️", use_container_width=True):
                                        st.session_state.current_page += 1
                                        st.rerun()
                            
                            with pagination_col5:
                                if len(jobs) >= JOBS_PER_PAGE:
                                    if st.button("Last ⏭️", use_container_width=True):
                                        st.session_state.current_page += 5
                                        st.rerun()
                        else:
                            st.warning("⚠️ No jobs found matching your filters. Try adjusting your search criteria.")
                    else:
                        st.error("❌ Unable to find jobs. Please check your internet connection and try again.")

    # Footer
    st.markdown("""
    <div style="
        margin-top: 3rem;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        color: #6b7280;
    ">
        <p style="margin: 0; font-size: 1rem;">
            🎆 Powered by AI • Built with ❤️ for Job Seekers • 🚀 RecruitifyAI 2024
        </p>
    </div>
    """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()
