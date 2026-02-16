# Contributing to CRUDREX

Thank you for your interest in contributing to CRUDREX! This document provides guidelines for contributing to both the Python and JavaScript versions.

## 🤝 How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Version of CRUDREX being used (Python or JavaScript)
- Operating system and runtime version
- Screenshots or error messages if applicable

### Suggesting Enhancements

Enhancement suggestions are welcome. Include:

- A clear and concise description of the suggested feature
- Example use cases for the feature
- Possible implementation approach (if you have ideas)
- How this feature would benefit users

## 🛠️ Development Setup

### Python Version

```bash
cd crudrex-py
pip install -e .
```

Run the development server:

```bash
python crudrex/cli/cli.py
```

### JavaScript Version

```bash
cd crudrex-js
npm install
npm run dev
```

Run the development server:

```bash
npm start
```

## 📋 Coding Standards

### Python Version

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and modular

### JavaScript Version

- Use ES6+ syntax
- Follow Airbnb JavaScript Style Guide
- Use meaningful variable and function names
- Add JSDoc comments for functions

## 🧪 Testing

Before submitting a pull request:

1. Test both versions if applicable
2. Ensure all existing functionality still works
3. Test on multiple operating systems if possible
4. Verify web interface renders correctly
5. Test all CRUD operations (GET, POST, PUT, PATCH, DELETE)

## 📝 Pull Request Process

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes following the coding standards
4. Test thoroughly
5. Commit your changes with descriptive messages
6. Push to your fork
7. Create a pull request with a clear description

## 🏗️ Project Structure

```
crudrex/
├── crudrex-py/          # Python version
│   ├── crudrex/         # Main package
│   ├── demo.py          # Demo script
│   └── README.md        # Python-specific docs
├── crudrex-js/          # JavaScript version
│   ├── src/             # Source code
│   ├── data/            # JSON data storage
│   └── README.md        # JavaScript-specific docs
├── CONTRIBUTING.md      # This file
├── LICENSE              # MIT License
└── README.md            # Main documentation
```

## 🌍 Language

The code and documentation should be primarily in English. However, if you're contributing to support multiple languages, ensure that:

- Comments in code are in English
- Documentation is in English
- UI text can be localized if needed

## ✨ Features to Add

We're always looking for new features! Some ideas:

- Authentication/Authorization support
- Data validation schemas
- Import/export functionality
- Real-time updates
- Advanced filtering and pagination
- API rate limiting
- Request logging and analytics

## 💡 Tips for Beginners

1. Start with small, manageable changes
2. Read the existing code to understand patterns
3. Ask questions in issues if you're unsure
4. Focus on one version first (Python or JavaScript)
5. Test your changes thoroughly before submitting

## 📄 License

By contributing to CRUDREX, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CRUDREX! Your help makes this project better for everyone. 🚀
