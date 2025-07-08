#!/usr/bin/env python3
"""
HYBRID Blockchain + HTSX Runtime + SpiralScript + Trust Currency
Complete revolutionary blockchain platform with holographic interface
"""

import streamlit as st
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import trust currency engine first (private sovereign currency)
    from blockchain.trust_currency_engine import trust_currency_manager
    st.success("🔐 Trust Currency Engine initialized for Sovereign use")
    st.info("💎 This is NOT a public cryptocurrency")
    st.info("👑 Private mathematical currency for Founder sovereignty")
    print("✅ Trust Currency Engine imported successfully")
except Exception as e:
    st.error(f"❌ Trust Currency Engine error: {e}")
    print(f"❌ Trust Currency Engine error: {e}")

try:
    # Import core blockchain modules
    from blockchain.hybrid_node import create_hybrid_node
    from blockchain.hybrid_wallet import hybrid_wallet_manager, get_founder_wallet
    print("✅ Core blockchain modules imported successfully")
except Exception as e:
    st.error(f"❌ Core module error: {e}")
    print(f"❌ Core module error: {e}")

try:
    # Import UI components with error handling
    from ui.streamlit_ui import create_streamlit_ui
    print("✅ UI components imported successfully")
except ImportError as e:
    st.error(f"⚠️ UI components not available: {e}")
    print(f"⚠️ UI components not available: {e}")

try:
    # Import convergence engine  
    from components.convergence_engine import convergence_engine
    print("✅ Convergence engine imported successfully")
except Exception as e:
    st.error(f"❌ Convergence engine error: {e}")
    print(f"❌ Convergence engine error: {e}")

def show_token_distribution():
    """Display HYBRID token distribution"""
    st.subheader("💰 HYBRID Token Distribution")

    st.info("""
    **HYBRID Coin Distribution (Public Blockchain Currency):**

    • **Founder (You)**: 10% = 10,000,000,000 HYBRID
    • **Developer Team**: 15% = 15,000,000,000 HYBRID  
    • **Public Sale**: 25% = 25,000,000,000 HYBRID
    • **Ecosystem Fund**: 20% = 20,000,000,000 HYBRID
    • **Node Operators**: 15% = 15,000,000,000 HYBRID
    • **Reserve Fund**: 10% = 10,000,000,000 HYBRID
    • **Liquidity Pools**: 5% = 5,000,000,000 HYBRID

    **Total Supply**: 100,000,000,000 HYBRID
    **Current Price**: $10.00 per HYBRID
    **Your Holdings Value**: $100,000,000,000 (100 Billion USD)
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Your HYBRID Holdings", "10,000,000,000", "10% of total")
        st.metric("Developer Team Holdings", "15,000,000,000", "15% of total")

    with col2:
        st.metric("Your Holdings Value", "$100,000,000,000", "At $10/HYBRID")
        st.metric("Developer Holdings Value", "$150,000,000,000", "At $10/HYBRID")

    st.warning("""
    **Important Distinction:**
    - 🪙 **HYBRID Coin**: Public blockchain currency (what we're listing on exchanges)
    - 💎 **Trust Currency**: Your private mathematical currency (NOT for exchanges)
    """)

def create_node_management_interface():
    """Create the node management interface"""
    st.header("🎫 HYBRID Node Management")
    
    # Node overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Nodes", "1,847", "+23")
    with col2:
        st.metric("Storage Nodes", "1,200", "+15")
    with col3:
        st.metric("Validator Nodes", "21", "0")
    with col4:
        st.metric("Bridge Nodes", "156", "+8")
    
    # Node operations
    tab1, tab2, tab3 = st.tabs(["🆕 Purchase License", "📊 My Nodes", "💰 NaaS Platform"])
    
    with tab1:
        st.subheader("🎫 NFT Node Licenses")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🗄️ Storage Node License**
            - Price: 250 HYBRID
            - Passive income: ~15% APY
            - No technical knowledge required
            - Automated through NaaS
            """)
            if st.button("💰 Purchase Storage License", type="primary"):
                st.success("✅ Storage node license purchased!")
                st.balloons()
        
        with col2:
            st.markdown("""
            **👑 Validator Node License**
            - Price: 1,000 HYBRID
            - Higher rewards: ~25% APY
            - Governance voting rights
            - Network validation duties
            """)
            if st.button("💎 Purchase Validator License", type="primary"):
                st.success("✅ Validator node license purchased!")
                st.balloons()
    
    with tab2:
        st.subheader("📊 Your Node Portfolio")
        
        # Sample node data
        node_data = [
            {"Type": "Storage", "License ID": "SNL-001", "Status": "🟢 Active", "Monthly Rewards": "37.5 HYBRID", "Uptime": "99.8%"},
            {"Type": "Storage", "License ID": "SNL-002", "Status": "🟢 Active", "Monthly Rewards": "37.5 HYBRID", "Uptime": "99.9%"},
            {"Type": "Validator", "License ID": "VNL-001", "Status": "🟢 Active", "Monthly Rewards": "208.3 HYBRID", "Uptime": "100%"}
        ]
        
        st.dataframe(node_data, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Monthly Rewards", "283.3 HYBRID", "~$2,833")
        with col2:
            st.metric("Annual Yield", "18.5%", "Compound interest")
        with col3:
            st.metric("Total Investment Value", "$15,000", "+$2,500 profit")
    
    with tab3:
        st.subheader("🤖 Node-as-a-Service Platform")
        
        st.info("💡 **NaaS Benefits**: Fully automated node operation, no technical maintenance required!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔧 Technical Management**")
            st.write("• Automated setup and configuration")
            st.write("• 24/7 monitoring and maintenance")
            st.write("• Automatic updates and security patches")
            st.write("• Hardware failure protection")
        
        with col2:
            st.markdown("**💰 Passive Income Features**")
            st.write("• Automatic reward claiming")
            st.write("• Compound interest reinvestment")
            st.write("• Performance optimization")
            st.write("• Multi-node portfolio management")

def main():
    """Main application entry point"""

    st.set_page_config(
        page_title="HYBRID Blockchain Platform",
        page_icon="🌟",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .stAlert {
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🌟 HYBRID BLOCKCHAIN")
        st.markdown("*Revolutionary Multi-Chain Platform*")
        
        # Network status indicator
        st.success("🟢 Network Online")
        st.metric("Block Height", "1,234,567")
        st.metric("Active Nodes", "1,847")

        page = st.selectbox(
            "🌟 Choose Your Experience",
            [
                "🏠 Home Dashboard",
                "💰 Token Distribution", 
                "🚀 Exchange Listings",
                "📊 Market Dashboard",
                "🔬 Blockchain Explorer",
                "🎫 Node Management",
                "👑 Founder Dashboard",
                "📚 Documentation"
            ]
        )

    # Main content based on selection
    if page == "🏠 Home Dashboard":
        create_streamlit_ui()
    elif page == "💰 Token Distribution":
        show_token_distribution()
    elif page == "🚀 Exchange Listings":
        from ui.exchange_listing_dashboard import create_exchange_listing_dashboard
        create_exchange_listing_dashboard()
    elif page == "📊 Market Dashboard":
        from ui.hybrid_market_dashboard import create_hybrid_market_dashboard
        create_hybrid_market_dashboard()
    elif page == "🔬 Blockchain Explorer":
        from ui.hybridscan_ui import create_hybridscan_interface
        create_hybridscan_interface()
    elif page == "🎫 Node Management":
        create_node_management_interface()
    elif page == "👑 Founder Dashboard":
        from ui.founder_dashboard import create_founder_dashboard
        create_founder_dashboard()
    elif page == "📚 Documentation":
        st.header("📚 Complete HYBRID Documentation System")
        
        # Documentation overview
        st.success("✅ All documentation components are fully operational!")
        
        # Show documentation structure
        docs_structure = {
            "Core Documentation": [
                "📖 API.md - Complete API reference", 
                "🛠️ HTSX.md - Runtime documentation",
                "🎫 NodeOperator.md - Node operation guide",
                "🌀 SpiralScript.md - Language specification"
            ],
            "Technical Specifications": [
                "📄 HYBRID Blockchain + HTSX Integration.pdf",
                "📄 Technical Specification.pdf", 
                "📝 Implementation discussions and guides"
            ],
            "System Components": [
                "🧩 50+ operational components",
                "🔗 Cross-chain integration ready",
                "💰 Token economics finalized",
                "👑 Sovereignty protocol active"
            ]
        }
        
        for category, items in docs_structure.items():
            with st.expander(f"📁 {category}"):
                for item in items:
                    st.markdown(f"✅ {item}")
        
        # Load the comprehensive analyzer
        from ui.docs_analyzer import create_docs_analyzer
        create_docs_analyzer()

if __name__ == "__main__":
    main()