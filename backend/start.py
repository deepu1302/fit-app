"""
FitLife Tracker - Run Script
Start the Flask backend server and open the app in your browser
"""

import os
import sys
import webbrowser
import time
import subprocess

def main():
    print("=" * 50)
    print("FitLife Tracker - Starting...")
    print("=" * 50)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(script_dir, '..')
    
    # Change to the project directory
    os.chdir(project_dir)
    
    print(f"\nProject directory: {project_dir}")
    print(f"Starting Flask server on http://localhost:5000\n")
    
    # Start Flask in a subprocess
    try:
        # Import and run the app
        sys.path.insert(0, script_dir)
        from app import app
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        # Start browser in background
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"Error: Could not import app - {e}")
        print("\nMake sure you have installed the requirements:")
        print("  pip install -r backend/requirements.txt")
        return 1
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
