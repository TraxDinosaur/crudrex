import os
import json
import uuid
from flask import Flask, request, jsonify, abort, render_template, send_from_directory
from flask_cors import CORS
import threading
import webbrowser
import time
import logging

class MockServer:
    def __init__(self, data_dir="data", port=8085):
        # Configure Flask to look for templates in the correct directory
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        static_dir = os.path.join(os.path.dirname(__file__), 'static')
        
        self.app = Flask(__name__, template_folder=template_dir)
        # Fix CORS with proper configuration
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        self.data_dir = data_dir
        self.port = port
        self.collections = {}
        self.setup_directories()
        self.load_collections()
        self.setup_routes()
        
    def setup_directories(self):
        """Create necessary directories"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
    def load_collections(self):
        """Load existing collections from data directory"""
        if os.path.exists(self.data_dir):
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    collection_name = filename[:-5]  # Remove .json extension
                    self.collections[collection_name] = self.load_collection_data(collection_name)
                    
    def load_collection_data(self, collection_name):
        """Load data for a specific collection"""
        filepath = os.path.join(self.data_dir, f"{collection_name}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
        
    def save_all_collections(self):
        """Save all collections to their respective files"""
        for collection_name in self.collections:
            filepath = os.path.join(self.data_dir, f"{collection_name}.json")
            with open(filepath, 'w') as f:
                json.dump(self.collections[collection_name], f, indent=2)
                
    def save_collection_data(self, collection_name):
        """Save data for a specific collection (deprecated - use save_all_collections)"""
        self.save_all_collections()
            
    def setup_routes(self):
        """Setup all routes for the server"""
        # ALWAYS allow OPTIONS (CORS preflight fix)
        @self.app.before_request
        def allow_options():
            if request.method == 'OPTIONS':
                return '', 200

        # Main page route
        @self.app.route('/', methods=['GET'])
        def index():
            return render_template('index.html')
            
        # API info route (for backwards compatibility)
        @self.app.route('/api/info', methods=['GET'])
        def api_info():
            return jsonify({
                "message": "Mock JSON Server is running",
                "collections": list(self.collections.keys()),
                "instructions": "Create a new collection by POSTing to /collections/",
                "port": self.port
            })
            
        # Collection management routes
        @self.app.route('/collections/', methods=['GET', 'POST'])
        def collections_handler():
            if request.method == 'GET':
                return jsonify({"collections": list(self.collections.keys())})
            elif request.method == 'POST':
                data = request.get_json(force=True)
                if not data or 'name' not in data:
                    return jsonify({"error": "Collection name is required"}), 400
                    
                collection_name = data['name']
                if collection_name in self.collections:
                    return jsonify({"error": "Collection already exists"}), 400
                    
                self.collections[collection_name] = {}
                self.save_collection_data(collection_name)
                return jsonify({"message": f"Collection '{collection_name}' created"}), 201
            
        def list_collections():
            return jsonify({"collections": list(self.collections.keys())})
            
        def create_collection():
            data = request.get_json()
            if not data or 'name' not in data:
                return jsonify({"error": "Collection name is required"}), 400
                
            collection_name = data['name']
            if collection_name in self.collections:
                return jsonify({"error": "Collection already exists"}), 400
                
            self.collections[collection_name] = {}
            self.save_collection_data(collection_name)
            return jsonify({"message": f"Collection '{collection_name}' created"}), 201
            
        # Dynamic collection routes
        @self.app.route('/<collection_name>/', methods=['GET', 'POST'])
        def collection_items_handler(collection_name):
            if request.method == 'GET':
                if collection_name not in self.collections:
                    return jsonify({"error": "Collection not found"}), 404
                    
                # Support query parameters for filtering
                items = []
                for key, value in self.collections[collection_name].items():
                    # Simple filtering support
                    match = True
                    for filter_key, filter_value in request.args.items():
                        if filter_key in value and str(value[filter_key]) != filter_value:
                            match = False
                            break
                    if match:
                        items.append(value)
                        
                return jsonify(items)
            elif request.method == 'POST':
                if collection_name not in self.collections:
                    # Auto-create collection if it doesn't exist
                    self.collections[collection_name] = {}
                    
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "JSON data required"}), 400
                    
                # Generate ID if not provided
                if 'id' not in data:
                    data['id'] = str(uuid.uuid4())
                    
                # Store with ID as key
                self.collections[collection_name][data['id']] = data
                self.save_collection_data(collection_name)
                return jsonify(data), 201
                
        def get_all_items(collection_name):
            if collection_name not in self.collections:
                return jsonify({"error": "Collection not found"}), 404
                
            # Support query parameters for filtering
            items = []
            for key, value in self.collections[collection_name].items():
                # Simple filtering support
                match = True
                for filter_key, filter_value in request.args.items():
                    if filter_key in value and str(value[filter_key]) != filter_value:
                        match = False
                        break
                if match:
                    items.append(value)
                    
            return jsonify(items)
            
        def create_item(collection_name):
            if collection_name not in self.collections:
                # Auto-create collection if it doesn't exist
                self.collections[collection_name] = {}
                
            data = request.get_json()
            if not data:
                return jsonify({"error": "JSON data required"}), 400
                
            # Generate ID if not provided
            if 'id' not in data:
                data['id'] = str(uuid.uuid4())
                
            # Store with ID as key
            self.collections[collection_name][data['id']] = data
            self.save_collection_data(collection_name)
            return jsonify(data), 201
            
        @self.app.route('/<collection_name>/<item_id>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
        def item_handler(collection_name, item_id):
            if request.method == 'GET':
                if collection_name not in self.collections:
                    return jsonify({"error": "Collection not found"}), 404
                    
                if item_id not in self.collections[collection_name]:
                    return jsonify({"error": "Item not found"}), 404
                    
                return jsonify(self.collections[collection_name][item_id])
            elif request.method == 'POST':
                if collection_name not in self.collections:
                    self.collections[collection_name] = {}
                    
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "JSON data required"}), 400
                    
                data['id'] = item_id
                self.collections[collection_name][item_id] = data
                self.save_collection_data(collection_name)
                return jsonify(data), 201
            elif request.method == 'PUT':
                if collection_name not in self.collections:
                    return jsonify({"error": "Collection not found"}), 404
                    
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "JSON data required"}), 400
                    
                # Update the item
                data['id'] = item_id  # Ensure ID consistency
                self.collections[collection_name][item_id] = data
                self.save_collection_data(collection_name)
                return jsonify(data)
            elif request.method == 'PATCH':
                if collection_name not in self.collections:
                    return jsonify({"error": "Collection not found"}), 404
                    
                if item_id not in self.collections[collection_name]:
                    return jsonify({"error": "Item not found"}), 404
                    
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "JSON data required"}), 400
                    
                # Partially update the item
                for key, value in data.items():
                    self.collections[collection_name][item_id][key] = value
                    
                self.save_collection_data(collection_name)
                return jsonify(self.collections[collection_name][item_id])
            elif request.method == 'DELETE':
                if collection_name not in self.collections:
                    return jsonify({"error": "Collection not found"}), 404
                    
                if item_id not in self.collections[collection_name]:
                    return jsonify({"error": "Item not found"}), 404
                    
                deleted_item = self.collections[collection_name].pop(item_id)
                self.save_collection_data(collection_name)
                return jsonify({"message": "Item deleted", "deleted_item": deleted_item})
                
        def get_item(collection_name, item_id):
            if collection_name not in self.collections:
                return jsonify({"error": "Collection not found"}), 404
                
            if item_id not in self.collections[collection_name]:
                return jsonify({"error": "Item not found"}), 404
                
            return jsonify(self.collections[collection_name][item_id])
            
        def update_item(collection_name, item_id):
            if collection_name not in self.collections:
                return jsonify({"error": "Collection not found"}), 404
                
            data = request.get_json()
            if not data:
                return jsonify({"error": "JSON data required"}), 400
                
            # Update the item
            data['id'] = item_id  # Ensure ID consistency
            self.collections[collection_name][item_id] = data
            self.save_collection_data(collection_name)
            return jsonify(data)
            
        def patch_item(collection_name, item_id):
            if collection_name not in self.collections:
                return jsonify({"error": "Collection not found"}), 404
                
            if item_id not in self.collections[collection_name]:
                return jsonify({"error": "Item not found"}), 404
                
            data = request.get_json()
            if not data:
                return jsonify({"error": "JSON data required"}), 400
                
            # Partially update the item
            for key, value in data.items():
                self.collections[collection_name][item_id][key] = value
                
            self.save_collection_data(collection_name)
            return jsonify(self.collections[collection_name][item_id])
            
        def delete_item(collection_name, item_id):
            if collection_name not in self.collections:
                return jsonify({"error": "Collection not found"}), 404
                
            if item_id not in self.collections[collection_name]:
                return jsonify({"error": "Item not found"}), 404
                
            deleted_item = self.collections[collection_name].pop(item_id)
            self.save_collection_data(collection_name)
            return jsonify({"message": "Item deleted", "deleted_item": deleted_item})
            
        # Catch-all route for nested paths (json-server style)
        @self.app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
        def catch_all(path):
            if request.method == 'OPTIONS':
                return '', 200
                
            # Split path into components
            path_parts = path.split('/')
            if not path_parts:
                return jsonify({"error": "Invalid path"}), 400
                
            # Use root collection name (first part of path)
            root_collection = path_parts[0]
            # Use hyphen-separated path for storage key
            storage_key = path.replace('/', '-')
            
            # Ensure root collection exists
            if root_collection not in self.collections:
                self.collections[root_collection] = {}
                
            # Get current timestamp
            current_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            
            if request.method == 'GET':
                # Return all items under this endpoint
                if storage_key in self.collections[root_collection]:
                    return jsonify(self.collections[root_collection][storage_key])
                else:
                    return jsonify({"items": []})
            
            elif request.method == 'POST':
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "JSON data required"}), 400
                    
                # Ensure the endpoint structure exists
                if storage_key not in self.collections[root_collection]:
                    self.collections[root_collection][storage_key] = {"items": []}
                elif "items" not in self.collections[root_collection][storage_key]:
                    self.collections[root_collection][storage_key] = {"items": []}
                    
                # Handle both object and array payloads
                if isinstance(data, list):
                    # If it's an array, process each item
                    results = []
                    for item in data:
                        if isinstance(item, dict):
                            # Extract ID or generate one
                            item_id = item.pop('id', str(uuid.uuid4()))
                            
                            # Separate metadata from data
                            item_data = {k: v for k, v in item.items()}
                            
                            # Create structured item
                            structured_item = {
                                "id": item_id,
                                "createdAt": current_time,
                                "updatedAt": current_time,
                                "data": item_data
                            }
                            
                            self.collections[root_collection][storage_key]["items"].append(structured_item)
                            results.append(structured_item)
                    self.save_all_collections()
                    return jsonify({"items": results}), 201
                else:
                    # If it's an object, process normally
                    # Extract ID or generate one
                    item_id = data.pop('id', str(uuid.uuid4()))
                    
                    # Separate metadata from data
                    item_data = {k: v for k, v in data.items()}
                    
                    # Create structured item
                    structured_item = {
                        "id": item_id,
                        "createdAt": current_time,
                        "updatedAt": current_time,
                        "data": item_data
                    }
                    
                    # Store in the endpoint array
                    self.collections[root_collection][storage_key]["items"].append(structured_item)
                    self.save_all_collections()
                    return jsonify(structured_item), 201
                    
            elif request.method == 'PUT':
                # PUT replaces the entire endpoint data
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "JSON data required"}), 400
                    
                # Replace the entire endpoint data
                self.collections[root_collection][storage_key] = data
                self.save_all_collections()
                return jsonify(data)
                
            elif request.method == 'PATCH':
                # PATCH updates specific items in the endpoint
                data = request.get_json(force=True)
                if not data:
                    return jsonify({"error": "JSON data required"}), 400
                    
                # Ensure the endpoint structure exists
                if storage_key not in self.collections[root_collection]:
                    self.collections[root_collection][storage_key] = {"items": []}
                elif "items" not in self.collections[root_collection][storage_key]:
                    self.collections[root_collection][storage_key] = {"items": []}
                    
                # Update items if provided
                if "items" in data:
                    # Update existing items or add new ones
                    for updated_item in data["items"]:
                        item_id = updated_item.get("id")
                        if item_id:
                            # Find existing item and update it
                            found = False
                            for i, existing_item in enumerate(self.collections[root_collection][storage_key]["items"]):
                                if existing_item.get("id") == item_id:
                                    # Update the item
                                    updated_item["updatedAt"] = current_time
                                    self.collections[root_collection][storage_key]["items"][i] = updated_item
                                    found = True
                                    break
                            # If not found, add as new item
                            if not found:
                                updated_item.setdefault("createdAt", current_time)
                                updated_item.setdefault("updatedAt", current_time)
                                self.collections[root_collection][storage_key]["items"].append(updated_item)
                                
                self.save_all_collections()
                return jsonify(self.collections[root_collection][storage_key])
                
            elif request.method == 'DELETE':
                # DELETE removes the entire endpoint
                if storage_key in self.collections[root_collection]:
                    deleted_data = self.collections[root_collection].pop(storage_key)
                    self.save_all_collections()
                    return jsonify({"message": "Endpoint deleted", "deleted_data": deleted_data})
                else:
                    return jsonify({"message": "Endpoint not found"}), 404
            
    def run(self, host='localhost', debug=False):
        """Run the server"""
        # Suppress only the specific Flask startup messages while keeping access logs
        import sys
        from werkzeug.serving import WSGIRequestHandler
        from werkzeug.serving import _log
        
        # Override the internal log function to filter out startup messages
        original_log = _log
        def filtered_log(type, message, *args):
            # Skip the specific startup messages we don't want
            if "Serving Flask app" in message or "Debug mode" in message or "WARNING:" in message:
                return
            # Show the running message but make it cleaner
            if "Running on" in message:
                return  # We already show our own startup message
            original_log(type, message, *args)
            
        # Monkey patch the log function
        import werkzeug.serving
        werkzeug.serving._log = filtered_log
        
        # Custom request handler for access logs
        class CustomRequestHandler(WSGIRequestHandler):
            def log(self, type, message, *args):
                # Continue to log access requests
                if type == 'info':
                    super().log(type, message, *args)
                    
        self.app.run(host=host, port=self.port, debug=debug, 
                    request_handler=CustomRequestHandler)
        
        # Restore original log function
        werkzeug.serving._log = original_log
        
    def run_async(self, host='localhost'):
        """Run the server in a separate thread"""
        thread = threading.Thread(target=self.run, kwargs={'host': host})
        thread.daemon = True
        thread.start()
        return thread

def main():
    """Main entry point for the server"""
    server = MockServer()
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(1)
        webbrowser.open(f'http://localhost:{server.port}/')
        
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print(f"Mock JSON Server starting on http://localhost:{server.port}")
    print("Press Ctrl+C to stop the server")
    server.run()

if __name__ == '__main__':
    main()