# Contributing to DocGenius

Thank you for considering contributing to DocGenius! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, Ollama version)
- Screenshots if applicable

### Suggesting Enhancements

We welcome feature requests! Please create an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Any examples or mockups

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**:
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed
3. **Test your changes**:
   - Ensure the app runs without errors
   - Test with different document types
   - Verify no existing functionality is broken
4. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference any related issues
5. **Push to your fork** and submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/DocGenius.git
cd DocGenius

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama models
ollama pull nomic-embed-text
ollama pull gemma3:1b

# Run the app
streamlit run app.py
```

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features (e.g., support for more file types)
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🧪 Testing improvements

## Questions?

Feel free to open an issue for any questions about contributing!

---

**Thank you for making DocGenius better! 🙏**
