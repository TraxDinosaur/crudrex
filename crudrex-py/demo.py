#!/usr/bin/env python3
"""
Demo script for CRUDREX - Mock JSON Server
Shows how to use CRUDREX programmatically
"""

import os
import sys
import time
import threading
import webbrowser
import requests
from crudrex.api.server import MockServer

def demo():
    """Demonstrate CRUDREX functionality"""
    print("🚀 Starting CRUDREX Demo")
    print("=" * 50)
    
    # Create server instance
    server = MockServer(data_dir="demo_data", port=8087)
    
    # Start server in background thread
    def run_server():
        server.run(host='localhost', debug=False)
    
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Starting server on http://localhost:8087...")
    time.sleep(2)
    
    base_url = "http://localhost:8087"
    
    try:
        # Open browser to show the web interface
        print("🌐 Opening web interface in browser...")
        webbrowser.open(f"{base_url}/")
        
        # Demonstrate API usage
        print("\n🔧 Demonstrating API usage:")
        print("-" * 30)
        
        # 1. Create a collection
        print("1. Creating 'products' collection...")
        response = requests.post(
            f"{base_url}/collections/",
            json={"name": "products"},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            print("   ✅ Collection created!")
        else:
            print(f"   ❌ Failed: {response.json()}")
            
        # 2. Add some products
        print("\n2. Adding sample products...")
        products = [
            {"name": "Laptop", "price": 999.99, "category": "Electronics"},
            {"name": "Book", "price": 19.99, "category": "Education"},
            {"name": "Coffee Mug", "price": 12.50, "category": "Kitchen"}
        ]
        
        for i, product in enumerate(products, 1):
            response = requests.post(
                f"{base_url}/products/",
                json=product,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 201:
                print(f"   ✅ Product {i} added: {product['name']}")
            else:
                print(f"   ❌ Failed to add product {i}")
                
        # 3. Retrieve all products
        print("\n3. Retrieving all products...")
        response = requests.get(f"{base_url}/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"   ✅ Retrieved {len(products)} products:")
            for product in products:
                print(f"      - {product['name']}: ${product['price']}")
        else:
            print("   ❌ Failed to retrieve products")
            
        # 4. Filter products
        print("\n4. Filtering products by category...")
        response = requests.get(f"{base_url}/products/?category=Electronics")
        if response.status_code == 200:
            electronics = response.json()
            print(f"   ✅ Found {len(electronics)} electronics products:")
            for product in electronics:
                print(f"      - {product['name']}")
        else:
            print("   ❌ Failed to filter products")
            
        print("\n" + "=" * 50)
        print("🎉 Demo completed successfully!")
        print("\n📝 Next steps:")
        print("   1. Visit http://localhost:8087 in your browser")
        print("   2. Explore the web interface")
        print("   3. Try creating collections and adding data")
        print("   4. Use the API endpoints as shown above")
        print("\n💡 Pro tip: Use Ctrl+C to stop the server when done")
        
        # Keep server running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            return True
            
    except Exception as e:
        print(f"\n💥 Error: {e}")
        return False
    finally:
        # Clean up demo data
        if os.path.exists("demo_data"):
            import shutil
            shutil.rmtree("demo_data")

if __name__ == "__main__":
    success = demo()
    sys.exit(0 if success else 1)