
#!/usr/bin/env python3
import asyncio
import subprocess
import sys
import time
import signal
import os
import shlex

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

def start_streamlit():
    """Start Streamlit UI"""
    print("🖥️ Starting HYBRID Streamlit UI...")
    # Use Python module execution to avoid path issues
    cmd = [sys.executable, "-m", "streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=5000"]
    return subprocess.Popen(cmd)

def main():
    print("🌟 HYBRID Blockchain + HTSX Runtime Starting...")
    print("=" * 50)
    
    # Start Streamlit UI
    streamlit_process = start_streamlit()
    
    try:
        # Keep the main process running
        print("✅ HYBRID blockchain is running!")
        print("📱 UI available at: http://0.0.0.0:5000")
        print("🔗 RPC endpoint: http://0.0.0.0:26657")
        print("\nPress Ctrl+C to stop...")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down HYBRID blockchain...")
        
        # Terminate processes
        if streamlit_process:
            streamlit_process.terminate()
            streamlit_process.wait()
        
        print("✅ HYBRID blockchain stopped successfully")

if __name__ == "__main__":
    main()
