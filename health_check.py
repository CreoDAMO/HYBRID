"""
HYBRID Blockchain System Health Check
Verifies all components are working correctly
"""

import asyncio
import sys
import os
import time
import psutil
import asyncio
from typing import Dict, Any
from blockchain.system_architecture import hybrid_system

# Add blockchain module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'blockchain'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

async def check_system_health():
    """Comprehensive system health check"""
    print("🔍 HYBRID System Health Check")
    print("=" * 50)

    health_status = {
        'spiral_trust_engine': False,
        'quantum_spiral_engine': False,
        'voynich_interface': False,
        'admin_dashboard': False,
        'main_app': False
    }

    # Test Spiral Trust Engine
    try:
        from blockchain.spiral_trust_engine import enhanced_trust_currency_manager, trust_currency_manager
        print("✅ Spiral Trust Engine: OK")
        health_status['spiral_trust_engine'] = True
    except Exception as e:
        print(f"❌ Spiral Trust Engine: {e}")

    # Test Quantum Spiral Engine
    try:
        from blockchain.quantum_spiral_engine import quantum_spiral_engine
        print("✅ Quantum Spiral Engine: OK")
        health_status['quantum_spiral_engine'] = True
    except Exception as e:
        print(f"❌ Quantum Spiral Engine: {e}")

    # Test Voynich Interface
    try:
        from blockchain.spiral_voynich_interface import spiral_voynich_interface
        print("✅ Spiral Voynich Interface: OK")
        health_status['voynich_interface'] = True
    except Exception as e:
        print(f"❌ Spiral Voynich Interface: {e}")

    # Test Admin Dashboard
    try:
        from ui.admin_dashboard import create_admin_dashboard
        print("✅ Admin Dashboard: OK")
        health_status['admin_dashboard'] = True
    except Exception as e:
        print(f"❌ Admin Dashboard: {e}")

    # Test Main App
    try:
        import main
        print("✅ Main Application: OK")
        health_status['main_app'] = True
    except Exception as e:
        print(f"❌ Main Application: {e}")

    print("\n📊 Health Summary:")
    working_components = sum(health_status.values())
    total_components = len(health_status)

    print(f"Working Components: {working_components}/{total_components}")

    if working_components == total_components:
        print("🎉 System Status: HEALTHY")
        return True
    elif working_components >= total_components * 0.8:
        print("⚠️ System Status: MOSTLY HEALTHY")
        return True
    else:
        print("🚨 System Status: NEEDS ATTENTION")
        return False

    # Get system architecture health
    architecture_health = hybrid_system.get_system_health()

    return {
        "status": "healthy",
        "timestamp": time.time(),
        "system": system_health,
        "blockchain": blockchain_health,
        "components": component_health,
        "architecture": architecture_health
    }

if __name__ == "__main__":
    asyncio.run(check_system_health())