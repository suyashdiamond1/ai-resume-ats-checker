import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

function FileUpload({ onFileSelect, onTextChange, resumeFile, resumeText }) {
  const onDrop = useCallback(
    (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0]);
        onTextChange(''); // Clear text input when file is uploaded
      }
    },
    [onFileSelect, onTextChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'text/plain': ['.txt'],
    },
    multiple: false,
  });

  return (
    <div className="upload-section">
      <h2>Upload Resume</h2>

      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        {resumeFile ? (
          <div className="file-info">
            <p>✓ {resumeFile.name}</p>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onFileSelect(null);
              }}
              className="remove-file"
            >
              Remove
            </button>
          </div>
        ) : (
          <div className="dropzone-content">
            <p>📄 Drag & drop your resume here, or click to browse</p>
            <p className="file-types">Supports: PDF, DOCX, TXT</p>
          </div>
        )}
      </div>

      <div className="divider">
        <span>OR</span>
      </div>

      <div className="text-input-section">
        <label htmlFor="resume-text">Paste Resume Text</label>
        <textarea
          id="resume-text"
          placeholder="Paste your resume text here..."
          value={resumeText}
          onChange={(e) => {
            onTextChange(e.target.value);
            if (e.target.value.trim()) {
              onFileSelect(null); // Clear file when text is entered
            }
          }}
          rows={8}
          disabled={!!resumeFile}
        />
      </div>
    </div>
  );
}

export default FileUpload;
