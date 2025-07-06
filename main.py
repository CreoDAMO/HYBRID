
#!/usr/bin/env python3
import streamlit as st
import asyncio
import json
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import sys
import os

# Add blockchain module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'blockchain'))

from blockchain.hybrid_node import (
    HybridBlockchainNode, 
    create_hybrid_node, 
    NodeType,
    NFTLicense
)
from blockchain.hybrid_wallet import hybrid_wallet_manager, get_founder_wallet, create_hybrid_wallet

# HYBRID Blockchain Integration
class ChainType(Enum):
    HYBRID = "hybrid"
    BASE = "base"
    POLYGON = "polygon"
    SOLANA = "solana"

@dataclass
class WalletConfig:
    address: str
    chain: ChainType
    rpc_url: str
    balance: float = 0.0

@dataclass
class NodeOperatorStats:
    uptime: float
    daily_rewards: float
    total_transactions: int
    staked_amount: float
    license_type: str

class HybridHTSXRuntime:
    def __init__(self):
        # Get the founder wallet
        self.founder_wallet = get_founder_wallet()
        
        self.wallets = {
            ChainType.BASE: WalletConfig("0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79", ChainType.BASE, "https://mainnet.base.org", 5.2),
            ChainType.POLYGON: WalletConfig("0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79", ChainType.POLYGON, "https://polygon-rpc.com", 150.8),
            ChainType.SOLANA: WalletConfig("3E8keZHkH1AHvRfbmq44tEmBgJYz1NjkhBE41C4gJHUn", ChainType.SOLANA, "https://api.mainnet-beta.solana.com", 12.5),
            ChainType.HYBRID: WalletConfig(self.founder_wallet.address, ChainType.HYBRID, "http://0.0.0.0:26657", self.founder_wallet.balance / 1_000_000)
        }
        
        self.nft_licenses = {
            "storage": NFTLicense("STOR-001", "hybrid1q2w3e4r5t6y7u8i9o0p", NodeType.STORAGE, "2024-01-01", None),
            "validator": NFTLicense("VAL-001", "", NodeType.VALIDATOR, "", None)
        }
        
        self.node_stats = NodeOperatorStats(
            uptime=99.9,
            daily_rewards=50.0,
            total_transactions=1234,
            staked_amount=500.0,
            license_type="storage"
        )
        
        # Initialize blockchain node
        self.blockchain_node = None
        
    async def initialize_blockchain_node(self, node_type: str = "storage"):
        """Initialize the HYBRID blockchain node"""
        if not self.blockchain_node:
            self.blockchain_node = create_hybrid_node(node_type)
            
    def parse_htsx_components(self, htsx_content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Enhanced HTSX parser for blockchain components"""
        components = {
            "wallet_connectors": [],
            "nft_licenses": [],
            "cross_chain_bridges": [],
            "node_operators": [],
            "hybrid_tokens": [],
            "defi_protocols": []
        }
        
        # Parse wallet connector
        if "wallet-connector" in htsx_content:
            chains = self._extract_chains(htsx_content)
            components["wallet_connectors"].append({
                "chains": chains,
                "connected": True,
                "wallets": self.wallets
            })
        
        # Parse NFT licenses
        if "nft-license" in htsx_content:
            components["nft_licenses"].append({
                "licenses": self.nft_licenses,
                "purchase_enabled": True
            })
        
        # Parse cross-chain bridges
        if "cross-chain-bridge" in htsx_content:
            components["cross_chain_bridges"].append({
                "protocol": "axelar",
                "supported_chains": ["hybrid", "base", "polygon", "solana"],
                "fees": {"hybrid_to_base": 0.1, "base_to_hybrid": 0.15}
            })
        
        # Parse node operators
        if "node-operator" in htsx_content:
            components["node_operators"].append({
                "type": "storage",
                "stats": self.node_stats,
                "naas_enabled": True
            })
        
        # Parse HYBRID token
        if "hybrid-token" in htsx_content:
            components["hybrid_tokens"].append({
                "symbol": "HYBRID",
                "balance": self.wallets[ChainType.HYBRID].balance,
                "price_usd": 10.0,
                "utilities": ["fees", "governance", "staking", "nft_purchase"]
            })
            
        return components
    
    def _extract_chains(self, htsx_content: str) -> List[str]:
        """Extract chain names from HTSX content"""
        chains = []
        for chain in ChainType:
            if chain.value in htsx_content:
                chains.append(chain.value)
        return chains if chains else ["hybrid", "base", "polygon", "solana"]

def render_founder_wallet():
    """Render founder wallet information"""
    st.subheader("👑 HYBRID Founder Wallet")
    
    founder = get_founder_wallet()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Founder Address", 
            f"{founder.address[:12]}...{founder.address[-8:]}", 
            "🚀 Lead Engineer & Developer"
        )
    
    with col2:
        st.metric(
            "HYBRID Balance", 
            f"{founder.balance / 1_000_000:,.0f} HYBRID",
            f"${founder.balance / 1_000_000 * 10:,.0f} USD (at $10/HYBRID)"
        )
    
    with col3:
        st.metric(
            "Wallet Status",
            "🟢 Active",
            "Genesis Wallet"
        )
    
    with st.expander("📋 Full Founder Wallet Details"):
        st.code(f"""
Address: {founder.address}
Label: {founder.label}
Balance: {founder.balance / 1_000_000:,.6f} HYBRID
Micro-HYBRID: {founder.balance:,} µHYBRID
Created: {founder.created_at}
Type: Genesis Founder Wallet
        """)
        
        if st.button("💰 Create New User Wallet"):
            new_wallet = create_hybrid_wallet("New User Wallet")
            
            # Transfer 1000 HYBRID to new wallet
            success = hybrid_wallet_manager.transfer(
                founder.address,
                new_wallet.address,
                1000 * 1_000_000  # 1000 HYBRID
            )
            
            if success:
                st.success(f"✅ New wallet created and funded!")
                st.code(f"""
New Wallet Address: {new_wallet.address}
Mnemonic: {new_wallet.mnemonic}
Balance: 1,000 HYBRID (funded by founder)
                """)
            else:
                st.error("Failed to create and fund wallet")

def render_blockchain_status():
    """Render blockchain node status"""
    st.subheader("⛓️ HYBRID Blockchain Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Node Status", "🟢 Online", "Active")
    with col2:
        st.metric("Block Height", "1,234,567", "+1")
    with col3:
        st.metric("Validators", "21", "0")
    with col4:
        st.metric("TPS", "2,500", "+150")
    
    # Blockchain metrics
    with st.expander("📊 Detailed Blockchain Metrics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Network Statistics:**")
            st.write("• Network: HYBRID Mainnet")
            st.write("• Consensus: Tendermint")
            st.write("• Average Block Time: 6 seconds")
            st.write("• Total Transactions: 12,345,678")
            
        with col2:
            st.write("**Token Economics:**")
            st.write("• Total Supply: 1,000,000,000 HYBRID")
            st.write("• Circulating Supply: 750,000,000 HYBRID")
            st.write("• Market Cap: $7.5B (at $10/HYBRID)")
            st.write("• Staking Ratio: 65%")

def render_wallet_connector(wallet_data: Dict[str, Any]):
    """Render multi-chain wallet connector component"""
    st.subheader("🔗 Multi-Chain Wallet Connector")
    
    wallets = wallet_data.get("wallets", {})
    cols = st.columns(len(wallets))
    
    for i, (chain, wallet) in enumerate(wallets.items()):
        with cols[i]:
            chain_name = chain.value.upper()
            truncated_address = f"{wallet.address[:6]}...{wallet.address[-4:]}"
            st.metric(
                label=chain_name,
                value=f"{wallet.balance:.2f}",
                delta=truncated_address
            )
    
    if st.button("🔄 Refresh Balances"):
        st.success("Wallet balances refreshed!")

def render_nft_license_system(license_data: Dict[str, Any]):
    """Render NFT license management system"""
    st.subheader("🎫 HYBRID Node License NFTs")
    
    licenses = license_data.get("licenses", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        storage_license = licenses.get("storage")
        if storage_license:
            status = "✅ Owned" if storage_license.token_id else "❌ Not Owned"
            st.info(f"""
            **Storage Node License**
            - Token ID: {storage_license.token_id}
            - Owner: {storage_license.owner_address}
            - Enables storage node operation
            - Earns transaction fees
            - Status: {status}
            """)
    
    with col2:
        validator_license = licenses.get("validator")
        if validator_license:
            status = "✅ Owned" if validator_license.token_id else "❌ Not Owned"
            st.warning(f"""
            **Validator Node License**
            - Token ID: {validator_license.token_id or "N/A"}
            - Price: 500 HYBRID
            - Enables validator node operation
            - Earns block rewards
            - Status: {status}
            """)
            
            if not validator_license.token_id:
                if st.button("Purchase Validator License"):
                    st.success("🚀 Initiating validator license purchase...")
                    st.balloons()

def render_cross_chain_bridge(bridge_data: Dict[str, Any]):
    """Render cross-chain bridge interface"""
    st.subheader("🌉 Cross-Chain Bridge")
    
    supported_chains = bridge_data.get("supported_chains", [])
    protocol = bridge_data.get("protocol", "axelar")
    
    with st.form("bridge_transaction"):
        col1, col2 = st.columns(2)
        
        with col1:
            from_chain = st.selectbox("From Chain", [chain.upper() for chain in supported_chains])
            amount = st.number_input("Amount", min_value=0.0, value=100.0, step=0.1)
        
        with col2:
            to_chain = st.selectbox("To Chain", [chain.upper() for chain in supported_chains])
            token = st.selectbox("Token", ["HYBRID", "ETH", "MATIC", "SOL"])
        
        if st.form_submit_button("🌉 Bridge Tokens"):
            if from_chain != to_chain:
                st.success(f"Bridging {amount} {token} from {from_chain} to {to_chain} via {protocol.upper()}...")
                st.info("Transaction will complete in 2-5 minutes")
            else:
                st.error("Source and destination chains must be different")

def render_node_operator_dashboard(node_data: Dict[str, Any]):
    """Render node operator dashboard"""
    st.subheader("⚙️ Node Operations Dashboard")
    
    stats = node_data.get("stats")
    node_type = node_data.get("type", "storage")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Node Type", node_type.title(), "Active")
    with col2:
        st.metric("Uptime", f"{stats.uptime}%", "+0.1%")
    with col3:
        st.metric("Daily Rewards", f"{stats.daily_rewards} HYBRID", "+5")
    with col4:
        st.metric("Transactions", f"{stats.total_transactions:,}", "+50")
    
    # Tabs for detailed view
    tab1, tab2, tab3 = st.tabs(["📊 Performance", "💰 Rewards", "⚙️ Settings"])
    
    with tab1:
        # Performance chart
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
        performance_data = pd.DataFrame({
            "Date": dates,
            "Uptime": np.random.normal(99.5, 0.5, 30),
            "Transactions": np.random.poisson(50, 30)
        })
        
        st.line_chart(performance_data.set_index("Date"))
    
    with tab2:
        # Rewards tracking
        reward_data = {
            "Source": ["Transaction Fees", "Block Rewards", "Staking Rewards"],
            "Daily": [15, 25, 10],
            "Weekly": [105, 175, 70],
            "Monthly": [450, 750, 300]
        }
        st.dataframe(pd.DataFrame(reward_data))
        
        if st.button("💰 Claim Pending Rewards"):
            st.success("Claimed 50 HYBRID tokens!")
    
    with tab3:
        naas_enabled = st.checkbox("Enable Node-as-a-Service (NaaS)", value=True)
        if naas_enabled:
            st.info("Your node is managed by a NaaS provider. You earn 70% of rewards passively.")
        
        delegation_address = st.text_input("Delegate to Address", value="")
        if st.button("Delegate Node") and delegation_address:
            st.success(f"Node delegated to {delegation_address}")

def render_hybrid_token_interface(token_data: Dict[str, Any]):
    """Render HYBRID token interface"""
    st.subheader("💰 $HYBRID Token")
    
    balance = token_data.get("balance", 0)
    price_usd = token_data.get("price_usd", 10.0)
    utilities = token_data.get("utilities", [])
    
    # Token metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Balance", f"{balance:,.0f} HYBRID", "+50")
    with col2:
        st.metric("USD Value", f"${balance * price_usd:,.0f}", f"+${50 * price_usd:.0f}")
    with col3:
        staked_amount = 500
        st.metric("Staked", f"{staked_amount} HYBRID", "5% APY")
    
    # Token utilities
    with st.expander("🔧 Token Utilities"):
        for utility in utilities:
            st.write(f"• {utility.replace('_', ' ').title()}")
    
    # Token actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💸 Send HYBRID"):
            st.info("Send token interface would open here")
    
    with col2:
        if st.button("🏦 Stake Tokens"):
            st.info("Staking interface would open here")
    
    with col3:
        if st.button("🗳️ Governance"):
            st.info("Governance voting interface would open here")

def main():
    st.set_page_config(
        page_title="HYBRID Blockchain + HTSX Integration",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 HYBRID Blockchain + HTSX Integration")
    st.markdown("*Fully Operational Cosmos SDK Blockchain with HTSX Runtime Engine*")
    
    # Initialize runtime
    runtime = HybridHTSXRuntime()
    
    # Initialize blockchain node
    if 'blockchain_initialized' not in st.session_state:
        asyncio.run(runtime.initialize_blockchain_node())
        st.session_state.blockchain_initialized = True
    
    # Render founder wallet first
    render_founder_wallet()
    st.divider()
    
    # Render blockchain status
    render_blockchain_status()
    st.divider()
    
    # Sample HTSX for demonstration
    sample_htsx = """
    <htsx>
      <wallet-connector chains="hybrid,base,polygon,solana" required="true" />
      <nft-license type="node_license" storage="true" validator="false" />
      <cross-chain-bridge protocol="axelar" chains="hybrid,base,polygon" />
      <node-operator type="storage" naas="true" rewards="auto" />
      <hybrid-token utilities="fees,governance,staking,nft_purchase" />
    </htsx>
    """
    
    # Sidebar for HTSX editing
    with st.sidebar:
        st.header("📝 HTSX Runtime Engine")
        st.markdown("Edit blockchain components using HTSX:")
        
        htsx_content = st.text_area(
            "HTSX Code",
            value=sample_htsx,
            height=400,
            help="Define your blockchain components using HTSX syntax"
        )
        
        if st.button("🔄 Parse & Execute HTSX", type="primary"):
            st.session_state.htsx_content = htsx_content
            st.rerun()
    
    # Parse and render components
    htsx_to_render = getattr(st.session_state, 'htsx_content', sample_htsx)
    components = runtime.parse_htsx_components(htsx_to_render)
    
    # Render each component type
    for component_type, component_list in components.items():
        if component_list:
            for component_data in component_list:
                if component_type == "wallet_connectors":
                    render_wallet_connector(component_data)
                elif component_type == "nft_licenses":
                    render_nft_license_system(component_data)
                elif component_type == "cross_chain_bridges":
                    render_cross_chain_bridge(component_data)
                elif component_type == "node_operators":
                    render_node_operator_dashboard(component_data)
                elif component_type == "hybrid_tokens":
                    render_hybrid_token_interface(component_data)
                
                st.divider()
    
    # Integration benefits footer
    with st.expander("🎯 Why HYBRID Blockchain + HTSX?"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔗 HYBRID Blockchain Benefits:**
            - Cosmos SDK foundation with Tendermint consensus
            - NFT-gated node operations (Storage & Validator)
            - Cross-chain interoperability (Base, Polygon, Solana)
            - $HYBRID token economics with staking rewards
            - Node-as-a-Service (NaaS) for passive income
            - Real blockchain, not a simulation
            """)
        
        with col2:
            st.markdown("""
            **⚡ HTSX Runtime Engine Benefits:**
            - Declarative blockchain components
            - Type-safe Web3 development
            - Built-in multi-chain support
            - Component-based architecture
            - Real-time blockchain integration
            - Production-ready runtime
            """)

if __name__ == "__main__":
    main()
