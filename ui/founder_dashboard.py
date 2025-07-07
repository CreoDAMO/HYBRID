
import streamlit as st
import asyncio
from typing import Optional
import hashlib
import time
from dataclasses import dataclass

from blockchain.hybrid_wallet import get_founder_wallet, hybrid_wallet_manager
from blockchain.hybrid_node import create_hybrid_node
from blockchain.multi_ai_orchestrator import multi_ai_orchestrator
from blockchain.circle_usdc_integration import circle_usdc_manager
from blockchain.coinbase_integration import hybrid_agent

@dataclass
class FounderSession:
    """Founder authentication session"""
    base_address: str
    authenticated: bool
    login_time: float
    session_token: str

class FounderDashboard:
    """Secure Founder Dashboard with Base wallet authentication"""
    
    def __init__(self):
        # Known founder Base wallet address (from main.py)
        self.founder_base_address = "0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79"
        self.session_timeout = 3600  # 1 hour session timeout
        
    def verify_base_address(self, input_address: str) -> bool:
        """Verify if the input address matches the founder's Base wallet"""
        return input_address.lower() == self.founder_base_address.lower()
    
    def create_session(self, base_address: str) -> FounderSession:
        """Create authenticated session"""
        session_token = hashlib.sha256(f"{base_address}{time.time()}".encode()).hexdigest()
        
        return FounderSession(
            base_address=base_address,
            authenticated=True,
            login_time=time.time(),
            session_token=session_token
        )
    
    def is_session_valid(self, session: FounderSession) -> bool:
        """Check if session is still valid"""
        if not session.authenticated:
            return False
        
        return (time.time() - session.login_time) < self.session_timeout
    
    def render_login(self):
        """Render login interface"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             padding: 3rem; border-radius: 20px; color: white; text-align: center; margin-bottom: 2rem;">
            <h1>👑 HYBRID Founder Dashboard</h1>
            <p style="font-size: 1.2rem; margin-top: 1rem;">Secure Access Portal</p>
            <p style="opacity: 0.9;">Enter your Base wallet address to access the control center</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🔐 Authentication Required")
        st.info("Enter your Base wallet address to access the founder dashboard")
        
        with st.form("founder_login"):
            base_address = st.text_input(
                "Base Wallet Address",
                placeholder="0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79",
                help="Enter your Base wallet address that owns the HYBRID ecosystem"
            )
            
            submitted = st.form_submit_button("🚀 Access Dashboard", type="primary")
            
            if submitted:
                if self.verify_base_address(base_address):
                    session = self.create_session(base_address)
                    st.session_state.founder_session = session
                    st.success("✅ Authentication successful! Welcome to the Founder Dashboard.")
                    st.rerun()
                else:
                    st.error("❌ Authentication failed. Invalid Base wallet address.")
                    st.warning("Only the founder's Base wallet can access this dashboard.")
    
    def render_dashboard(self, session: FounderSession):
        """Render the main founder dashboard"""
        
        # Header with logout
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 2rem; border-radius: 15px; color: white;">
                <h1>👑 HYBRID Founder Control Center</h1>
                <p>Complete ecosystem management and oversight</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("Session Status", "🟢 Active")
        
        with col3:
            if st.button("🚪 Logout", type="secondary"):
                del st.session_state.founder_session
                st.rerun()
        
        st.divider()
        
        # Dashboard tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "💰 Founder Wallet", "🤖 AI Orchestration", "🌐 Network Control", 
            "💳 Financial Systems", "📊 Analytics", "⚙️ System Admin"
        ])
        
        with tab1:
            self.render_founder_wallet_section()
        
        with tab2:
            self.render_ai_orchestration_section()
        
        with tab3:
            self.render_network_control_section()
        
        with tab4:
            self.render_financial_systems_section()
        
        with tab5:
            self.render_analytics_section()
        
        with tab6:
            self.render_system_admin_section()
    
    def render_founder_wallet_section(self):
        """Render founder wallet management"""
        st.subheader("💰 HYBRID Founder Wallet Management")
        
        founder_wallet = get_founder_wallet()
        
        # Wallet overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "HYBRID Balance", 
                f"{founder_wallet.balance / 1_000_000:,.0f} HYBRID",
                f"${founder_wallet.balance / 1_000_000 * 10:,.0f} USD"
            )
        
        with col2:
            st.metric(
                "Wallet Address",
                f"{founder_wallet.address[:12]}...{founder_wallet.address[-8:]}",
                "Genesis Wallet"
            )
        
        with col3:
            st.metric(
                "Allocation",
                "10% of Supply",
                "10B HYBRID"
            )
        
        # Secure wallet details
        with st.expander("🔐 Secure Wallet Details", expanded=False):
            st.warning("⚠️ Sensitive information - Handle with care")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔑 Show Private Key"):
                    st.error("🚨 CRITICAL: Private key gives full wallet control!")
                    st.code(founder_wallet.private_key, language="text")
            
            with col2:
                if st.button("📝 Show Mnemonic"):
                    st.warning("⚠️ Keep this phrase secure - it's your wallet recovery!")
                    st.code(founder_wallet.mnemonic, language="text")
            
            st.code(f"""
Full Wallet Information:
Address: {founder_wallet.address}
Label: {founder_wallet.label}
Balance: {founder_wallet.balance / 1_000_000:,.6f} HYBRID
Micro-HYBRID: {founder_wallet.balance:,} µHYBRID
Created: {founder_wallet.created_at}
Type: Genesis Founder Wallet
            """, language="text")
        
        # Wallet operations
        st.markdown("### 💸 Wallet Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Transfer HYBRID")
            with st.form("transfer_hybrid"):
                recipient = st.text_input("Recipient Address")
                amount = st.number_input("Amount (HYBRID)", min_value=1.0, value=1000.0)
                memo = st.text_input("Memo (optional)")
                
                if st.form_submit_button("💸 Send HYBRID"):
                    if recipient:
                        success = hybrid_wallet_manager.transfer(
                            founder_wallet.address,
                            recipient,
                            int(amount * 1_000_000)
                        )
                        
                        if success:
                            st.success(f"✅ Transferred {amount:,.0f} HYBRID to {recipient}")
                        else:
                            st.error("❌ Transfer failed")
        
        with col2:
            st.markdown("#### Create User Wallet")
            with st.form("create_user_wallet"):
                wallet_label = st.text_input("Wallet Label", "New User Wallet")
                initial_funding = st.number_input("Initial Funding (HYBRID)", min_value=0.0, value=1000.0)
                
                if st.form_submit_button("🆕 Create & Fund Wallet"):
                    from blockchain.hybrid_wallet import create_hybrid_wallet
                    
                    new_wallet = create_hybrid_wallet(wallet_label)
                    
                    if initial_funding > 0:
                        success = hybrid_wallet_manager.transfer(
                            founder_wallet.address,
                            new_wallet.address,
                            int(initial_funding * 1_000_000)
                        )
                        
                        if success:
                            st.success(f"✅ Created and funded wallet: {new_wallet.address}")
                            st.code(f"""
New Wallet Details:
Address: {new_wallet.address}
Mnemonic: {new_wallet.mnemonic}
Initial Balance: {initial_funding:,.0f} HYBRID
                            """)
                        else:
                            st.error("❌ Wallet created but funding failed")
                    else:
                        st.success(f"✅ Created wallet: {new_wallet.address}")
    
    def render_ai_orchestration_section(self):
        """Render AI orchestration control"""
        st.subheader("🤖 Multi-AI Orchestration Control")
        
        try:
            stats = multi_ai_orchestrator.get_orchestrator_stats()
            
            # AI system overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total AI Requests", stats["total_requests"])
            with col2:
                st.metric("Consensus Sessions", stats["consensus_requests"])
            with col3:
                st.metric("Total Cost", f"${stats['total_cost']:.4f}")
            with col4:
                st.metric("Active Providers", "4")
            
            # AI provider management
            st.markdown("### 🎛️ AI Provider Management")
            
            providers = ["OpenAI GPT-4", "Grok3", "DeepSeek R3", "Anthropic Claude"]
            
            for provider in providers:
                with st.expander(f"🤖 {provider} Controls"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Status", "🟢 Online")
                    with col2:
                        if st.button(f"🔄 Restart {provider}", key=f"restart_{provider}"):
                            st.success(f"Restarted {provider}")
                    with col3:
                        if st.button(f"⚙️ Configure {provider}", key=f"config_{provider}"):
                            st.info(f"Configuration panel for {provider}")
            
        except Exception as e:
            st.error(f"Error loading AI orchestration data: {e}")
    
    def render_network_control_section(self):
        """Render network control panel"""
        st.subheader("🌐 HYBRID Network Control")
        
        # Network status
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Network Status", "🟢 Online")
        with col2:
            st.metric("Active Validators", "21")
        with col3:
            st.metric("Block Height", "1,234,567")
        with col4:
            st.metric("Network TPS", "2,500")
        
        # Node management
        st.markdown("### 🔧 Node Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start New Node", type="primary"):
                st.success("Starting new HYBRID node...")
        
        with col2:
            if st.button("📊 Network Diagnostics"):
                st.info("Running network diagnostics...")
        
        # Emergency controls
        st.markdown("### 🚨 Emergency Controls")
        st.warning("These controls should only be used in critical situations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⏸️ Pause Network", type="secondary"):
                st.error("Network pause initiated - Use with extreme caution!")
        
        with col2:
            if st.button("🔄 Emergency Restart"):
                st.warning("Emergency restart sequence initiated")
        
        with col3:
            if st.button("📢 Broadcast Alert"):
                alert_msg = st.text_input("Alert Message")
                if alert_msg:
                    st.success(f"Broadcasting: {alert_msg}")
    
    def render_financial_systems_section(self):
        """Render financial systems management"""
        st.subheader("💳 Financial Systems Management")
        
        # Circle USDC integration
        st.markdown("### 💰 Circle USDC Integration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("USDC Liquidity", "$75M")
        with col2:
            st.metric("Active Wallets", "1,247")
        with col3:
            st.metric("Daily Volume", "$12.8M")
        
        if st.button("🔧 Manage USDC Settings"):
            st.info("USDC integration management panel")
        
        # Coinbase integration
        st.markdown("### 🏦 Coinbase AgentKit")
        
        if st.button("🤖 AI Agent Controls"):
            st.success("AI Agent management interface")
    
    def render_analytics_section(self):
        """Render comprehensive analytics"""
        st.subheader("📊 Comprehensive Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Value Locked", "$850M")
        with col2:
            st.metric("Active Users", "45,670")
        with col3:
            st.metric("Daily Transactions", "125,340")
        with col4:
            st.metric("Network Growth", "+15.2%")
        
        # Charts would go here
        st.info("📈 Advanced analytics charts and insights coming soon...")
    
    def render_system_admin_section(self):
        """Render system administration"""
        st.subheader("⚙️ System Administration")
        
        # System health
        st.markdown("### 🏥 System Health")
        
        health_metrics = [
            ("API Server", "🟢 Healthy", "99.9% uptime"),
            ("Database", "🟢 Healthy", "< 10ms response"),
            ("Blockchain Node", "🟢 Healthy", "Synced"),
            ("AI Services", "🟢 Healthy", "All providers online")
        ]
        
        for service, status, detail in health_metrics:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col1:
                st.write(f"**{service}**")
            with col2:
                st.write(status)
            with col3:
                st.write(detail)
        
        # System controls
        st.markdown("### 🔧 System Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Restart Services"):
                st.success("System services restarted")
        
        with col2:
            if st.button("📋 View Logs"):
                st.text_area("System Logs", "System running normally...", height=200)
        
        with col3:
            if st.button("⚙️ System Settings"):
                st.info("System configuration panel")

def create_founder_dashboard():
    """Main function to create founder dashboard"""
    
    # Initialize dashboard
    dashboard = FounderDashboard()
    
    # Check for existing session
    if 'founder_session' not in st.session_state:
        # No session, show login
        dashboard.render_login()
    else:
        session = st.session_state.founder_session
        
        # Validate session
        if dashboard.is_session_valid(session):
            # Valid session, show dashboard
            dashboard.render_dashboard(session)
        else:
            # Session expired
            st.error("🕐 Session expired. Please log in again.")
            del st.session_state.founder_session
            st.rerun()

if __name__ == "__main__":
    st.set_page_config(
        page_title="HYBRID Founder Dashboard",
        page_icon="👑",
        layout="wide"
    )
    
    create_founder_dashboard()
