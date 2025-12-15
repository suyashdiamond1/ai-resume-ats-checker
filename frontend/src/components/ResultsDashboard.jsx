import React from 'react';

const tierForScore = (score) => {
  if (score >= 80) return 'Excellent';
  if (score >= 65) return 'Good';
  if (score >= 45) return 'Fair';
  return 'Poor';
};

const colorForScore = (score) => {
  if (score >= 80) return '#16a34a'; // success
  if (score >= 65) return '#f59e0b'; // warn
  if (score >= 45) return '#f59e0b';
  return '#ef4444'; // danger
};

function Radial({ value }) {
  const clamped = Math.max(0, Math.min(100, value || 0));
  const radius = 100;
  const circumference = 2 * Math.PI * radius;
  const dash = (clamped / 100) * circumference;
  const tier = tierForScore(clamped);
  const stroke = colorForScore(clamped);

  return (
    <div className="score-circle">
      <svg width="220" height="220" viewBox="0 0 240 240">
        <circle cx="120" cy="120" r={radius} stroke="#e5e7eb" strokeWidth="16" fill="none" />
        <circle
          cx="120"
          cy="120"
          r={radius}
          stroke={stroke}
          strokeWidth="16"
          fill="none"
          strokeDasharray={`${dash} ${circumference - dash}`}
          strokeLinecap="round"
          transform="rotate(-90 120 120)"
        />
      </svg>
      <div style={{ position: 'absolute', textAlign: 'center' }}>
        <div className="score-number">{clamped}</div>
        <div className="score-label">{tier}</div>
      </div>
    </div>
  );
}

function ResultsDashboard({ results, onReset }) {

  return (
    <div className="results-dashboard">
      <h2>ATS Analysis Results</h2>
      {/* Score Card */}
      <div className="score-card">
        <Radial value={results.ats_score} />
        <div className="score-details">
          <div className="match-rate">
            Overall ATS Score categorized: <strong>{tierForScore(results.ats_score)}</strong>
          </div>
          <div className="score-breakdown">
            <div className="metric">
              <div className="label">Keywords</div>
              <div className="value">{results.keyword_match_rate}%</div>
            </div>
            <div className="metric">
              <div className="label">Sections</div>
              <div className="value">{
                [results.section_analysis.skills, results.section_analysis.experience, results.section_analysis.education]
                  .filter(Boolean).length
              }/3</div>
            </div>
            <div className="metric">
              <div className="label">Formatting</div>
              <div className="value">OK</div>
            </div>
          </div>
        </div>
      </div>

      {/* Section Analysis */}
      <div className="section-analysis">
        <h3>Resume Sections</h3>
        <div className="section-grid">
          <div className={`section-item ${results.section_analysis.skills ? 'present' : 'missing'}`}>
            <span className="icon">{results.section_analysis.skills ? '✓' : '✗'}</span>
            <span>Skills Section</span>
          </div>
          <div className={`section-item ${results.section_analysis.experience ? 'present' : 'missing'}`}>
            <span className="icon">{results.section_analysis.experience ? '✓' : '✗'}</span>
            <span>Experience Section</span>
          </div>
          <div className={`section-item ${results.section_analysis.education ? 'present' : 'missing'}`}>
            <span className="icon">{results.section_analysis.education ? '✓' : '✗'}</span>
            <span>Education Section</span>
          </div>
        </div>
      </div>

      {/* Keywords */}
      <div className="keywords-section">
        <div className="keyword-group matched">
          <h3>Matched Keywords ({results.matched_keywords.length})</h3>
          <div className="keyword-tags">
            {results.matched_keywords
              .filter(k => k && !/^(and|or|the|a|an|to|of|in|on|for|with|by|from|at|is|are|be|was|were|it|as)$/i.test(k) && !/^\d+$/.test(k))
              .map((keyword, index) => (
                <span key={index} className="keyword-tag matched-tag">{keyword}</span>
              ))}
          </div>
        </div>

        <div className="keyword-group missing">
          <h3>Missing Keywords ({results.missing_keywords.length})</h3>
          <div className="keyword-tags">
            {results.missing_keywords
              .filter(k => k && !/^(and|or|the|a|an|to|of|in|on|for|with|by|from|at|is|are|be|was|were|it|as)$/i.test(k) && !/^\d+$/.test(k))
              .map((keyword, index) => (
                <span key={index} className="keyword-tag missing-tag">{keyword}</span>
              ))}
          </div>
        </div>

        {results.skill_gaps && results.skill_gaps.length > 0 && (
          <div className="keyword-group skill-gaps">
            <h3>🎯 Skill Gaps</h3>
            <div className="keyword-tags">
              {results.skill_gaps.map((skill, index) => (
                <span key={index} className="keyword-tag skill-gap-tag">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Suggestions */}
      <div className="suggestions-section">
        <h3>Improvement Suggestions</h3>
        <ul className="suggestions-list">
          {results.suggestions.map((suggestion, index) => (
            <li key={index}>
              <div style={{ fontWeight: 600 }}>{suggestion}</div>
              <div className="small muted">Estimated score improvement: +2 to +5</div>
            </li>
          ))}
        </ul>
        <div className="actions">
          <button className="btn btn--primary" onClick={onReset}>Analyze Another Resume</button>
          <button className="btn" aria-label="Rewrite Resume for ATS">Rewrite Resume for ATS</button>
          <button className="btn" aria-label="Download ATS-Optimized Version">Download ATS-Optimized Version</button>
        </div>
      </div>
    </div>
  );
}

export default ResultsDashboard;
