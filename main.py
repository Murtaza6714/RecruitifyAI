
import streamlit as st
import PyPDF2
import openai
import requests
import json
from datetime import datetime

RAPIDAPI_KEY = "c5ac9d5e75msh0ad1714a2260ef0p12bea4jsn6b409a897083" 

if 'resume_analysis' not in st.session_state:
    st.session_state.resume_analysis = None
if 'jobs' not in st.session_state:
    st.session_state.jobs = None

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
    
    # Configure the API
    GEMINI_API_KEY = "AIzaSyBzMDJJ0wTuVxQUW3m5goFqQ-dtAFWdh6w"
    genai.configure(api_key=GEMINI_API_KEY)
    
    # Initialize the model
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    
    
    # Define the prompt with explicit instructions to return JSON
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
        # Generate response
        response = model.generate_content(prompt)
        
        
        
        
        # Clean the response text
        response_text = response.text.strip()
        
        # Remove any markdown code block indicators if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        response_text = response_text.strip()
        
        # Debug: Print cleaned response
        st.write("Cleaned Response:", response_text)
        
        # Parse JSON
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
        background: #fdfdfd;  /* not pure white */
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
}
    .job-title {
        color: #2d3748;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .job-company {
        color: #4a5568;
        font-size: 1.1rem;
        margin-bottom: 0.3rem;
    }
    .job-detail {
        color: #718096;
        font-size: 0.95rem;
        margin: 0.15rem 0;
    }
    .salary-badge {
        background: #edf2f7;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        color: #2d3748;
        font-weight: 500;
        font-size: 0.9rem;
        display: inline-block;
        margin: 0.4rem 0;
    }
    .apply-btn {
        background: linear-gradient(90deg, #ff6b6b, #ff8e53);
        color: white !important;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(255, 107, 107, 0.3);
    }
    .apply-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 107, 107, 0.4);
    }
    .job-type {
        background: #e6fffa;
        color: #319795;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        display: inline-block;
        margin-top: 0.3rem;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        # Main card wrapper
        st.markdown('<div class="job-card">', unsafe_allow_html=True)

        # Top section
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<div class="job-title">{job["job_title"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="job-company">🏢 {job["employer_name"]}</div>', unsafe_allow_html=True)
            
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

        # Description in expander
        with st.expander("📋 View Job Description & Details"):
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

        # Apply button center aligned
        if job.get("job_apply_link"):
            st.markdown(f"""
            <div style="text-align: center;">
                <a href="{job['job_apply_link']}" target="_blank" class="apply-btn">🚀 Apply Now</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
def main():
    st.title("🎯 RecruitifyAI")
    st.write("Upload your resume and let AI find the perfect job matches for you!")

    # File upload
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    # Location filter
    location = st.text_input("Enter location (optional)", "")

    if uploaded_file:
        with st.spinner("📑 Analyzing your resume..."):
            # Extract text and analyze only once
            resume_text = extract_text_from_pdf(uploaded_file)
            if not st.session_state.resume_analysis:
                st.session_state.resume_analysis = analyze_resume(resume_text)

            st.markdown("## 📄 Resume Summary", unsafe_allow_html=True)

            # Two column layout for Resume Insights
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🧑‍💼 Profile")
                st.markdown(f"- **Primary Role:** {st.session_state.resume_analysis['Primary job role']}")
                st.markdown(f"- **Years of Experience:** {st.session_state.resume_analysis['Years of experience']}")

                st.markdown("### 🛠️ Key Skills")
                skills = st.session_state.resume_analysis.get("Key skills", [])
                if skills:
                    st.markdown(
                        "<ul style='margin-top:0;'>"
                        + "".join([f"<li>{skill}</li>" for skill in skills])
                        + "</ul>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("No key skills extracted.")

            with col2:
                st.markdown("### 🏆 Key Achievements")
                achievements = st.session_state.resume_analysis.get("Key achievements", [])
                if achievements:
                    st.markdown(
                        "<ul style='margin-top:0;'>"
                        + "".join([f"<li>{achievement}</li>" for achievement in achievements])
                        + "</ul>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("No achievements found.")

            # Divider
            st.markdown("---")

            # Job search section
            st.markdown("## 🔍 Job Matches")

            # Filter options
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

            if st.button("🚀 Find Matching Jobs"):
                with st.spinner("🔎 Searching for jobs..."):
                    jobs_response = fetch_jobs_rapidapi(
                        st.session_state.resume_analysis['Primary job role'],
                        location
                    )

                    if jobs_response and 'data' in jobs_response:
                        jobs = jobs_response['data']

                        # Apply employment filter
                        if employment_type != "All":
                            jobs = [
                                job for job in jobs
                                if job.get('job_employment_type', '').upper() == employment_type
                            ]

                        if jobs:
                            st.success(f"✅ Found {len(jobs)} matching jobs")

                            # Display job cards
                            for job in jobs:
                                display_job_card(job)

                            # Pagination (load more)
                            if len(jobs) >= 10:
                                col1, col2, col3 = st.columns([1, 2, 1])
                                with col2:
                                    if st.button("⬇️ Load More Jobs"):
                                        current_page = len(jobs) // 10 + 1
                                        more_jobs = fetch_jobs_rapidapi(
                                            st.session_state.resume_analysis['Primary job role'],
                                            location,
                                            page=current_page
                                        )
                                        if more_jobs.get("data"):
                                            jobs.extend(more_jobs["data"])
                                            for job in more_jobs["data"]:
                                                display_job_card(job)
                        else:
                            st.warning("⚠️ No jobs found matching your filters.")
                    else:
                        st.error("❌ Unable to find jobs. Please try again later.")

    
if __name__ == "__main__":
    main()
