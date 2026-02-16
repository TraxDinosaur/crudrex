# CRUDREX-JS - Mock JSON Server

A modern mock JSON server for testing HTTP requests and learning CRUD operations - **JavaScript/Node.js version**.

This is a complete JavaScript port of the original [Python CRUDREX](https://github.com/TraxDinosaur/crudrex) server, designed for JavaScript developers who want to use the same powerful mock API server functionality.

## Features

- 🚀 **Create collections dynamically** on-the-fly
- 🔄 **Full CRUD operations** (GET, POST, PUT, PATCH, DELETE)
- 💾 **Automatic data persistence** in JSON files
- 🌐 **CORS enabled** for cross-origin requests
- 🖥️ **Beautiful web interface** with Hyde/Hyprland-inspired design
- ⌨️ **CLI interface** for easy server management
- 📱 **Responsive design** that works on all devices
- 🟢 **Node.js native** - No Python required!

## Installation

### Prerequisites

- Node.js 14.0.0 or higher
- npm or yarn

### Install Dependencies

```bash
cd crudrex-js
npm install
```

## Quick Start

1. Clone or download this repository:

   ```bash
   git clone https://github.com/TraxDinosaur/crudrex
   cd crudrex-js
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the server:

   ```bash
   npm start
   ```

4. Visit `http://localhost:8085` in your browser to access the web interface.

## Global Installation

To use CRUDREX-JS from anywhere on your system:

### Option 1: Using npm link

```bash
npm link
```

Now you can run `crudrex` from anywhere:

```bash
crudrex
crudrex --port 3000
crudrex --data-dir ./my-data
```

### Option 2: Direct execution

```bash
node src/cli.js
```

## Usage

### Starting the Server

Start the server with default settings:

```bash
npm start
# or
node src/cli.js
```

Customize the port and data directory:

```bash
node src/cli.js --port 3000 --data-dir ./my-data
```

### CLI Options

| Option | Alias | Default | Description |
|--------|-------|---------|-------------|
| `--port` | `-p` | 8085 | Port to run the server on |
| `--data-dir` | `-d` | data | Directory to store data files |
| `--host` | `-H` | localhost | Host to run the server on |
| `--no-browser` | - | false | Don't open browser automatically |
| `--silent` | `-s` | false | Run in silent mode |
| `--version` | `-v` | - | Show version number |
| `--help` | `-h` | - | Show help |

### Creating Collections

#### Via Web Interface

1. Visit `http://localhost:8085`
2. Enter a collection name in the "Create New Collection" form
3. Click "Create Collection"

#### Via API

```bash
curl -X POST http://localhost:8085/collections/ \
  -H "Content-Type: application/json" \
  -d '{"name": "users"}'
```

### Working with Data

Once you have a collection, you can perform CRUD operations:

#### Create (POST)

```bash
curl -X POST http://localhost:8085/users/ \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
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
curl -X PUT http://localhost:8085/users/{item-id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Doe", "email": "jane@example.com"}'
```

#### Partial Update (PATCH)

```bash
curl -X PATCH http://localhost:8085/users/{item-id} \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Smith"}'
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

## Project Structure

```
crudrex-js/
├── package.json       # Project configuration and dependencies
├── README.md          # Documentation
└── src/
    ├── cli.js         # Command line interface
    ├── server.js      # Core server implementation
    └── templates/
        └── index.html # Web interface template
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

## Comparison with Python Version

| Feature | Python Version | JavaScript Version |
|---------|---------------|-------------------|
| Runtime | Python 3.7+ | Node.js 14+ |
| Framework | Flask | Express |
| CORS | Flask-CORS | cors middleware |
| CLI | argparse | commander |
| Data Persistence | JSON files | JSON files (identical) |
| Web Interface | Jinja2 template | Static HTML (identical) |
| API Endpoints | Same | Same |
| Design | Hyde/Hyprland | Hyde/Hyprland (identical) |

## Use Cases

- **Frontend Development**: Mock API for testing UI components
- **API Learning**: Learn CRUD operations and REST API concepts
- **Prototyping**: Quickly create mock backends for prototypes
- **Testing**: Test HTTP requests without setting up a real backend
- **Education**: Teaching web development and API concepts

## Examples

### Using with Fetch API

```javascript
// Create a collection
await fetch('http://localhost:8085/collections/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'products' })
});

// Add items
await fetch('http://localhost:8085/products/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Laptop', price: 999 })
});

// Get all items
const response = await fetch('http://localhost:8085/products/');
const products = await response.json();
console.log(products);
```

### Using with Axios

```javascript
const axios = require('axios');
const API = 'http://localhost:8085';

// Create and populate a collection
await axios.post(`${API}/collections/`, { name: 'todos' });
await axios.post(`${API}/todos/`, { title: 'Learn Node.js', completed: false });

// Get all todos
const { data } = await axios.get(`${API}/todos/`);
console.log(data);
```

## Requirements

- Node.js 14.0.0+
- Express >= 4.18.0
- CORS >= 2.8.5

## Author

**Original Python Version**: TraxDinosaur
- GitHub: [@TraxDinosaur](https://github.com/TraxDinosaur)
- Email: acciotraxdinosaur@duck.com

**JavaScript Port**: Community Contribution

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Original [CRUDREX](https://github.com/TraxDinosaur/crudrex) Python project
- Inspired by [mockapi.io](https://mockapi.io) and [crudcrud.com](https://crudcrud.com)
