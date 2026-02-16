# CRUDREX - Mock JSON Server

A modern mock JSON server for testing HTTP requests and learning CRUD operations - **Available in Python and JavaScript!**

> CRUDREX helps you quickly set up a mock REST API server for testing your applications, learning CRUD operations, or prototyping without needing a real backend.

## 🚀 Quick Start - Choose Your Version

### 🐍 Python Version (Original)

[![PyPI](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://pypi.org/project/crudrex)

```bash
cd crudrex-py
pip install -e .
crudrex
```

#### Installation

```bash
cd crudrex-py
pip install -r requirements.txt
```

#### Run Server

```bash
python crudrex/cli/cli.py
# or
crudrex
```

### 💻 JavaScript/Node.js Version

[![Node.js](https://img.shields.io/badge/Node.js-14+-green.svg)](https://nodejs.org)

```bash
cd crudrex-js
npm install
npm start
```

#### Installation

```bash
cd crudrex-js
npm install
```

#### Run Server

```bash
npm start
# or
node src/cli.js
```

## ✨ Features (Both Versions)

- 🚀 **Create collections dynamically** on-the-fly
- 🔄 **Full CRUD operations** (GET, POST, PUT, PATCH, DELETE)
- 💾 **Automatic data persistence** in JSON files
- 🌐 **CORS enabled** for cross-origin requests
- 🖥️ **Beautiful web interface** with modern design
- ⌨️ **CLI interface** for easy server management
- 📱 **Responsive design** that works on all devices

## 📚 Documentation

- **Python Version**: See [`crudrex-py/README.md`](crudrex-py/README.md) for detailed documentation
- **JavaScript Version**: See [`crudrex-js/README.md`](crudrex-js/README.md) for detailed documentation

## 🗂️ Project Structure

```
crudrex/
├── crudrex-py/          # Python version (Flask)
│   ├── crudrex/         # Main package
│   │   ├── api/         # API server
│   │   └── cli/         # CLI interface
│   ├── demo.py          # Demo script
│   ├── README.md        # Python docs
│   └── pyproject.toml   # Python config
│
├── crudrex-js/          # JavaScript version (Node.js)
│   ├── src/             # Source code
│   │   ├── cli.js       # CLI interface
│   │   └── server.js    # API server
│   ├── data/            # JSON data storage
│   ├── README.md        # JavaScript docs
│   └── package.json     # Node.js config
│
├── LICENSE              # MIT License
└── README.md            # This file
```

## 🤔 Which Version Should I Use?

| Feature      | Python Version           | JavaScript Version            |
| ------------ | ------------------------ | ----------------------------- |
| Best For     | Python developers        | Node.js/JavaScript developers |
| Framework    | Flask                    | Express.js                    |
| Dependencies | Lightweight              | npm ecosystem                 |
| Performance  | Fast for Python apps     | Better for JavaScript apps    |
| Learning     | Understanding Python web | Understanding Node.js web     |

## 🔧 Configuration

Both versions support custom configuration:

- **Port**: Default 3000
- **Data Directory**: Auto-created for JSON storage
- **CORS**: Enabled by default

## 📝 Usage Examples

### Create a Collection

```bash
# POST request to create a new collection
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Read Data

```bash
# GET all users
curl http://localhost:3000/api/users

# GET specific user
curl http://localhost:3000/api/users/1
```

### Update Data

```bash
# PUT (replace)
curl -X PUT http://localhost:3000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'

# PATCH (partial update)
curl -X PATCH http://localhost:3000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"email": "jane.new@example.com"}'
```

### Delete Data

```bash
curl -X DELETE http://localhost:3000/api/users/1
```

## 🌐 Web Interface

Both versions come with a beautiful web interface available at:

```
http://localhost:3000
```

The interface allows you to:

- View all collections and their data
- Add, edit, and delete records
- Test API endpoints interactively
- Monitor request/response logs

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

**Python Version:**

```bash
cd crudrex-py
pip install -e .
```

**JavaScript Version:**

```bash
cd crudrex-js
npm install
npm run dev
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**TraxDinosaur**

- GitHub: [@TraxDinosaur](https://github.com/TraxDinosaur)
- Original Python Version & JavaScript Port

## 🙏 Acknowledgments

- Inspired by [mockapi.io](https://mockapi.io) and [crudcrud.com](https://crudcrud.com)
- Web interface design inspired by Hyde/Hyprland aesthetics

---

**Note**: Both versions (Python and JavaScript) offer identical functionality from a user's perspective. Choose the one that best fits your development environment and preferences.
