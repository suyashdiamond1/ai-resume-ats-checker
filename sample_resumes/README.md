# Sample Files for Testing

This directory contains sample resume and job description files for testing the AI Resume ATS Checker.

## Files

- `sample_resume.txt` - Sample software engineer resume
- `sample_job_description.txt` - Sample job posting for a full-stack developer

## Usage

1. Start the application (backend and frontend)
2. Upload `sample_resume.txt` as the resume
3. Copy and paste the content from `sample_job_description.txt` into the job description field
4. Click "Analyze Resume" to see the ATS analysis

## Creating Your Own Test Files

You can add your own resume and job description files to this directory for testing:

- Supported formats: PDF, DOCX, TXT
- Include complete resume information (skills, experience, education)
- Use real job descriptions from job boards for accurate testing

## Expected Results

When testing with the provided samples, you should see:
- High ATS score (75-85 range) due to good keyword overlap
- Matched keywords: python, javascript, react, aws, docker, etc.
- Some missing keywords based on the job requirements
- Suggestions for improvement
