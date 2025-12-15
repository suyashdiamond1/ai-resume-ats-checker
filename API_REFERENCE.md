# API Reference

Complete API documentation for the AI Resume ATS Checker backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production, consider implementing:
- API keys
- OAuth 2.0
- JWT tokens

---

## Endpoints

### 1. Health Check

Check if the API is running.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "Resume ATS Checker"
}
```

**Status Codes:**
- `200`: Service is healthy

**Example:**
```bash
curl http://localhost:8000/api/health
```

---

### 2. Analyze Resume

Analyze a resume against a job description.

**Endpoint:** `POST /api/analyze`

**Content-Type:** `multipart/form-data`

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `job_description` | string | Yes | Job description text (min 10 chars) |
| `resume_file` | file | No* | Resume file (PDF, DOCX, or TXT) |
| `resume_text` | string | No* | Resume as plain text |

*Note: Either `resume_file` OR `resume_text` must be provided.

**Supported File Formats:**
- PDF (`.pdf`)
- Microsoft Word (`.docx`, `.doc`)
- Plain Text (`.txt`)

**Request Example (with file):**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "resume_file=@/path/to/resume.pdf" \
  -F "job_description=We are seeking a Python developer..."
```

**Request Example (with text):**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "resume_text=John Doe\nSoftware Engineer\n..." \
  -F "job_description=We are seeking a Python developer..."
```

**Response:**
```json
{
  "ats_score": 75,
  "matched_keywords": [
    "python",
    "javascript",
    "react",
    "aws",
    "docker",
    "api",
    "postgresql"
  ],
  "missing_keywords": [
    "kubernetes",
    "terraform",
    "ci/cd",
    "graphql"
  ],
  "section_analysis": {
    "skills": true,
    "experience": true,
    "education": true
  },
  "suggestions": [
    "Good alignment! Add a few more relevant keywords to improve further.",
    "Add these important keywords: kubernetes, terraform, ci/cd, graphql",
    "Use standard section headings (Skills, Experience, Education) for better ATS parsing.",
    "Include specific achievements with metrics where possible.",
    "Avoid tables, images, and complex formatting that ATS systems may not parse correctly."
  ],
  "keyword_match_rate": 63.64,
  "skill_gaps": [
    "kubernetes",
    "terraform"
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `ats_score` | integer | ATS compatibility score (0-100) |
| `matched_keywords` | array | Keywords found in both resume and job description |
| `missing_keywords` | array | Important keywords from job description not in resume |
| `section_analysis` | object | Presence of key resume sections |
| `section_analysis.skills` | boolean | Whether skills section detected |
| `section_analysis.experience` | boolean | Whether experience section detected |
| `section_analysis.education` | boolean | Whether education section detected |
| `suggestions` | array | Actionable improvement recommendations |
| `keyword_match_rate` | float | Percentage of job keywords found (0-100) |
| `skill_gaps` | array | Technical skills missing from resume |

**Status Codes:**

| Code | Description |
|------|-------------|
| `200` | Success - Analysis completed |
| `400` | Bad Request - Invalid input or missing required fields |
| `500` | Internal Server Error - Processing failed |

**Error Response:**
```json
{
  "detail": "Resume content is too short or could not be extracted properly"
}
```

**Common Error Messages:**

| Error | Cause | Solution |
|-------|-------|----------|
| "Either resume_file or resume_text must be provided" | No resume input | Provide either a file or text |
| "Unsupported file format" | Invalid file type | Use PDF, DOCX, or TXT |
| "Resume content is too short" | Insufficient content | Ensure resume has at least 50 characters |
| "Job description is too short" | Insufficient content | Provide detailed job description (20+ chars) |

---

### 3. Root Endpoint

Get API information and available endpoints.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "AI Resume ATS Checker API",
  "version": "1.0.0",
  "endpoints": {
    "analyze": "/api/analyze",
    "health": "/api/health",
    "docs": "/docs"
  }
}
```

---

## Interactive Documentation

The API provides auto-generated interactive documentation:

### Swagger UI
```
http://localhost:8000/docs
```
- Try out endpoints directly
- See request/response schemas
- View all available operations

### ReDoc
```
http://localhost:8000/redoc
```
- Clean, readable documentation
- Three-panel layout
- Search functionality

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:
- Implementing rate limiting per IP
- Using API keys with quotas
- Caching frequent analyses

---

## CORS

CORS is configured to allow all origins (`*`). For production:

```python
# In backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Data Processing Pipeline

1. **Input Validation**: Check required fields and formats
2. **File Parsing**: Extract text from PDF/DOCX/TXT
3. **Text Cleaning**: Normalize whitespace and formatting
4. **Keyword Extraction**: Use spaCy NLP to identify keywords
5. **TF-IDF Analysis**: Calculate semantic similarity
6. **Section Detection**: Identify resume structure
7. **Score Calculation**: Weighted algorithm (40% keywords, 30% TF-IDF, 30% sections)
8. **Suggestion Generation**: Create actionable recommendations

---

## Score Interpretation

| Score Range | Rating | Interpretation |
|-------------|--------|----------------|
| 80-100 | Excellent | Well-optimized for ATS |
| 60-79 | Good | Minor improvements needed |
| 40-59 | Fair | Moderate revision recommended |
| 0-39 | Needs Work | Significant improvements required |

---

## Best Practices

### For API Consumers

1. **File Size**: Keep resume files under 5MB
2. **File Quality**: Use clean, text-based PDFs (not scanned images)
3. **Job Descriptions**: Provide complete, detailed job postings
4. **Error Handling**: Always check status codes and handle errors
5. **Timeouts**: Set appropriate timeout values (30+ seconds)

### For Developers

1. **Input Validation**: Always validate before processing
2. **Error Logging**: Log errors for debugging
3. **Caching**: Consider caching for duplicate requests
4. **Monitoring**: Track API usage and performance
5. **Security**: Sanitize file uploads in production

---

## Python Client Example

```python
import requests

def analyze_resume(resume_path: str, job_description: str) -> dict:
    """Analyze resume using the API"""
    url = "http://localhost:8000/api/analyze"
    
    with open(resume_path, 'rb') as f:
        files = {'resume_file': f}
        data = {'job_description': job_description}
        
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        
        return response.json()

# Usage
result = analyze_resume(
    resume_path="resume.pdf",
    job_description="Python developer position..."
)

print(f"ATS Score: {result['ats_score']}")
print(f"Matched: {result['matched_keywords']}")
print(f"Missing: {result['missing_keywords']}")
```

---

## JavaScript Client Example

```javascript
async function analyzeResume(resumeFile, jobDescription) {
  const formData = new FormData();
  formData.append('resume_file', resumeFile);
  formData.append('job_description', jobDescription);

  try {
    const response = await fetch('http://localhost:8000/api/analyze', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Analysis failed:', error);
    throw error;
  }
}

// Usage
const fileInput = document.querySelector('#resume-file');
const jobDesc = document.querySelector('#job-description').value;

const result = await analyzeResume(fileInput.files[0], jobDesc);
console.log('ATS Score:', result.ats_score);
```

---

## Deployment Considerations

### Environment Variables

Consider using environment variables for:
- API host and port
- CORS origins
- File size limits
- spaCy model path

### Performance

- Response time: < 5 seconds for typical resumes
- Concurrent requests: Tested up to 10 simultaneous
- Memory usage: ~200MB per worker

### Scaling

For high traffic:
1. Use multiple worker processes: `uvicorn main:app --workers 4`
2. Deploy behind a load balancer
3. Cache analysis results
4. Use async file processing

---

## Troubleshooting

### Common Issues

**Issue:** spaCy model not found
```bash
Solution: python -m spacy download en_core_web_sm
```

**Issue:** PDF parsing fails
```bash
Solution: Ensure PDF is text-based, not scanned image
```

**Issue:** CORS errors
```bash
Solution: Check CORS configuration in backend/main.py
```

---

## Support

- API Documentation: http://localhost:8000/docs
- GitHub Issues: [Repository Issues](https://github.com/yourusername/ai-resume-ats-checker/issues)
- Email: support@example.com

---

**API Version:** 1.0.0  
**Last Updated:** December 2025
