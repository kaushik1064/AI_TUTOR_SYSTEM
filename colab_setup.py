"""
Google Colab setup script for AI Tutor System
Automatically installs dependencies and configures the environment
"""

import os
import subprocess
import sys
import time
import threading
import json
from pathlib import Path

def install_dependencies():
    """Install required Python packages"""
    print("🔧 Installing dependencies...")
    
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0", 
        "streamlit==1.28.1",
        "pydantic==2.4.2",
        "pydantic-settings==2.0.3",
        "google-generativeai==0.3.1",
        "google-cloud-firestore==2.13.1",
        "firebase-admin==6.2.0",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "plotly==5.17.0",
        "pandas==2.0.3",
        "requests==2.31.0",
        "sentence-transformers==2.2.2",
        "pyngrok"
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          check=True, capture_output=True)
            print(f"✅ Installed {package.split('==')[0]}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def setup_environment():
    """Setup environment variables"""
    print("🔐 Setting up environment...")
    
    # Prompt for required credentials
    gemini_api_key = input("🔑 Enter your Gemini Pro API Key: ").strip()
    if not gemini_api_key:
        print("❌ Gemini API key is required!")
        return False
    
    google_project_id = input("🌐 Enter your Google Cloud Project ID: ").strip()
    if not google_project_id:
        print("❌ Google Cloud Project ID is required!")
        return False
    
    # Set environment variables
    os.environ['GEMINI_API_KEY'] = gemini_api_key
    os.environ['GOOGLE_CLOUD_PROJECT'] = google_project_id
    os.environ['SECRET_KEY'] = 'colab-demo-secret-key-12345'
    os.environ['DEBUG'] = 'True'
    os.environ['HOST'] = '0.0.0.0'
    os.environ['PORT'] = '8000'
    
    print("✅ Environment configured successfully!")
    return True

def upload_firebase_credentials():
    """Handle Firebase credentials upload"""
    print("🔥 Firebase setup...")
    
    use_firebase = input("📤 Do you want to upload Firebase credentials? (y/n): ").strip().lower()
    
    if use_firebase == 'y':
        print("📁 Please upload your Firebase service account JSON file when prompted.")
        try:
            from google.colab import files
            uploaded = files.upload()
            
            if uploaded:
                filename = list(uploaded.keys())[0]
                print(f"✅ Firebase credentials uploaded: {filename}")
                
                # Set the credentials path
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = filename
                
                # Read and set Firebase config as environment variable
                with open(filename, 'r') as f:
                    firebase_config = json.load(f)
                os.environ['FIREBASE_CONFIG'] = json.dumps(firebase_config)
                
                return True
        except ImportError:
            print("⚠️  Not in Colab environment, skipping file upload")
        except Exception as e:
            print(f"❌ Error uploading Firebase credentials: {e}")
    
    # Use demo mode without Firebase
    print("🔄 Using demo mode without Firebase")
    demo_config = {
        "type": "service_account",
        "project_id": os.environ.get('GOOGLE_CLOUD_PROJECT', 'demo-project'),
        "private_key_id": "demo-key-id",
        "private_key": "demo-private-key", 
        "client_email": "demo@demo-project.iam.gserviceaccount.com",
        "client_id": "demo-client-id"
    }
    os.environ['FIREBASE_CONFIG'] = json.dumps(demo_config)
    return True

def start_backend_server():
    """Start the FastAPI backend server"""
    print("🚀 Starting backend server...")
    
    def run_backend():
        try:
            subprocess.run([
                sys.executable, "-m", "uvicorn",
                "ai_tutor_system.backend.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ], check=True)
        except Exception as e:
            print(f"❌ Backend server error: {e}")
    
    # Start backend in background thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(10)
    
    # Test if server is running
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running!")
            return True
    except:
        pass
    
    print("⚠️  Backend server may still be starting...")
    return True

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting frontend...")
    
    try:
        # Start Streamlit in background
        subprocess.Popen([
            sys.executable, "-m", "streamlit", "run",
            "ai_tutor_system/frontend/app.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--server.enableCORS", "false"
        ])
        
        time.sleep(5)
        print("✅ Frontend server started!")
        return True
        
    except Exception as e:
        print(f"❌ Frontend start error: {e}")
        return False

def create_public_urls():
    """Create public URLs using ngrok"""
    print("🌐 Creating public URLs...")
    
    try:
        from pyngrok import ngrok
        
        # Create tunnels
        backend_tunnel = ngrok.connect(8000)
        frontend_tunnel = ngrok.connect(8501)
        
        print("\n🎉 AI Tutor System is now live!")
        print("=" * 50)
        print(f"🔧 Backend API: {backend_tunnel.public_url}")
        print(f"🎓 AI Tutor App: {frontend_tunnel.public_url}")
        print("=" * 50)
        print("\n📚 Features available:")
        print("  ✅ Conversational AI tutoring")
        print("  ✅ Academic progress tracking")
        print("  ✅ Emotional support system")
        print("  ✅ Study reminders & scheduling")
        print("  ✅ Interactive analytics dashboard")
        print("\n🚀 Click the AI Tutor App link above to start!")
        
        return True
        
    except ImportError:
        print("❌ pyngrok not installed. Install it with: !pip install pyngrok")
        return False
    except Exception as e:
        print(f"❌ Error creating public URLs: {e}")
        print("\n🔧 Manual access:")
        print("- Backend: http://localhost:8000")
        print("- Frontend: http://localhost:8501")
        return False

def main():
    """Main setup function"""
    print("🎓 AI Tutor System - Colab Setup")
    print("=" * 40)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Step 2: Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment") 
        return False
    
    # Step 3: Firebase credentials
    if not upload_firebase_credentials():
        print("❌ Failed to setup Firebase")
        return False
    
    # Step 4: Start backend
    if not start_backend_server():
        print("❌ Failed to start backend")
        return False
    
    # Step 5: Start frontend
    if not start_frontend():
        print("❌ Failed to start frontend")
        return False
    
    # Step 6: Create public URLs
    create_public_urls()
    
    print("\n✅ Setup completed successfully!")
    print("\n📖 Usage Instructions:")
    print("1. Click the AI Tutor App link above")
    print("2. Create an account or login (demo credentials work)")
    print("3. Start chatting with your AI tutor!")
    print("4. Explore the dashboard, reminders, and reports")
    print("\n💡 Tip: Keep this Colab notebook running to maintain the service")
    
    return True

if __name__ == "__main__":
    main()
