import argparse
import sys
import os
import subprocess
import signal
import time
from pathlib import Path

# Add the parent directory to sys.path to import the api module
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.server import MockServer
import threading

def main():
    parser = argparse.ArgumentParser(description='Crudrex - Mock JSON Server')
    parser.add_argument('--port', type=int, default=8085, help='Port to run the server on (default: 8085)')
    parser.add_argument('--data-dir', default='data', help='Directory to store data files (default: data)')
    parser.add_argument('--host', default='localhost', help='Host to run the server on (default: localhost)')
    
    args = parser.parse_args()
    
    try:
        server = MockServer(data_dir=args.data_dir, port=args.port)
        print(f"Crudrex server started at http://{args.host}:{args.port}")
        server.run(host=args.host)
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()