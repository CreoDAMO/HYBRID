
#!/usr/bin/env python3
"""
HYBRID Blockchain Health Check
Comprehensive system verification for all components
"""
import sys
import os
import importlib
from typing import Dict, List, Any

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.9+)"

def check_dependencies():
    """Check all required dependencies"""
    required_packages = [
        'streamlit', 'plotly', 'pandas', 'numpy', 'requests',
        'cryptography', 'mnemonic', 'aiohttp', 'fastapi', 'uvicorn',
        'web3', 'eth_account', 'bech32', 'ecdsa', 'secp256k1'
    ]
    
    results = {}
    for package in required_packages:
        try:
            importlib.import_module(package)
            results[package] = "✅ Available"
        except ImportError:
            results[package] = "❌ Missing"
    
    return results

def check_blockchain_modules():
    """Check blockchain module availability"""
    blockchain_modules = [
        'blockchain.hybrid_node',
        'blockchain.wallet_manager', 
        'blockchain.transaction_pool',
        'blockchain.block_producer',
        'blockchain.validator_set',
        'blockchain.spiral_trust_engine',
        'blockchain.multi_ai_orchestrator',
        'blockchain.holographic_blockchain_engine',
        'blockchain.nvidia_cloud_integration',
        'blockchain.agglayer_integration',
        'blockchain.circle_usdc_integration',
        'blockchain.coinbase_integration',
        'blockchain.x_moe',
        'blockchain.x_licence',
        'blockchain.x_naas',
        'blockchain.consensus',
        'blockchain.ethermint',
        'blockchain.staking',
        'blockchain.governance'
    ]
    
    results = {}
    for module in blockchain_modules:
        try:
            importlib.import_module(module)
            results[module] = "✅ Available"
        except ImportError:
            results[module] = "❌ Missing"
    
    return results

def check_ui_modules():
    """Check UI module availability"""
    ui_modules = [
        'ui.streamlit_ui',
        'ui.admin_dashboard',
        'ui.holographic_interface',
        'ui.founder_dashboard',
        'ui.wallet_generator'
    ]
    
    results = {}
    for module in ui_modules:
        try:
            importlib.import_module(module)
            results[module] = "✅ Available"
        except ImportError:
            results[module] = "❌ Missing"
    
    return results

def check_component_modules():
    """Check component module availability"""
    component_modules = [
        'components.hybrid_htsx',
        'components.hybrid_htsx_holographic',
        'components.spiral_script_compiler'
    ]
    
    results = {}
    for module in component_modules:
        try:
            importlib.import_module(module)
            results[module] = "✅ Available"
        except ImportError:
            results[module] = "❌ Missing"
    
    return results

def check_file_structure():
    """Check critical file structure"""
    critical_files = [
        'main.py',
        'start_hybrid.py',
        'requirements.txt',
        'README.md',
        '.replit',
        'blockchain/__init__.py',
        'ui/__init__.py',
        'components/hybrid_htsx.py'
    ]
    
    results = {}
    for file_path in critical_files:
        if os.path.exists(file_path):
            results[file_path] = "✅ Exists"
        else:
            results[file_path] = "❌ Missing"
    
    return results

def main():
    """Run comprehensive health check"""
    print("🌟 HYBRID Blockchain Health Check")
    print("=" * 50)
    
    # Check Python version
    python_ok, python_msg = check_python_version()
    print(f"\n🐍 Python Version: {python_msg}")
    
    # Check dependencies
    print("\n📦 Dependencies:")
    deps = check_dependencies()
    for package, status in deps.items():
        print(f"   {package}: {status}")
    
    # Check blockchain modules
    print("\n⛓️ Blockchain Modules:")
    blockchain_modules = check_blockchain_modules()
    for module, status in blockchain_modules.items():
        print(f"   {module}: {status}")
    
    # Check UI modules
    print("\n🖥️ UI Modules:")
    ui_modules = check_ui_modules()
    for module, status in ui_modules.items():
        print(f"   {module}: {status}")
    
    # Check component modules
    print("\n🧩 Component Modules:")
    component_modules = check_component_modules()
    for module, status in component_modules.items():
        print(f"   {module}: {status}")
    
    # Check file structure
    print("\n📁 File Structure:")
    files = check_file_structure()
    for file_path, status in files.items():
        print(f"   {file_path}: {status}")
    
    # Summary
    print("\n📊 Health Check Summary:")
    
    total_deps = len(deps)
    available_deps = sum(1 for status in deps.values() if "✅" in status)
    print(f"   Dependencies: {available_deps}/{total_deps} available")
    
    total_blockchain = len(blockchain_modules)
    available_blockchain = sum(1 for status in blockchain_modules.values() if "✅" in status)
    print(f"   Blockchain Modules: {available_blockchain}/{total_blockchain} available")
    
    total_ui = len(ui_modules)
    available_ui = sum(1 for status in ui_modules.values() if "✅" in status)
    print(f"   UI Modules: {available_ui}/{total_ui} available")
    
    total_components = len(component_modules)
    available_components = sum(1 for status in component_modules.values() if "✅" in status)
    print(f"   Component Modules: {available_components}/{total_components} available")
    
    total_files = len(files)
    existing_files = sum(1 for status in files.values() if "✅" in status)
    print(f"   Critical Files: {existing_files}/{total_files} existing")
    
    # Overall health
    if (available_deps >= total_deps * 0.8 and 
        available_blockchain >= total_blockchain * 0.7 and
        existing_files >= total_files * 0.9):
        print("\n🎉 Overall Health: EXCELLENT")
        print("   HYBRID blockchain is ready for operation!")
    elif (available_deps >= total_deps * 0.6 and 
          available_blockchain >= total_blockchain * 0.5):
        print("\n⚠️ Overall Health: GOOD")
        print("   HYBRID blockchain can run with some limitations")
    else:
        print("\n❌ Overall Health: NEEDS ATTENTION")
        print("   Please install missing dependencies and modules")

if __name__ == "__main__":
    main()
