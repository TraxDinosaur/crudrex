# CRUDREX - Mock JSON Server

A modern mock JSON server for testing HTTP requests and learning CRUD operations, similar to mockapi.io or crudcrud.com.

## Features

- 🚀 **Create collections dynamically** on-the-fly
- 🔄 **Full CRUD operations** (GET, POST, PUT, PATCH, DELETE)
- 💾 **Automatic data persistence** in JSON files
- 🌐 **CORS enabled** for cross-origin requests
- 🖥️ **Beautiful web interface** with Hyde/Hyprland-inspired design
- ⌨️ **CLI interface** for easy server management
- 📱 **Responsive design** that works on all devices

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Required Dependencies

Install dependencies using pip:

```bash
pip install flask flask-cors
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

## Quick Start

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd crudrex
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the server:

   ```bash
   python crudrex/cli/cli.py
   ```

4. Visit `http://localhost:8085` in your browser to access the web interface.

## Global Installation

To use CRUDREX from anywhere on your system:

1. Add the CRUDREX directory to your system PATH:
   - **Windows**: Add the full path to the crudrex folder to your PATH environment variable
   - **Linux/macOS**: Add `export PATH="$PATH:/path/to/crudrex"` to your shell profile (~/.bashrc, ~/.zshrc, etc.)

2. Create a script file in the CRUDREX directory according to your system:
   - **Windows**: Create `crudrex.bat` with content: `@echo off` and `python "YOUR_PATH\crudrex\cli\cli.py" %*`
   - **Linux/macOS**: Create `crudrex` shell script with content: `#!/bin/bash` and `python3 "$(dirname "$0")/crudrex/cli/cli.py" "$@"`

3. Make the script executable (Linux/macOS only):

   ```bash
   chmod +x crudrex
   ```

4. Use CRUDREX from anywhere:
   ```bash
   crudrex
   crudrex --port 3000
   ```

## Usage

### Starting the Server

Start the server with default settings:

```bash
python crudrex/cli/cli.py
```

Customize the port and data directory:

```bash
python crudrex/cli/cli.py --port 3000 --data-dir ./my-data
```

### Creating Collections

#### Via Web Interface

1. Visit `http://localhost:8085`
2. Enter a collection name in the "Create New Collection" form
3. Click "Create Collection"

#### Via API

```bash
curl -X POST http://localhost:8085/collections/ -H "Content-Type: application/json" -d '{"name": "users"}'
```

### Working with Data

Once you have a collection, you can perform CRUD operations:

#### Create (POST)

```bash
curl -X POST http://localhost:8085/users/ -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}'
```

#### Read (GET)

```bash
# Get all items
curl http://localhost:8085/users/

# Get a specific item
curl http://localhost:8085/users/{item-id}

# Filter items
curl http://localhost:8085/users/?name=John
```

#### Update (PUT)

```bash
curl -X PUT http://localhost:8085/users/{item-id} -H "Content-Type: application/json" -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

#### Partial Update (PATCH)

```bash
curl -X PATCH http://localhost:8085/users/{item-id} -H "Content-Type: application/json" -d '{"name": "Jane Smith"}'
```

#### Delete (DELETE)

```bash
curl -X DELETE http://localhost:8085/users/{item-id}
```

## Web Interface

Visit `http://localhost:8085/` in your browser to access the modern web interface featuring:

- Collection management dashboard
- Real-time data visualization
- JSON data preview
- API endpoint reference
- Responsive design for all devices

## Data Storage

Data is automatically persisted in JSON files in the data directory (default: `./data`).

Each collection is stored in a separate JSON file named `{collection-name}.json`.

## Requirements

- Python 3.7+
- Flask >= 2.0.0
- Flask-CORS >= 3.0.0

## Project Structure

```
crudrex/
├── cli/           # Command line interface
├── api/           # Core server implementation
│   └── templates/ # Web interface templates
└── data/          # Data storage directory
```

## API Endpoints

| Method | Endpoint           | Description                 |
| ------ | ------------------ | --------------------------- |
| GET    | `/collections/`    | List all collections        |
| POST   | `/collections/`    | Create a new collection     |
| GET    | `/:collection/`    | Get all items in collection |
| POST   | `/:collection/`    | Create a new item           |
| GET    | `/:collection/:id` | Get a specific item         |
| PUT    | `/:collection/:id` | Update an item (full)       |
| PATCH  | `/:collection/:id` | Update an item (partial)    |
| DELETE | `/:collection/:id` | Delete an item              |

## Author

**TraxDinosaur**

- GitHub: [@TraxDinosaur](https://github.com/TraxDinosaur)
- Email: acciotraxdinosaur@duck.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

For complete documentation, see [DOCUMENTATION.md](DOCUMENTATION.md).
