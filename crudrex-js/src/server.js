/**
 * CRUDREX - Mock JSON Server (JavaScript/Node.js Version)
 * A modern mock JSON server for testing HTTP requests and learning CRUD operations
 *
 * @author TraxDinosaur (JavaScript Port)
 * @version 0.1.2
 */

const express = require("express");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const { v4: uuidv4 } = require("crypto");

class MockServer {
  /**
   * Create a new MockServer instance
   * @param {Object} options - Server configuration options
   * @param {string} options.dataDir - Directory to store data files (default: 'data')
   * @param {number} options.port - Port to run the server on (default: 8085)
   */
  constructor(options = {}) {
    this.dataDir = options.dataDir || "data";
    this.port = options.port || 8085;
    this.collections = {};

    // Initialize Express app
    this.app = express();

    // Setup middleware
    this.setupMiddleware();

    // Setup directories
    this.setupDirectories();

    // Load existing collections
    this.loadCollections();

    // Setup routes
    this.setupRoutes();
  }

  /**
   * Setup Express middleware
   */
  setupMiddleware() {
    // Enable CORS for all origins
    this.app.use(
      cors({
        origin: "*",
        methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allowedHeaders: ["Content-Type", "Authorization"],
      }),
    );

    // Parse JSON bodies
    this.app.use(express.json());

    // Parse URL-encoded bodies
    this.app.use(express.urlencoded({ extended: true }));

    // Request logging middleware
    this.app.use((req, res, next) => {
      const timestamp = new Date().toISOString();
      const methodColors = {
        GET: "\x1b[32m",
        POST: "\x1b[33m",
        PUT: "\x1b[34m",
        PATCH: "\x1b[35m",
        DELETE: "\x1b[31m",
        OPTIONS: "\x1b[36m",
      };
      const statusColors = {
        2: "\x1b[32m",
        3: "\x1b[36m",
        4: "\x1b[33m",
        5: "\x1b[31m",
      };
      const methodColor = methodColors[req.method] || "\x1b[0m";
      const reset = "\x1b[0m";
      const dim = "\x1b[2m";
      const bright = "\x1b[1m";

      const originalEnd = res.end;
      res.end = function (...args) {
        const statusColor =
          statusColors[Math.floor(res.statusCode / 100)] || reset;
        console.log(
          `${dim}${timestamp}${reset} ${methodColor}${bright}${req.method}${reset} ${req.path} ${statusColor}${res.statusCode}${reset}`,
        );
        originalEnd.apply(res, args);
      };

      next();
    });

    // Handle OPTIONS requests for CORS preflight
    this.app.use((req, res, next) => {
      if (req.method === "OPTIONS") {
        return res.status(200).end();
      }
      next();
    });
  }

  /**
   * Create necessary directories
   */
  setupDirectories() {
    if (!fs.existsSync(this.dataDir)) {
      fs.mkdirSync(this.dataDir, { recursive: true });
    }
  }

  /**
   * Load existing collections from data directory
   */
  loadCollections() {
    if (fs.existsSync(this.dataDir)) {
      const files = fs.readdirSync(this.dataDir);
      for (const filename of files) {
        if (filename.endsWith(".json")) {
          const collectionName = filename.slice(0, -5); // Remove .json extension
          this.collections[collectionName] =
            this.loadCollectionData(collectionName);
        }
      }
    }
  }

  /**
   * Load data for a specific collection
   * @param {string} collectionName - Name of the collection
   * @returns {Object} Collection data
   */
  loadCollectionData(collectionName) {
    const filepath = path.join(this.dataDir, `${collectionName}.json`);
    if (fs.existsSync(filepath)) {
      try {
        const data = fs.readFileSync(filepath, "utf8");
        return JSON.parse(data);
      } catch (error) {
        console.error(
          `Error loading collection ${collectionName}:`,
          error.message,
        );
        return {};
      }
    }
    return {};
  }

  /**
   * Save all collections to their respective files
   */
  saveAllCollections() {
    for (const collectionName in this.collections) {
      this.saveCollectionData(collectionName);
    }
  }

  /**
   * Save data for a specific collection
   * @param {string} collectionName - Name of the collection
   */
  saveCollectionData(collectionName) {
    const filepath = path.join(this.dataDir, `${collectionName}.json`);
    try {
      fs.writeFileSync(
        filepath,
        JSON.stringify(this.collections[collectionName], null, 2),
      );
    } catch (error) {
      console.error(
        `Error saving collection ${collectionName}:`,
        error.message,
      );
    }
  }

  /**
   * Get current timestamp in ISO format
   * @returns {string} ISO timestamp
   */
  getCurrentTimestamp() {
    return new Date().toISOString();
  }

  /**
   * Generate a unique ID
   * @returns {string} UUID
   */
  generateId() {
    return require("crypto").randomUUID();
  }

  /**
   * Setup all routes for the server
   */
  setupRoutes() {
    // Main page route - serve the HTML template
    this.app.get("/", (req, res) => {
      const templatePath = path.join(__dirname, "templates", "index.html");
      if (fs.existsSync(templatePath)) {
        res.sendFile(templatePath);
      } else {
        res.send(this.getDefaultHTML());
      }
    });

    // API info route
    this.app.get("/api/info", (req, res) => {
      res.json({
        message: "Mock JSON Server is running",
        collections: Object.keys(this.collections),
        instructions: "Create a new collection by POSTing to /collections/",
        port: this.port,
      });
    });

    // Collection management routes
    this.app
      .route("/collections/")
      .get((req, res) => {
        res.json({ collections: Object.keys(this.collections) });
      })
      .post((req, res) => {
        const data = req.body;
        if (!data || !data.name) {
          return res.status(400).json({ error: "Collection name is required" });
        }

        const collectionName = data.name;
        if (this.collections[collectionName]) {
          return res.status(400).json({ error: "Collection already exists" });
        }

        this.collections[collectionName] = {};
        this.saveCollectionData(collectionName);
        res
          .status(201)
          .json({ message: `Collection '${collectionName}' created` });
      });

    // Dynamic collection routes - items list
    this.app
      .route("/:collectionName/")
      .get((req, res) => {
        const { collectionName } = req.params;

        if (!this.collections[collectionName]) {
          return res.status(404).json({ error: "Collection not found" });
        }

        // Support query parameters for filtering
        let items = Object.values(this.collections[collectionName]);

        // Apply filters from query parameters
        for (const [filterKey, filterValue] of Object.entries(req.query)) {
          items = items.filter((item) => {
            return (
              item[filterKey] !== undefined &&
              String(item[filterKey]) === filterValue
            );
          });
        }

        res.json(items);
      })
      .post((req, res) => {
        const { collectionName } = req.params;
        const data = req.body;

        if (!data) {
          return res.status(400).json({ error: "JSON data required" });
        }

        // Auto-create collection if it doesn't exist
        if (!this.collections[collectionName]) {
          this.collections[collectionName] = {};
        }

        // Generate ID if not provided
        if (!data.id) {
          data.id = this.generateId();
        }

        // Store with ID as key
        this.collections[collectionName][data.id] = data;
        this.saveCollectionData(collectionName);
        res.status(201).json(data);
      });

    // Dynamic collection routes - individual items
    this.app
      .route("/:collectionName/:itemId")
      .get((req, res) => {
        const { collectionName, itemId } = req.params;

        if (!this.collections[collectionName]) {
          return res.status(404).json({ error: "Collection not found" });
        }

        if (!this.collections[collectionName][itemId]) {
          return res.status(404).json({ error: "Item not found" });
        }

        res.json(this.collections[collectionName][itemId]);
      })
      .post((req, res) => {
        const { collectionName, itemId } = req.params;
        const data = req.body;

        if (!data) {
          return res.status(400).json({ error: "JSON data required" });
        }

        // Auto-create collection if it doesn't exist
        if (!this.collections[collectionName]) {
          this.collections[collectionName] = {};
        }

        data.id = itemId;
        this.collections[collectionName][itemId] = data;
        this.saveCollectionData(collectionName);
        res.status(201).json(data);
      })
      .put((req, res) => {
        const { collectionName, itemId } = req.params;
        const data = req.body;

        if (!this.collections[collectionName]) {
          return res.status(404).json({ error: "Collection not found" });
        }

        if (!data) {
          return res.status(400).json({ error: "JSON data required" });
        }

        // Update the item
        data.id = itemId; // Ensure ID consistency
        this.collections[collectionName][itemId] = data;
        this.saveCollectionData(collectionName);
        res.json(data);
      })
      .patch((req, res) => {
        const { collectionName, itemId } = req.params;
        const data = req.body;

        if (!this.collections[collectionName]) {
          return res.status(404).json({ error: "Collection not found" });
        }

        if (!this.collections[collectionName][itemId]) {
          return res.status(404).json({ error: "Item not found" });
        }

        if (!data) {
          return res.status(400).json({ error: "JSON data required" });
        }

        // Partially update the item
        for (const [key, value] of Object.entries(data)) {
          this.collections[collectionName][itemId][key] = value;
        }

        this.saveCollectionData(collectionName);
        res.json(this.collections[collectionName][itemId]);
      })
      .delete((req, res) => {
        const { collectionName, itemId } = req.params;

        if (!this.collections[collectionName]) {
          return res.status(404).json({ error: "Collection not found" });
        }

        if (!this.collections[collectionName][itemId]) {
          return res.status(404).json({ error: "Item not found" });
        }

        const deletedItem = this.collections[collectionName][itemId];
        delete this.collections[collectionName][itemId];
        this.saveCollectionData(collectionName);
        res.json({ message: "Item deleted", deleted_item: deletedItem });
      });

    // Catch-all route for nested paths (json-server style)
    this.app.all("/*", (req, res) => {
      const pathParts = req.path.split("/").filter((part) => part);

      if (pathParts.length === 0) {
        return res.status(400).json({ error: "Invalid path" });
      }

      const rootCollection = pathParts[0];

      // Ensure root collection exists
      if (!this.collections[rootCollection]) {
        this.collections[rootCollection] = {};
      }

      const current_time = this.getCurrentTimestamp();

      // Determine if this is an item-level operation
      const isItemOperation =
        pathParts.length >= 2 &&
        (/^\d+$/.test(pathParts[pathParts.length - 1]) ||
          (pathParts[pathParts.length - 1].length >= 8 &&
            pathParts[pathParts.length - 1].includes("-")));

      if (isItemOperation) {
        // Handle item-level operations
        const endpointKey = pathParts.slice(0, -1).join("-");
        const itemId = pathParts[pathParts.length - 1];

        switch (req.method) {
          case "GET":
            if (this.collections[rootCollection][endpointKey]) {
              const items =
                this.collections[rootCollection][endpointKey].items || [];
              const item = items.find((i) => String(i.id) === String(itemId));
              if (item) {
                return res.json(item);
              }
            }
            return res.status(404).json({ error: "Item not found" });

          case "PUT":
            const putData = req.body;
            if (!putData) {
              return res.status(400).json({ error: "JSON data required" });
            }

            if (!this.collections[rootCollection][endpointKey]) {
              return res.status(404).json({ error: "Endpoint not found" });
            }

            // Find and update the item
            const items =
              this.collections[rootCollection][endpointKey].items || [];
            const itemIndex = items.findIndex(
              (i) => String(i.id) === String(itemId),
            );

            if (itemIndex !== -1) {
              const updatedItem = {
                id: itemId,
                createdAt: items[itemIndex].createdAt || current_time,
                updatedAt: current_time,
                data: putData.data || putData,
              };
              this.collections[rootCollection][endpointKey].items[itemIndex] =
                updatedItem;
              this.saveAllCollections();
              return res.json(updatedItem);
            }

            // If item not found, create new one
            const newItem = {
              id: itemId,
              createdAt: current_time,
              updatedAt: current_time,
              data: putData.data || putData,
            };
            this.collections[rootCollection][endpointKey].items.push(newItem);
            this.saveAllCollections();
            return res.status(201).json(newItem);

          case "PATCH":
            const patchData = req.body;
            if (!patchData) {
              return res.status(400).json({ error: "JSON data required" });
            }

            if (!this.collections[rootCollection][endpointKey]) {
              return res.status(404).json({ error: "Endpoint not found" });
            }

            const patchItems =
              this.collections[rootCollection][endpointKey].items || [];
            const patchItemIndex = patchItems.findIndex(
              (i) => String(i.id) === String(itemId),
            );

            if (patchItemIndex !== -1) {
              patchItems[patchItemIndex].updatedAt = current_time;
              if (patchData.data) {
                const itemData = patchItems[patchItemIndex].data || {};
                Object.assign(itemData, patchData.data);
                patchItems[patchItemIndex].data = itemData;
              } else {
                Object.assign(patchItems[patchItemIndex], patchData);
              }
              this.saveAllCollections();
              return res.json(patchItems[patchItemIndex]);
            }

            return res.status(404).json({ error: "Item not found" });

          case "DELETE":
            if (!this.collections[rootCollection][endpointKey]) {
              return res.status(404).json({ error: "Endpoint not found" });
            }

            const deleteItems =
              this.collections[rootCollection][endpointKey].items || [];
            const deleteIndex = deleteItems.findIndex(
              (i) => String(i.id) === String(itemId),
            );

            if (deleteIndex !== -1) {
              const deletedItem = deleteItems.splice(deleteIndex, 1)[0];
              this.saveAllCollections();
              return res.json({
                message: "Item deleted",
                deleted_item: deletedItem,
              });
            }

            return res.status(404).json({ error: "Item not found" });

          default:
            return res.status(405).json({ error: "Method not allowed" });
        }
      } else {
        // Handle endpoint-level operations
        const storageKey = pathParts.join("-");

        switch (req.method) {
          case "GET":
            if (this.collections[rootCollection][storageKey]) {
              return res.json(this.collections[rootCollection][storageKey]);
            }
            return res.json({ items: [] });

          case "POST":
            const postData = req.body;
            if (!postData) {
              return res.status(400).json({ error: "JSON data required" });
            }

            // Ensure the endpoint structure exists
            if (!this.collections[rootCollection][storageKey]) {
              this.collections[rootCollection][storageKey] = { items: [] };
            } else if (!this.collections[rootCollection][storageKey].items) {
              this.collections[rootCollection][storageKey] = { items: [] };
            }

            // Handle both object and array payloads
            if (Array.isArray(postData)) {
              const results = postData.map((item) => {
                const itemId = item.id || this.generateId();
                const structuredItem = {
                  id: itemId,
                  createdAt: current_time,
                  updatedAt: current_time,
                  data: { ...item },
                };
                delete structuredItem.data.id;
                this.collections[rootCollection][storageKey].items.push(
                  structuredItem,
                );
                return structuredItem;
              });
              this.saveAllCollections();
              return res.status(201).json({ items: results });
            } else {
              const itemId = postData.id || this.generateId();
              const structuredItem = {
                id: itemId,
                createdAt: current_time,
                updatedAt: current_time,
                data: { ...postData },
              };
              delete structuredItem.data.id;
              this.collections[rootCollection][storageKey].items.push(
                structuredItem,
              );
              this.saveAllCollections();
              return res.status(201).json(structuredItem);
            }

          case "PUT":
            const putDataAll = req.body;
            if (!putDataAll) {
              return res.status(400).json({ error: "JSON data required" });
            }
            this.collections[rootCollection][storageKey] = putDataAll;
            this.saveAllCollections();
            return res.json(putDataAll);

          case "PATCH":
            const patchDataAll = req.body;
            if (!patchDataAll) {
              return res.status(400).json({ error: "JSON data required" });
            }

            if (!this.collections[rootCollection][storageKey]) {
              this.collections[rootCollection][storageKey] = { items: [] };
            } else if (!this.collections[rootCollection][storageKey].items) {
              this.collections[rootCollection][storageKey] = { items: [] };
            }

            if (patchDataAll.items) {
              for (const updatedItem of patchDataAll.items) {
                const itemId = updatedItem.id;
                if (itemId) {
                  const existingIndex = this.collections[rootCollection][
                    storageKey
                  ].items.findIndex((i) => i.id === itemId);

                  if (existingIndex !== -1) {
                    updatedItem.updatedAt = current_time;
                    this.collections[rootCollection][storageKey].items[
                      existingIndex
                    ] = updatedItem;
                  } else {
                    updatedItem.createdAt =
                      updatedItem.createdAt || current_time;
                    updatedItem.updatedAt = current_time;
                    this.collections[rootCollection][storageKey].items.push(
                      updatedItem,
                    );
                  }
                }
              }
            }

            this.saveAllCollections();
            return res.json(this.collections[rootCollection][storageKey]);

          case "DELETE":
            if (this.collections[rootCollection][storageKey]) {
              const deletedData = this.collections[rootCollection][storageKey];
              delete this.collections[rootCollection][storageKey];
              this.saveAllCollections();
              return res.json({
                message: "Endpoint deleted",
                deleted_data: deletedData,
              });
            }
            return res.status(404).json({ message: "Endpoint not found" });

          default:
            return res.status(405).json({ error: "Method not allowed" });
        }
      }
    });
  }

  /**
   * Get default HTML template
   * @returns {string} HTML content
   */
  getDefaultHTML() {
    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRUDREX - Mock JSON Server</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #cba6f7; }
        code { background: #313244; padding: 2px 6px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>CRUDREX</h1>
    <p>Mock JSON Server is running on port ${this.port}</p>
    <p>Collections: ${Object.keys(this.collections).join(", ") || "None"}</p>
</body>
</html>`;
  }

  /**
   * Run the server
   * @param {string} host - Host to run the server on
   * @param {boolean} silent - Whether to suppress startup messages
   */
  run(host = "localhost", silent = false) {
    return new Promise((resolve, reject) => {
      try {
        this.server = this.app.listen(this.port, host, () => {
          if (!silent) {
            console.log(
              `Mock JSON Server running at http://${host}:${this.port}`,
            );
          }
          resolve();
        });

        this.server.on("error", (error) => {
          if (error.code === "EADDRINUSE") {
            console.error(`Port ${this.port} is already in use`);
          }
          reject(error);
        });
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Stop the server
   */
  stop() {
    if (this.server) {
      this.server.close();
    }
  }
}

module.exports = MockServer;
