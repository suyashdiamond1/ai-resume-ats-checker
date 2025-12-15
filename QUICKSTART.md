# Quick Start Guide

## For Development

### Prerequisites
```bash
# Check versions
python --version  # Should be 3.11+
node --version    # Should be 18+
```

### Installation Steps

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/ai-resume-ats-checker.git
cd ai-resume-ats-checker
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
# Activate venv if not already active
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Visit: http://localhost:3000

## For Production (Docker)

```bash
docker-compose up --build
```

Visit: http://localhost:3000

## Testing the Application

1. Open http://localhost:3000
2. Upload a resume (PDF, DOCX, or TXT) or paste resume text
3. Paste a job description
4. Click "Analyze Resume"
5. Review the ATS score and suggestions

## API Testing

```bash
# Health check
curl http://localhost:8000/api/health

# Analyze with text
curl -X POST http://localhost:8000/api/analyze \
  -F "resume_text=Your resume text here" \
  -F "job_description=Job description here"

# Analyze with file
curl -X POST http://localhost:8000/api/analyze \
  -F "resume_file=@path/to/resume.pdf" \
  -F "job_description=Job description here"
```

## Troubleshooting

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Port already in use:**
- Backend: Change port in `backend/main.py`
- Frontend: Change port in `frontend/vite.config.js`

**CORS errors:**
- Ensure backend is running before frontend
- Check CORS settings in `backend/main.py`

## Need Help?

- Check API docs: http://localhost:8000/docs
- Open an issue on GitHub
- Review the main README.md
