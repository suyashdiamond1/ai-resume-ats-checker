# Contributing to AI Resume ATS Checker

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, Node version)

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend tests
   cd frontend
   npm test
   ```

5. **Commit your changes**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
   
   Use conventional commit format:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation
   - `style:` for formatting
   - `refactor:` for code restructuring
   - `test:` for adding tests
   - `chore:` for maintenance

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Describe your changes
   - Link related issues
   - Add screenshots for UI changes

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Maximum line length: 100 characters

```python
def analyze_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Analyze resume against job description.
    
    Args:
        resume_text: The resume content
        job_description: The job posting content
        
    Returns:
        Dictionary with analysis results
    """
    pass
```

### JavaScript/React (Frontend)
- Use functional components with hooks
- Use meaningful variable names
- Add JSDoc comments for complex functions
- Use Prettier for formatting

```javascript
/**
 * Analyze resume and display results
 * @param {File} resumeFile - The resume file to analyze
 * @param {string} jobDescription - Job description text
 */
function analyzeResume(resumeFile, jobDescription) {
  // Implementation
}
```

## Testing

### Backend
- Write unit tests with pytest
- Aim for >80% code coverage
- Test edge cases and error handling

### Frontend
- Write component tests
- Test user interactions
- Test API integration

## Documentation

- Update README.md for major features
- Add docstrings/comments for complex logic
- Update API documentation if endpoints change
- Keep QUICKSTART.md current

## Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, your PR will be merged
4. Your contribution will be credited in the project

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the code, not the person

## Questions?

Feel free to open an issue with the "question" label or reach out to the maintainers.

Thank you for contributing! 🎉
