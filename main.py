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
    # Import UI components with error handling
    from ui.docs_analyzer import DocsAnalyzer
    print("✅ UI components imported successfully")
except ImportError as e:
    print(f"⚠️ UI components not available: {e}")

try:
    # Import core blockchain modules
    from blockchain.hybrid_node import create_hybrid_node
    from blockchain.hybrid_wallet import hybrid_wallet_manager, get_founder_wallet
    from ui.streamlit_ui import create_streamlit_ui
    print("✅ Core blockchain modules imported successfully")
except Exception as e:
    st.error(f"❌ Core module error: {e}")
    print(f"❌ Core module error: {e}")

try:
    # Import convergence engine  
    from components.convergence_engine import ConvergenceEngine
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
        st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=HYBRID+BLOCKCHAIN", width=200)

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
    elif page == "👑 Founder Dashboard":
        from ui.founder_dashboard import create_founder_dashboard
        create_founder_dashboard()
    else:
        st.write(f"Page {page} coming soon!")

if __name__ == "__main__":
    main()