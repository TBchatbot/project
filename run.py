import subprocess
import sys
import os

def install_requirements():
    try:
        import streamlit
        print("✅ Streamlit is already installed")
    except ImportError:
        print("📦 Installing Streamlit...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✅ Streamlit installed successfully")

def run_app():
    print("🚀 Starting TB Health Assistant...")
    print("🌐 The app will open in your browser automatically")
    print("📍 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 TB Health Assistant stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error running the application: {e}")
        print("💡 Try running: streamlit run app.py")

if __name__ == "__main__":
    print("🏥 TB Health Assistant - Python Version")
    print("=" * 50)
    
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        print("💡 Make sure you're in the correct folder with all files")
        sys.exit(1)
    
    install_requirements()
    run_app()
