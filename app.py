import streamlit as st
import os
from utils.llm_handler import LLMHandler
from utils.document_engine import DocumentEngine

# Page configuration
st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("static/styles.css")

# Initialize handlers
if 'provider' not in st.session_state:
    st.session_state.provider = "Groq"

# Sidebar
st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Build Resume", "Cover Letter", "Digital Portfolio", "ATS Optimizer"])

st.sidebar.divider()
st.sidebar.subheader("⚙️ AI Configuration")

# Prioritize Groq as requested
groq_key = os.getenv("GROQ_API_KEY", "")
api_key_input = st.sidebar.text_input("Groq API Key", value=groq_key, type="password")

if not api_key_input:
    st.sidebar.warning("Please provide a Groq API Key to proceed.")

llm = LLMHandler(provider="Groq", api_key=api_key_input)
doc_engine = DocumentEngine()

# Home Page
if page == "Home":
    st.markdown('<div class="badge">AICTE – IBM SkillsBuild Internship</div>', unsafe_allow_html=True)
    st.title("💼 AI Resume & Portfolio Builder")
    
    st.markdown("""
    ### 🚀 Overview
    AI Resume & Portfolio Builder is an AI-driven application designed to help students create professional resumes, cover letters, and digital portfolios automatically.
    
    The system uses **Natural Language Processing (NLP)** and **Generative AI** techniques to tailor resumes according to job roles and student profiles.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        #### 🎯 Problem Statement
        Many students struggle to:
        - Create professional resumes
        - Highlight skills effectively
        - Match resumes to job descriptions
        - Optimize resumes for ATS systems
        """)
    with col2:
        st.success("""
        #### 💡 Proposed Solution
        The AI Resume Builder provides:
        - 📄 Tailored Resume Generation
        - ✍️ AI-based Content Optimization
        - 📨 Cover Letter Creation
        - 🌐 Digital Portfolio Layouts
        - 🔍 Keyword Optimization for ATS
        """)

    with st.expander("🏗️ System Architecture & How It Works"):
        st.markdown("""
        1. **User Inputs**: Personal Details, Education, Skills, Projects, Target Job Role.
        2. **NLP Processing**: Extraction of skills and keywords.
        3. **Role Matching**: Optimization based on target job description.
        4. **Document Generation**: AI crafts formatted Resume / Cover Letter output.
        """)

    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Features", "⚙️ Tech Stack", "🔮 Future Scope", "📽️ Project Slides"])
    
    with tab1:
        st.markdown("""
        - **ATS-friendly formatting**
        - **Role-based resume optimization**
        - **Keyword matching & Analysis**
        - **Easy export functionality (PDF)**
        """)
    
    with tab2:
        st.markdown("""
        - **Python** (Core Logic)
        - **Gemini / Groq** (Generative AI Models)
        - **Streamlit** (Interactive Frontend)
        - **NLP Techniques** (Content Extraction)
        """)

    with tab3:
        st.markdown("""
        - 🔗 LinkedIn profile integration
        - 🤖 AI-based Interview Preparation
        - 📊 Resume scoring system
        - 🌐 One-click portfolio website generation
        """)

    with tab4:
        st.markdown("""
        **🔹 Slide: Problem Statement**  
        Students often struggle to create professional resumes that highlight their skills effectively. Generic templates fail to showcase individual strengths. There is a need for an AI-based system that automatically generates personalized resumes and portfolios.

        **🔹 Slide: Proposed Solution**  
        The AI Resume Builder:  
        - Generates tailored resumes  
        - Suggests improvements  
        - Creates cover letters  
        - Builds digital portfolio layouts

        **🔹 Slide: System Development Approach**  
        - Python  
        - NLP for content optimization  
        - Resume template engine  
        - Streamlit / Gradio for deployment  
        - GitHub for version control

        **🔹 Slide: Algorithm & Deployment**  
        1. User enters personal details  
        2. AI analyzes skills & projects  
        3. System generates Resume & Cover Letter  
        4. Export in PDF format  

        **🔹 Slide: Result**  
        - Professional resume generation  
        - Improved job opportunities  
        - Time-saving solution
        """)

    st.sidebar.divider()
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);">
        <p style="margin-bottom: 5px; font-weight: 600; color: #F8FAFC;">👨‍💻 Author</p>
        <p style="margin: 0; font-size: 0.9rem; color: #CBD5E1;">Chukka Dhanushkoti</p>
        <p style="margin: 0; font-size: 0.8rem; color: #94A3B8;">Aditya College of Engineering and Technology</p>
        <p style="margin-top: 10px; font-size: 0.75rem; color: #6366F1; font-weight: 600;">AICTE – IBM SkillsBuild Internship</p>
    </div>
    """, unsafe_allow_html=True)

# Build Resume Page
elif page == "Build Resume":
    st.title("📄 Build Your Resume")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Your Profile Details")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        skills = st.text_area("Skills (comma-separated)", placeholder="Python, NLP, Streamlit, etc.")
        experience = st.text_area("Experience / Projects", placeholder="Describe your key projects and work history.")
        target_role = st.text_input("Target Job Role", placeholder="e.g., Data Scientist Junior")
        
        generate_btn = st.button("Generate Resume Content ✨")
    
    with col2:
        st.subheader("Generated Preview")
        if generate_btn:
            user_data = f"Name: {name}, Email: {email}, Phone: {phone}, Skills: {skills}, Experience: {experience}"
            with st.spinner("AI is crafting your resume..."):
                content = llm.generate_resume_sections(user_data, target_role)
                st.session_state['resume_content'] = content
                st.markdown(content)
                
                # PDF Generation
                pdf_path = doc_engine.create_pdf(content, "resume.pdf")
                with open(pdf_path, "rb") as f:
                    st.download_button("Download PDF", f, "resume.pdf", "application/pdf")

# Cover Letter Page
elif page == "Cover Letter":
    st.title("📨 Create Cover Letter")
    
    name = st.text_input("Full Name")
    target_role = st.text_input("Target Job Role")
    company_name = st.text_input("Company Name")
    user_details = st.text_area("Brief Background/Skills")
    
    if st.button("Generate Letter ✨"):
        with st.spinner("Writing your cover letter..."):
            letter = llm.generate_cover_letter(user_details, target_role, company_name)
            st.markdown(letter)
            
            pdf_path = doc_engine.create_pdf(letter, "cover_letter.pdf")
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, "cover_letter.pdf", "application/pdf")

# Digital Portfolio Page
elif page == "Digital Portfolio":
    st.title("🌐 Digital Portfolio Layout")
    
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    skills = st.text_input("Key Skills")
    summary = st.text_area("Short Bio")
    experience_summary = st.text_area("Project Highlights")
    
    if st.button("Generate Portfolio ✨"):
        user_data = {'name': name, 'email': email, 'skills': skills}
        sections = {'summary': summary, 'experience': experience_summary}
        
        html_path = doc_engine.create_html_portfolio(user_data, sections)
        st.success("Digital Portfolio Generated!")
        
        with open(html_path, "r", encoding="utf-8") as f:
            st.download_button("Download Portfolio HTML", f, "portfolio.html", "text/html")
            st.info("Download the HTML file and open it in your browser to see your digital portfolio!")

# ATS Optimizer Page
elif page == "ATS Optimizer":
    st.title("🔍 ATS Keyword Optimizer")
    
    resume_text = st.text_area("Paste your Resume Text", height=200)
    job_desc = st.text_area("Paste Job Description", height=200)
    
    if st.button("Analyze & Optimize 🚀"):
        with st.spinner("Analyzing keywords..."):
            optimization = llm.optimize_keywords(resume_text, job_desc)
            st.markdown(optimization)

# Footer
st.markdown("---")
st.markdown("""
<div class='project-footer'>
    <p style='color: #94A3B8;'>© 2024 AI Resume & Portfolio Builder | Developed for Academic Purposes</p>
    <p style='font-size: 0.75rem; color: #6366F1; font-weight: 600;'>Powered by Google Gemini & Groq AI</p>
</div>
""", unsafe_allow_html=True)
