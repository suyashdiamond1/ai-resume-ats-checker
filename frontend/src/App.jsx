import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import JobDescriptionInput from './components/JobDescriptionInput';
import ResultsDashboard from './components/ResultsDashboard';
import axios from 'axios';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    if (!resumeFile && !resumeText.trim()) {
      setError('Please upload a resume or enter resume text');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const formData = new FormData();
      formData.append('job_description', jobDescription);

      if (resumeFile) {
        formData.append('resume_file', resumeFile);
      } else {
        formData.append('resume_text', resumeText);
      }

      const response = await axios.post('/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setResumeFile(null);
    setResumeText('');
    setJobDescription('');
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>AI Resume ATS Checker</h1>
        <p>Optimize your resume for Applicant Tracking Systems</p>
      </header>

      <main className="app-main">
        {!results ? (
          <div className="input-section">
            <FileUpload
              onFileSelect={setResumeFile}
              onTextChange={setResumeText}
              resumeFile={resumeFile}
              resumeText={resumeText}
            />

            <JobDescriptionInput
              value={jobDescription}
              onChange={setJobDescription}
            />

            {error && <div className="error-message">{error}</div>}

            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Analyze Resume'}
            </button>
          </div>
        ) : (
          <div className="results-section">
            <ResultsDashboard results={results} onReset={handleReset} />
            <button className="reset-button" onClick={handleReset} aria-label="Analyze Another Resume">
              Analyze Another Resume
            </button>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>This tool provides indicative ATS analysis only and does not guarantee job placement.</p>
        <p>© 2025 AI Resume ATS Checker - Open Source Project</p>
      </footer>
    </div>
  );
}

export default App;
