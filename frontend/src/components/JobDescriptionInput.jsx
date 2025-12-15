import React from 'react';

function JobDescriptionInput({ value, onChange }) {
  return (
    <div className="job-description-section">
      <h2>Job Description</h2>
      <textarea
        placeholder="Paste the job description here..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        rows={10}
        className="job-description-input"
      />
      <p className="input-hint">
        Include the full job description with required skills, qualifications, and responsibilities
      </p>
    </div>
  );
}

export default JobDescriptionInput;
