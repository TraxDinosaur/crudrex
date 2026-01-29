# CRUDREX - Mock JSON Server - Complete Documentation

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Project Structure](#project-structure)
6. [API Endpoints](#api-endpoints)
7. [Web Interface](#web-interface)
8. [CLI Usage](#cli-usage)
9. [Global Installation](#global-installation)
10. [Data Persistence](#data-persistence)
11. [Examples](#examples)
12. [Testing](#testing)
13. [Troubleshooting](#troubleshooting)
14. [Contributing](#contributing)
15. [License](#license)

## Overview

CRUDREX is a modern mock JSON server designed for testing HTTP requests and learning CRUD operations. It provides a simple yet powerful platform similar to services like mockapi.io and crudcrud.com, allowing developers to quickly create temporary APIs for testing purposes.

The server supports all standard HTTP methods (GET, POST, PUT, PATCH, DELETE) and automatically persists data in JSON files. With its beautiful web interface and comprehensive API, CRUDREX is perfect for frontend developers, API testers, and anyone learning about RESTful services.

## Features

- 🚀 **Create collections dynamically** on-the-fly
- 🔄 **Full CRUD operations** (GET, POST, PUT, PATCH, DELETE)
- 💾 **Automatic data persistence** in JSON files
- 🌐 **CORS enabled** for cross-origin requests
- 🖥️ **Beautiful web interface** with Hyde/Hyprland-inspired design
- ⌨️ **CLI interface** for easy server management
- 📱 **Responsive design** that works on all devices
- 🔍 **Query parameter filtering** for data retrieval
- 📁 **Organized project structure** for easy maintenance
- 🌍 **Cross-platform compatibility** (Windows, macOS, Linux)

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Required Dependencies

CRUDREX requires the following Python packages:

- Flask >= 2.0.0
- Flask-CORS >= 3.0.0

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

## Project Structure

```
crudrex/
├── cli/                    # Command line interface
│   ├── __init__.py
│   └── cli.py             # Main CLI entry point
├── api/                   # Core server implementation
│   ├── __init__.py
│   ├── server.py          # Flask server implementation
│   └── templates/         # Web interface templates
│       └── index.html     # Main UI template
├── __init__.py            # Package metadata
├── data/                  # Default data storage directory
├── requirements.txt       # Python dependencies
├── README.md              # Project overview
└── CRUDREX_FULL_DOCUMENTATION.md  # Complete documentation
```

## API Endpoints

### Collection Management

| Method | Endpoint        | Description             | Body Format          |
| ------ | --------------- | ----------------------- | -------------------- |
| GET    | `/collections/` | List all collections    | N/A                  |
| POST   | `/collections/` | Create a new collection | `{"name": "string"}` |

### Data Operations

| Method | Endpoint           | Description                 | Body Format     |
| ------ | ------------------ | --------------------------- | --------------- |
| GET    | `/:collection/`    | Get all items in collection | N/A             |
| POST   | `/:collection/`    | Create a new item           | Any JSON object |
| GET    | `/:collection/:id` | Get a specific item         | N/A             |
| PUT    | `/:collection/:id` | Update an item (full)       | Any JSON object |
| PATCH  | `/:collection/:id` | Update an item (partial)    | Any JSON object |
| DELETE | `/:collection/:id` | Delete an item              | N/A             |

### Query Parameters

You can filter results using query parameters:

```
GET /:collection/?field=value
```

Example:

```
GET /users/?name=John
GET /products/?category=Electronics&price=999.99
```

## Web Interface

CRUDREX features a modern, responsive web interface accessible at the root URL (`/`). The interface includes:

### Dashboard

- Collection management panel
- Create new collections form
- List of existing collections with endpoints
- API endpoint reference guide

### Collection View

- Data table showing all items in a collection
- Add new items form with JSON input
- Delete individual items
- View item details

### Design Features

- Hyde/Hyprland-inspired dark theme
- Responsive layout for all device sizes
- Smooth animations and transitions
- Monospace fonts for developer familiarity
- Color-coded HTTP method indicators

## CLI Usage

### Basic Usage

Start the server with default settings:

```bash
python crudrex/cli/cli.py
```

### Custom Options

```bash
python crudrex/cli/cli.py --port 3000 --data-dir ./my-data --host 0.0.0.0
```

### Command Line Arguments

| Argument     | Default     | Description                    |
| ------------ | ----------- | ------------------------------ |
| `--port`     | 8085        | Port to run the server on      |
| `--data-dir` | "./data"    | Directory for data persistence |
| `--host`     | "localhost" | Host to bind the server to     |
| `--help`     | N/A         | Show help message              |

## Global Installation

To use CRUDREX from anywhere on your system:

### Windows

1. Add the CRUDREX directory to your system PATH:
   - Press Win + R, type `sysdm.cpl`, press Enter
   - Go to Advanced tab → Environment Variables
   - Under System Variables, find and select "Path", click Edit
   - Click New and add the full path to your CRUDREX folder
   - Click OK to save

2. Create a batch file `crudrex.bat` in the CRUDREX directory:

   ```batch
   @echo off
   python "%~dp0crudrex\cli\cli.py" %*
   ```

3. Use CRUDREX from anywhere:
   ```cmd
   crudrex
   crudrex --port 3000
   ```

### Linux/macOS

1. Add the CRUDREX directory to your PATH by adding this line to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

   ```bash
   export PATH="$PATH:/path/to/crudrex"
   ```

2. Create a shell script `crudrex` in the CRUDREX directory:

   ```bash
   #!/bin/bash
   python3 "$(dirname "$0")/crudrex/cli/cli.py" "$@"
   ```

3. Make it executable:

   ```bash
   chmod +x crudrex
   ```

4. Use CRUDREX from anywhere:
   ```bash
   crudrex
   crudrex --port 3000
   ```

## Data Persistence

CRUDREX automatically saves data to JSON files in the specified data directory (default: `./data`).

### File Structure

```
data/
├── collection1.json
├── collection2.json
└── collection3.json
```

### Data Format

Each collection is stored as a JSON array of objects:

```json
[
  {
    "id": "unique-uuid-string",
    "field1": "value1",
    "field2": "value2"
  },
  {
    "id": "another-uuid-string",
    "field1": "value3",
    "field2": "value4"
  }
]
```

### ID Generation

CRUDREX automatically generates UUIDs for each item to ensure uniqueness:

- Format: `xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx`
- Generated when items are created via POST requests
- Used for identifying items in PUT, PATCH, and DELETE operations

## Examples

### Creating a Collection

Using cURL:

```bash
curl -X POST http://localhost:8085/collections/ \
  -H "Content-Type: application/json" \
  -d '{"name": "users"}'
```

### Adding Data

```bash
curl -X POST http://localhost:8085/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'
```

### Retrieving Data

Get all users:

```bash
curl http://localhost:8085/users/
```

Get a specific user:

```bash
curl http://localhost:8085/users/USER-ID-HERE
```

Filter users:

```bash
curl http://localhost:8085/users/?name=John
```

### Updating Data

Full update:

```bash
curl -X PUT http://localhost:8085/users/USER-ID-HERE \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com", "age": 25}'
```

Partial update:

```bash
curl -X PATCH http://localhost:8085/users/USER-ID-HERE \
  -H "Content-Type: application/json" \
  -d '{"age": 26}'
```

### Deleting Data

```bash
curl -X DELETE http://localhost:8085/users/USER-ID-HERE
```

## Testing

CRUDREX includes a comprehensive test suite to verify functionality:

### Running Tests

```bash
python test_crudrex.py
```

### Test Coverage

The test suite verifies:

- Server startup and accessibility
- Collection creation and management
- Full CRUD operations
- Data persistence
- Query parameter filtering
- Error handling
- Response codes and formats

### Demo Script

A demo script is included to showcase CRUDREX features:

```bash
python demo.py
```

This script demonstrates:

- Starting the server programmatically
- Creating collections via API
- Adding and manipulating data
- Filtering and retrieving data
- Web interface integration

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Solution: Use a different port with `--port` option
   - Example: `python crudrex/cli/cli.py --port 3001`

2. **Permission denied when writing data files**
   - Solution: Ensure the data directory is writable
   - Example: `python crudrex/cli/cli.py --data-dir ./writable-directory`

3. **Dependencies not found**
   - Solution: Install required packages
   - Example: `pip install flask flask-cors`

4. **Server not accessible from other devices**
   - Solution: Bind to all interfaces
   - Example: `python crudrex/cli/cli.py --host 0.0.0.0`

### Logging

CRUDREX provides access logs for monitoring requests:

```
127.0.0.1 - - [29/Jan/2026 12:03:36] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [29/Jan/2026 12:03:38] "POST /collections/ HTTP/1.1" 201 -
```

Logs include:

- Client IP address
- Timestamp
- HTTP method and endpoint
- Response status code

## Contributing

We welcome contributions to CRUDREX! Here's how you can help:

### Reporting Issues

1. Check if the issue already exists
2. Provide detailed reproduction steps
3. Include environment information (OS, Python version)
4. Add any relevant error messages or logs

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

### Development Guidelines

- Follow PEP 8 coding standards
- Write clear, descriptive commit messages
- Include docstrings for functions and classes
- Test your changes thoroughly
- Keep dependencies minimal

## License

MIT License

Copyright (c) 2026 TraxDinosaur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
