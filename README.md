# AI Resume Analyzer

An intelligent, full-stack application that evaluates a candidate's resume against a specific job description. This tool uses a hybrid approach, combining mathematical semantic similarity (ATS scoring) with generative AI to provide actionable, qualitative feedback.
Features

**Dual-Engine Analysis:**
**ATS Similarity Score:** Uses BERT embeddings (`all-mpnet-base-v2`) to mathematically calculate the cosine similarity between the resume and the job description.
**Qualitative AI Feedback:** Integrates with the Groq API (running `Llama-3.3-70b-versatile`) to act as an AI recruiter, scoring individual job requirements and providing emoji-coded feedback.
**Separation of Concerns:** Built with a modern architecture featuring a high-performance **FastAPI** backend and an interactive **Streamlit** frontend.
**Efficient Processing:** The heavy machine learning model (BERT) is cached in memory on server startup to ensure lightning-fast subsequent requests.
**Exportable Reports:** Users can download their personalized AI analysis directly as a text file.

##  Tech Stack

**Backend:** FastAPI, Uvicorn, Python
**Frontend:** Streamlit, Requests
**Machine Learning & NLP:** Sentence-Transformers, scikit-learn
**LLM Integration:** Groq API (Llama 3)
**Utilities:** PDFMiner.six (PDF text extraction), python-dotenv

## Project Structure
```text
ai-resume-analyzer/
│
├── backend.py            # FastAPI server, ML models, and Groq API logic
├── frontend.py           # Streamlit user interface
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (API keys) - Ignored by Git
└── .gitignore            # Git ignore rules

