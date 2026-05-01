import streamlit as st
import requests

# URL of your FastAPI backend
FASTAPI_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📝")
st.title("AI Resume Analyzer 📝")

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if not st.session_state.form_submitted:
    with st.form("my_form"):
        resume_file = st.file_uploader(label="Upload your Resume/CV in PDF format", type="pdf")
        job_desc = st.text_area("Enter the Job Description of the role you are applying for:", placeholder="Job Description...")
        
        submitted = st.form_submit_button("Analyze")
        
        if submitted:
            if job_desc and resume_file:
                with st.spinner("Analyzing resume... This might take a few seconds."):
                    # Prepare data to send to FastAPI
                    files = {"resume_file": (resume_file.name, resume_file.getvalue(), "application/pdf")}
                    data = {"job_desc": job_desc}
                    
                    try:
                        # Call the backend API
                        response = requests.post(FASTAPI_URL, files=files, data=data)
                        
                        if response.status_code == 200:
                            st.session_state.analysis_data = response.json()
                            st.session_state.form_submitted = True
                            st.rerun()
                        else:
                            st.error(f"Backend Error: {response.json().get('detail', 'Unknown error')}")
                    except requests.exceptions.ConnectionError:
                        st.error("Failed to connect to the backend. Is the FastAPI server running?")
            else:
                st.warning("Please upload both a Resume and a Job Description to analyze.")

# Display Results
if st.session_state.form_submitted and st.session_state.analysis_data:
    data = st.session_state.analysis_data
    
    st.success("Analysis complete!")
    
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.write("Similarity Match (ATS):")
        # Formatting as a percentage for better UX
        st.subheader(f"{data['similarity_score'] * 100:.2f}%")

    with col2:
        st.write("Qualitative Average (AI):")
        # Showing as a standard decimal
        st.subheader(f"{data['average_score']:.2f} / 1.0")

    st.subheader("AI Generated Analysis Report:")
    
    # Displaying Report using Streamlit's native markdown for better rendering
    st.markdown(data['report'])
    
    # Download Button
    st.download_button(
        label="Download Report",
        data=data['report'],
        file_name="resume_analysis_report.txt",
        icon=":material/download:",
    )
    
    # Reset button to allow analyzing another resume
    if st.button("Analyze Another Resume"):
        st.session_state.form_submitted = False
        st.session_state.analysis_data = None
        st.rerun()
