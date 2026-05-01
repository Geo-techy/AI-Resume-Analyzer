# AI Resume Analyzer

An intelligent, full-stack application that evaluates a candidate's resume against a specific job description. This tool uses a hybrid approach, combining mathematical semantic similarity (ATS scoring) with generative AI to provide actionable, qualitative feedback.
Features

* **Dual-Engine Analysis:** 
  * **ATS Similarity Score:** Uses BERT embeddings (`all-mpnet-base-v2`) to mathematically calculate the cosine similarity between the resume and the job description.
  * **Qualitative AI Feedback:** Integrates with the Groq API (running `Llama-3.3-70b-versatile`) to act as an AI recruiter, scoring individual job requirements and providing emoji-coded feedback.
* **Separation of Concerns:** Built with a modern architecture featuring a high-performance **FastAPI** backend and an interactive **Streamlit** frontend.
* **Efficient Processing:** The heavy machine learning model (BERT) is cached in memory on server startup to ensure lightning-fast subsequent requests.
* **Exportable Reports:** Users can download their personalized AI analysis directly as a text file.

##  Tech Stack

* **Backend:** FastAPI, Uvicorn, Python
* **Frontend:** Streamlit, Requests
* **Machine Learning & NLP:** Sentence-Transformers, scikit-learn
* **LLM Integration:** Groq API (Llama 3)
* **Utilities:** PDFMiner.six (PDF text extraction), python-dotenv

## Project Structure
```text
ai-resume-analyzer/
│
├── backend.py            # FastAPI server, ML models, and Groq API logic
├── frontend.py           # Streamlit user interface
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys) - Ignored by Git
└── .gitignore            # Git ignore rules

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

1. Create an account on Groq and generate an API key.
2. Create a `.env` file in the root directory of the project.
3. Add the following line to the `.env` file:

```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

---

#  Running the Application

This project uses a **decoupled architecture**, so the backend and frontend must be run in **two separate terminal windows**.

## Start the Backend

Open a terminal inside the project folder and run:

```bash
uvicorn backend:app --reload
```

Wait until you see:

```bash
Application startup complete
```

---

## Start the Frontend

Open a second terminal in the same project folder and run:

```bash
streamlit run frontend.py
```

The application interface will automatically open in your default web browser.

---

# How to Use

1. **Upload Resume**
   Upload your resume in **PDF format**.

2. **Paste Job Description**
   Enter the target job description into the provided text area.

3. **Analyze Resume**
   Click the **Analyze** button to generate:

   * ATS compatibility score
   * Skill match analysis
   * AI-generated feedback and suggestions

4. **Download Report**
   Save the generated analysis report locally using the **Download Report** button.


