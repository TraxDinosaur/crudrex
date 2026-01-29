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
        CORS(self.app)
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
        
    def save_collection_data(self, collection_name):
        """Save data for a specific collection"""
        filepath = os.path.join(self.data_dir, f"{collection_name}.json")
        with open(filepath, 'w') as f:
            json.dump(self.collections[collection_name], f, indent=2)
            
    def setup_routes(self):
        """Setup all routes for the server"""
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
        @self.app.route('/collections/', methods=['GET'])
        def list_collections():
            return jsonify({"collections": list(self.collections.keys())})
            
        @self.app.route('/collections/', methods=['POST'])
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
        @self.app.route('/<collection_name>/', methods=['GET'])
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
            
        @self.app.route('/<collection_name>/', methods=['POST'])
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
            
        @self.app.route('/<collection_name>/<item_id>', methods=['GET'])
        def get_item(collection_name, item_id):
            if collection_name not in self.collections:
                return jsonify({"error": "Collection not found"}), 404
                
            if item_id not in self.collections[collection_name]:
                return jsonify({"error": "Item not found"}), 404
                
            return jsonify(self.collections[collection_name][item_id])
            
        @self.app.route('/<collection_name>/<item_id>', methods=['PUT'])
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
            
        @self.app.route('/<collection_name>/<item_id>', methods=['PATCH'])
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
            
        @self.app.route('/<collection_name>/<item_id>', methods=['DELETE'])
        def delete_item(collection_name, item_id):
            if collection_name not in self.collections:
                return jsonify({"error": "Collection not found"}), 404
                
            if item_id not in self.collections[collection_name]:
                return jsonify({"error": "Item not found"}), 404
                
            deleted_item = self.collections[collection_name].pop(item_id)
            self.save_collection_data(collection_name)
            return jsonify({"message": "Item deleted", "deleted_item": deleted_item})
            
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