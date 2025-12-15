# 🎯 AI Resume ATS Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)

An AI-powered Resume ATS (Applicant Tracking System) Checker that analyzes resume compatibility against job descriptions using NLP and machine learning techniques.

## 📋 Overview

This tool helps job seekers optimize their resumes for Applicant Tracking Systems by:

- **Analyzing ATS Compatibility**: Scores resumes on a 0-100 scale
- **Keyword Matching**: Identifies matched and missing keywords from job descriptions
- **Section Detection**: Verifies presence of key resume sections (Skills, Experience, Education)
- **Actionable Suggestions**: Provides specific recommendations for improvement
- **Multi-format Support**: Accepts PDF, DOCX, and plain text resumes

## ✨ Features

### Core Features
- ✅ **PDF, DOCX, and TXT Resume Parsing** - Extract clean text from multiple file formats
- ✅ **TF-IDF Similarity Analysis** - Calculate semantic similarity between resume and job description
- ✅ **Keyword Extraction with NLP** - Use spaCy for intelligent keyword identification
- ✅ **Section Detection** - Automatically identify resume sections
- ✅ **Skill Gap Analysis** - Identify missing technical skills
- ✅ **Real-time Analysis** - Fast processing with immediate results
- ✅ **Responsive UI** - Modern, mobile-friendly interface
- ✅ **RESTful API** - Clean API design for easy integration

### Technical Features
- **Backend**: Python FastAPI with async support
- **NLP**: spaCy for natural language processing
- **ML**: scikit-learn for TF-IDF vectorization and cosine similarity
- **Frontend**: React with modern hooks and component architecture
- **File Parsing**: pdfplumber for PDFs, python-docx for DOCX files
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

## 🏗️ Project Structure

```
ai-resume-ats-checker/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py          # API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ats_scorer.py      # Core ATS scoring logic
│   │   └── resume_analyzer.py # Resume analysis service
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py      # PDF parsing
│   │   ├── docx_parser.py     # DOCX parsing
│   │   └── text_parser.py     # Text parsing
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx        # File upload component
│   │   │   ├── JobDescriptionInput.jsx
│   │   │   └── ResultsDashboard.jsx  # Results display
│   │   ├── styles/
│   │   │   └── App.css               # Styling
│   │   ├── App.jsx                   # Main React component
│   │   └── main.jsx                  # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── sample_resumes/            # Sample files for testing
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Installation

#### Option 1: Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-resume-ats-checker.git
cd ai-resume-ats-checker
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Set up the frontend**
```bash
cd ../frontend
npm install
```

4. **Run the application**

In one terminal (backend):
```bash
cd backend
python main.py
```

In another terminal (frontend):
```bash
cd frontend
npm run dev
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

#### Option 2: Docker Setup

```bash
docker-compose up --build
```

Access the application at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## 📖 Usage

### Web Interface

1. **Upload Resume**: Drag & drop or click to upload PDF/DOCX/TXT file, or paste resume text
2. **Enter Job Description**: Paste the target job description
3. **Analyze**: Click "Analyze Resume" button
4. **Review Results**: Get ATS score, keyword analysis, and improvement suggestions

### API Usage

**Endpoint**: `POST /api/analyze`

**Request** (multipart/form-data):
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Software Engineer position requiring Python, React, and AWS..."
```

**Response**:
```json
{
  "ats_score": 75,
  "matched_keywords": ["python", "react", "aws", "api", "docker"],
  "missing_keywords": ["kubernetes", "terraform", "ci/cd"],
  "section_analysis": {
    "skills": true,
    "experience": true,
    "education": true
  },
  "suggestions": [
    "Good alignment! Add a few more relevant keywords to improve further.",
    "Add these important keywords: kubernetes, terraform, ci/cd"
  ],
  "keyword_match_rate": 62.5,
  "skill_gaps": ["kubernetes", "terraform"]
}
```

## 🧪 Testing

### Backend Testing

Create a sample test:

```bash
cd backend
pytest
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to customize:
- CORS origins
- API prefix
- Host and port

### Frontend Configuration

Edit `frontend/vite.config.js` to customize:
- Proxy settings
- Build options
- Port

## 🎯 ATS Scoring Algorithm

The ATS score is calculated using:

1. **Keyword Match Rate (40%)**: Percentage of job description keywords found in resume
2. **TF-IDF Similarity (30%)**: Cosine similarity between resume and job description vectors
3. **Section Completeness (30%)**: Presence of key resume sections

Score Ranges:
- **80-100**: Excellent - Well-optimized for ATS
- **60-79**: Good - Minor improvements needed
- **40-59**: Fair - Moderate revision recommended
- **0-39**: Needs Work - Significant improvements required

## 📊 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **spaCy**: Industrial-strength NLP
- **scikit-learn**: Machine learning utilities
- **pdfplumber**: PDF text extraction
- **python-docx**: DOCX document parsing
- **Pydantic**: Data validation

### Frontend
- **React**: UI library
- **Vite**: Build tool
- **Axios**: HTTP client
- **react-dropzone**: File upload

## 🚧 Roadmap

- [ ] Add support for more file formats (RTF, ODT)
- [ ] Implement user accounts and history
- [ ] Add resume templates
- [ ] Integrate LLM for content rewriting suggestions
- [ ] Add A/B testing for resume variations
- [ ] Export analysis reports as PDF
- [ ] Add industry-specific ATS templates
- [ ] Multi-language support
- [ ] Browser extension
- [ ] Mobile app

## ⚠️ Ethical Disclaimer

**Important**: This tool provides indicative ATS analysis only and does not guarantee job placement or interview callbacks. Resume optimization is just one factor in the hiring process. 

- Use this tool as a guide, not a definitive solution
- Focus on genuine skills and experience
- Don't artificially inflate your qualifications
- Always be truthful in your resume content

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 (Python) and ESLint standards (JavaScript)
- Tests are included for new features
- Documentation is updated

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Authors

- Your Name - [GitHub Profile](https://github.com/yourusername)

## 🙏 Acknowledgments

- spaCy for excellent NLP capabilities
- FastAPI for the amazing web framework
- The open-source community

## 📧 Contact

For questions or feedback:
- Open an issue on GitHub
- Email: your.email@example.com

## 📈 Project Status

This project is actively maintained. Last updated: December 2025

---

**Star ⭐ this repository if you find it helpful!**
