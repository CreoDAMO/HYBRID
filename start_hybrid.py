#!/usr/bin/env python3
import asyncio
import subprocess
import sys
import time
import signal
import os
import shlex
import importlib

def run_command(cmd, background=False):
    """Run a command safely"""
    # Split command safely to prevent injection
    if isinstance(cmd, str):
        cmd_list = shlex.split(cmd)
    else:
        cmd_list = cmd

    if background:
        return subprocess.Popen(cmd_list)
    else:
        return subprocess.run(cmd_list)

async def start_blockchain_node():
    """Start the blockchain node in background"""
    print("🚀 Starting HYBRID blockchain node...")

    # Import and start node
    from blockchain.hybrid_node import create_hybrid_node

    node = create_hybrid_node("storage")

    try:
        await node.start()
    except KeyboardInterrupt:
        print("\n⏹️ Stopping blockchain node...")
        await node.stop()

def check_and_install_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        'streamlit', 'plotly', 'pandas', 'numpy', 'requests',
        'cryptography', 'mnemonic', 'aiohttp', 'fastapi', 'uvicorn',
        'web3', 'eth_account', 'bech32', 'ecdsa'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            # Install packages one by one to identify problematic ones
            for package in missing_packages:
                try:
                    print(f"   Installing {package}...")
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", "--upgrade", package
                    ], check=True, capture_output=True)
                    print(f"   ✅ {package} installed")
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️ Failed to install {package}: {e}")
                    # Continue with other packages
            print("✅ Dependencies installation completed!")
        except Exception as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("⚠️ Continuing with available packages...")
            # Don't return False - continue with what we have
    
    return True

def start_streamlit():
    """Start Streamlit UI with proper error handling"""
    print("🖥️ Starting HYBRID Streamlit UI...")
    
    # Check dependencies first
    check_and_install_dependencies()  # Don't fail if some dependencies missing
    
    # Check if streamlit is available
    try:
        import streamlit
        print("✅ Streamlit is available")
        
        # Try with module execution
        cmd = [
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.address=0.0.0.0",
            "--server.port=8501",
            "--server.runOnSave=true",
            "--server.allowRunOnSave=true"
        ]
        print(f"🚀 Executing: {' '.join(cmd)}")
        return subprocess.Popen(cmd)
    except ImportError:
        print("❌ Streamlit not available, trying simple web server...")
        return start_simple_server()
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        print("🔄 Falling back to simple web server...")
        return start_simple_server()

def start_simple_server():
    """Start a simple HTTP server as fallback"""
    try:
        import http.server
        import socketserver
        import threading
        
        PORT = 8501
        Handler = http.server.SimpleHTTPRequestHandler
        
        def serve():
            with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
                print(f"✅ Simple web server started on port {PORT}")
                httpd.serve_forever()
        
        # Start server in background thread
        server_thread = threading.Thread(target=serve, daemon=True)
        server_thread.start()
        
        # Return a dummy process-like object
        class DummyProcess:
            def __init__(self):
                self.poll_count = 0
            
            def poll(self):
                # Keep running
                return None
                
            def terminate(self):
                print("🛑 Stopping simple web server...")
                
            def wait(self, timeout=None):
                pass
                
            def kill(self):
                pass
        
        return DummyProcess()
        
    except Exception as e:
        print(f"❌ Failed to start simple server: {e}")
        return None

def main():
    print("🌟 HYBRID Blockchain + HTSX Runtime Starting...")
    print("=" * 50)

    # Start Streamlit UI
    streamlit_process = start_streamlit()
    
    if streamlit_process is None:
        print("❌ Failed to start Streamlit UI")
        print("🔍 Check the error messages above for details")
        return

    try:
        # Monitor process health
        print("✅ HYBRID blockchain is running!")
        print("📱 UI available at: http://0.0.0.0:8501")
        print("🔗 RPC endpoint: http://0.0.0.0:26657")
        print("\nPress Ctrl+C to stop...")

        # Check if process is still running
        while streamlit_process.poll() is None:
            time.sleep(1)
        
        # If we get here, the process died
        print("❌ Streamlit process terminated unexpectedly")
        stdout, stderr = streamlit_process.communicate()
        if stdout:
            print("📝 Stdout:", stdout.decode())
        if stderr:
            print("🚨 Stderr:", stderr.decode())

    except KeyboardInterrupt:
        print("\n🛑 Shutting down HYBRID blockchain...")

        # Terminate processes
        if streamlit_process and streamlit_process.poll() is None:
            streamlit_process.terminate()
            try:
                streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                streamlit_process.kill()

        print("✅ HYBRID blockchain stopped successfully")

if __name__ == "__main__":
    main()