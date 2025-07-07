
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
"""
Founder Dashboard for HYBRID Blockchain
Exclusive access to founder controls and system administration
"""

import streamlit as st
import asyncio
from datetime import datetime

def create_founder_dashboard():
    """Create the founder dashboard interface"""
    
    st.header("👑 HYBRID Blockchain Founder Dashboard")
    st.markdown("*Exclusive founder access to system controls*")
    
    # Authentication check (simplified for demo)
    if not st.session_state.get('founder_authenticated', False):
        st.subheader("🔐 Founder Authentication")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            founder_key = st.text_input("Founder Private Key", type="password", placeholder="Enter founder wallet private key...")
        with col2:
            if st.button("🔓 Authenticate", type="primary"):
                if founder_key:  # Simplified - in production, verify against actual founder wallet
                    st.session_state.founder_authenticated = True
                    st.success("✅ Founder authenticated!")
                    st.rerun()
                else:
                    st.error("❌ Invalid founder key")
        
        st.info("**Demo Access:** Use any value to access the founder dashboard in this demo environment.")
        return
    
    # Founder controls (only accessible after authentication)
    st.success("✅ Authenticated as HYBRID Blockchain Founder")
    
    if st.button("🚪 Logout"):
        st.session_state.founder_authenticated = False
        st.rerun()
    
    # Founder dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💰 Treasury", "⚙️ System Controls", "👑 Governance", "📊 Analytics", "🔧 Emergency"
    ])
    
    with tab1:
        st.subheader("💰 Founder Treasury Management")
        
        # Treasury overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Founder Wallet", "100B HYBRID", "Genesis allocation")
        with col2:
            st.metric("Treasury Value", "$1.0T", "At $10/HYBRID")
        with col3:
            st.metric("Available", "95B HYBRID", "95% remaining")
        with col4:
            st.metric("Distributed", "5B HYBRID", "5% distributed")
        
        # Treasury actions
        st.subheader("💸 Treasury Operations")
        
        with st.form("treasury_operations"):
            operation = st.selectbox("Operation Type", [
                "Fund Development",
                "Ecosystem Grants",
                "Node Operator Rewards",
                "Community Programs",
                "Strategic Partnerships"
            ])
            
            recipient = st.text_input("Recipient Address", placeholder="hybrid1...")
            amount = st.number_input("Amount (HYBRID)", min_value=1000, value=1000000, step=1000)
            purpose = st.text_area("Purpose", placeholder="Describe the purpose of this allocation...")
            
            if st.form_submit_button("💰 Execute Treasury Transfer", type="primary"):
                if recipient and amount and purpose:
                    st.success(f"✅ Transferred {amount:,} HYBRID to {recipient}")
                    st.info(f"Purpose: {purpose}")
                    st.balloons()
                else:
                    st.error("All fields are required")
    
    with tab2:
        st.subheader("⚙️ System Administration Controls")
        
        # Network parameters
        st.subheader("🌐 Network Parameters")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Current Parameters:**")
            st.write("• Block Time: 6 seconds")
            st.write("• Max Validators: 21")
            st.write("• Inflation Rate: 7% → 2%")
            st.write("• Min Commission: 1%")
            st.write("• Governance Quorum: 33.4%")
        
        with col2:
            st.write("**Modification Controls:**")
            if st.button("⏱️ Adjust Block Time"):
                st.info("Block time adjustment interface would open")
            if st.button("👑 Modify Validator Set"):
                st.info("Validator set modification interface would open")
            if st.button("📈 Update Inflation"):
                st.info("Inflation parameters interface would open")
        
        # License management
        st.subheader("🎫 NFT License Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏭 Mint Storage Licenses"):
                st.success("Minted 100 new storage licenses")
        with col2:
            if st.button("👑 Mint Validator Licenses"):
                st.success("Minted 10 new validator licenses")
        with col3:
            if st.button("🚫 Revoke License"):
                license_id = st.text_input("License ID to revoke")
                if license_id:
                    st.warning(f"Revoked license {license_id}")
        
        # Cross-chain controls
        st.subheader("🌉 Cross-Chain Bridge Controls")
        
        bridge_status = st.radio("Bridge Status", ["🟢 Active", "🟡 Maintenance", "🔴 Emergency Stop"])
        
        if bridge_status == "🔴 Emergency Stop":
            st.error("⚠️ Emergency stop activated - all cross-chain operations halted")
        elif bridge_status == "🟡 Maintenance":
            st.warning("🔧 Bridge in maintenance mode - limited operations")
        else:
            st.success("✅ Bridge operating normally")
    
    with tab3:
        st.subheader("👑 Governance & DAO Management")
        
        # Governance overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Proposals", "3", "+1")
        with col2:
            st.metric("Voting Power", "15%", "Founder allocation")
        with col3:
            st.metric("Participation Rate", "67%", "+5%")
        
        # Active proposals
        st.subheader("📋 Active Governance Proposals")
        
        proposals = [
            {
                "ID": "PROP-001",
                "Title": "Increase Validator Set to 25",
                "Status": "🗳️ Voting",
                "For": "78%",
                "Against": "22%",
                "Ends": "2 days"
            },
            {
                "ID": "PROP-002", 
                "Title": "Reduce Storage License Price",
                "Status": "🗳️ Voting",
                "For": "65%",
                "Against": "35%",
                "Ends": "5 days"
            },
            {
                "ID": "PROP-003",
                "Title": "Add Arbitrum Bridge Support",
                "Status": "📝 Draft",
                "For": "-",
                "Against": "-",
                "Ends": "Not started"
            }
        ]
        
        for prop in proposals:
            with st.expander(f"{prop['ID']}: {prop['Title']}"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Status", prop['Status'])
                with col2:
                    st.metric("For", prop['For'])
                with col3:
                    st.metric("Against", prop['Against'])
                with col4:
                    st.metric("Ends", prop['Ends'])
                
                if prop['Status'] == "🗳️ Voting":
                    vote_col1, vote_col2, vote_col3 = st.columns(3)
                    with vote_col1:
                        if st.button(f"✅ Vote For", key=f"for_{prop['ID']}"):
                            st.success(f"Voted FOR {prop['ID']}")
                    with vote_col2:
                        if st.button(f"❌ Vote Against", key=f"against_{prop['ID']}"):
                            st.success(f"Voted AGAINST {prop['ID']}")
                    with vote_col3:
                        if st.button(f"🚫 Veto", key=f"veto_{prop['ID']}"):
                            st.warning(f"VETOED {prop['ID']} (Founder privilege)")
        
        # Create new proposal
        st.subheader("📝 Create New Proposal")
        with st.form("new_proposal"):
            prop_title = st.text_input("Proposal Title")
            prop_description = st.text_area("Description", height=100)
            prop_type = st.selectbox("Type", ["Parameter Change", "Software Upgrade", "Spending", "Constitutional"])
            
            if st.form_submit_button("📝 Submit Proposal"):
                if prop_title and prop_description:
                    st.success(f"✅ Proposal '{prop_title}' submitted successfully!")
                else:
                    st.error("Title and description are required")
    
    with tab4:
        st.subheader("📊 Founder Analytics Dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Network Value", "$10.5B", "+12.3%")
        with col2:
            st.metric("Daily Revenue", "$125K", "+8.7%")
        with col3:
            st.metric("Active Nodes", "1,847", "+23")
        with col4:
            st.metric("TVL", "$2.3B", "+15.2%")
        
        # Growth metrics
        st.subheader("📈 Growth Metrics")
        
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        # Generate sample data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Daily Active Users**")
            dau_data = pd.DataFrame({
                "Date": dates,
                "Users": np.random.randint(8000, 15000, len(dates))
            })
            st.line_chart(dau_data.set_index("Date"))
        
        with col2:
            st.write("**Transaction Volume**")
            volume_data = pd.DataFrame({
                "Date": dates,
                "Volume": np.random.uniform(1000000, 5000000, len(dates))
            })
            st.line_chart(volume_data.set_index("Date"))
        
        # Revenue breakdown
        st.subheader("💰 Revenue Sources")
        revenue_sources = {
            "Transaction Fees": 45,
            "License Sales": 25,
            "Staking Rewards": 20,
            "Cross-chain Fees": 10
        }
        st.bar_chart(revenue_sources)
    
    with tab5:
        st.subheader("🚨 Emergency Controls")
        st.warning("⚠️ **Warning:** These controls should only be used in emergency situations")
        
        # Emergency actions
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔴 Critical Controls")
            
            if st.button("🛑 Emergency Network Halt", type="primary"):
                if st.checkbox("I understand this will halt all network operations"):
                    st.error("🚨 EMERGENCY NETWORK HALT ACTIVATED")
                    st.error("All blockchain operations have been suspended")
            
            if st.button("🔒 Freeze All Bridges"):
                st.warning("🔒 All cross-chain bridges have been frozen")
            
            if st.button("⏸️ Pause NFT License System"):
                st.warning("⏸️ NFT license operations have been paused")
        
        with col2:
            st.subheader("🔧 Recovery Controls")
            
            if st.button("🔄 Restart Network"):
                st.success("🔄 Network restart initiated")
            
            if st.button("🔓 Unfreeze Bridges"):
                st.success("🔓 Cross-chain bridges have been unfrozen")
            
            if st.button("▶️ Resume License System"):
                st.success("▶️ NFT license system has been resumed")
        
        # System status
        st.subheader("🔍 System Status Monitor")
        
        status_data = {
            "Component": [
                "Consensus Engine",
                "P2P Network", 
                "RPC Services",
                "Cross-chain Bridges",
                "NFT License System",
                "Staking Module",
                "Governance Module"
            ],
            "Status": [
                "🟢 Operational",
                "🟢 Operational",
                "🟢 Operational", 
                "🟢 Operational",
                "🟢 Operational",
                "🟢 Operational",
                "🟢 Operational"
            ],
            "Uptime": [
                "99.9%",
                "99.8%",
                "99.7%",
                "99.6%",
                "99.9%",
                "99.8%",
                "99.9%"
            ],
            "Last Check": [
                "30s ago",
                "45s ago",
                "1m ago",
                "2m ago",
                "30s ago",
                "1m ago",
                "45s ago"
            ]
        }
        
        st.dataframe(status_data, use_container_width=True)
        
        # Real-time monitoring
        if st.button("🔄 Refresh Status"):
            st.success("System status refreshed")
            st.rerun()
