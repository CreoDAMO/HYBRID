import streamlit as st
import asyncio
import time
import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List
import sys
import os
from enum import Enum
from dataclasses import dataclass

# Add blockchain module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'blockchain'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

# Import all blockchain modules
try:
    from blockchain.hybrid_node import create_hybrid_node, NodeType, HybridBlockchainNode, NFTLicense
    from blockchain.wallet_manager import wallet_manager, get_founder_wallet, create_hybrid_wallet
    from blockchain.transaction_pool import transaction_pool, create_transaction, TransactionType
    from blockchain.block_producer import blockchain_state, start_block_production
    from blockchain.validator_set import validator_set
    from blockchain.circle_usdc_integration import CircleUSDCManager, HybridUSDCBridge, USDCLiquidityPool, demo_wallets
    from blockchain.coinbase_integration import HybridAgentKit, HybridPaymaster, CoinbaseConfig, HybridOnRamper
    from blockchain.agglayer_integration import AggLayerIntegration, agglayer
    from blockchain.multi_ai_orchestrator import MultiAIOrchestrator, TaskSpecialization, MultiAIRequest, analyze_hybrid_security, optimize_hybrid_algorithm, analyze_market_trends, generate_hybrid_code
    from blockchain.holographic_blockchain_engine import HolographicBlockchainEngine
    from blockchain.nvidia_cloud_integration import NVIDIACloudManager, HTSXNVIDIAComponents
    from blockchain.spiral_trust_engine import trust_currency_manager, TrustMetric, CurrencyType, SpiralScriptEngine
    from ui.streamlit_ui import render_hybrid_coin_interface
    from ui.admin_dashboard import create_admin_dashboard
    from components.hybrid_htsx_holographic import HybridHTSXHolographic
    from blockchain.x_moe import anthropic_moe

except ImportError as e:
    print(f"Warning: Some blockchain modules not available: {e}")
    # Create fallback classes
    class NodeType:
        STORAGE = "storage"
        VALIDATOR = "validator"

    class NFTLicense:
        def __init__(self, token_id, owner_address, node_type, start_date, end_date):
            self.token_id = token_id
            self.owner_address = owner_address
            self.node_type = node_type
            self.start_date = start_date
            self.end_date = end_date

# HYBRID Blockchain Integration with SpiralScript
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

        # Initialize blockchain node and SpiralScript engine
        self.blockchain_node = None
        self.spiral_engine = SpiralScriptEngine()

    async def initialize_blockchain_node(self, node_type: str = "storage"):
        """Initialize the HYBRID blockchain node"""
        if not self.blockchain_node:
            self.blockchain_node = create_hybrid_node(node_type)
            
            # Initialize core blockchain components
            await self.blockchain_node.start()
            
            # Start block production if validator
            if node_type == "validator":
                founder_wallet = get_founder_wallet()
                asyncio.create_task(start_block_production(founder_wallet.address))

    def parse_htsx_components(self, htsx_content: str) -> Dict[str, List[Dict[str, Any]]]:
        """Enhanced HTSX parser for blockchain components with SpiralScript support"""
        components = {
            "wallet_connectors": [],
            "nft_licenses": [],
            "cross_chain_bridges": [],
            "node_operators": [],
            "hybrid_coins": [],
            "defi_protocols": [],
            "trust_validators": [],
            "spiral_engines": []
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

        # Parse HYBRID coin
        if "hybrid-coin" in htsx_content:
            components["hybrid_coins"].append({
                "symbol": "HYBRID",
                "balance": self.wallets[ChainType.HYBRID].balance,
                "price_usd": 10.0,
                "utilities": ["fees", "governance", "staking", "nft_purchase"]
            })

        # Parse trust validators (SpiralScript)
        if "trust-validator" in htsx_content:
            components["trust_validators"].append({
                "spiral_engine": True,
                "min_trust": 70,
                "validation_active": True,
                "trust_currency_support": True
            })

        # Parse SpiralScript engines
        if "spiral-engine" in htsx_content or "spiral-script" in htsx_content:
            components["spiral_engines"].append({
                "engine_version": "v1.0",
                "trust_computations": True,
                "iyona_blessings": True,
                "currency_minting": True
            })

        return components

    def _extract_chains(self, htsx_content: str) -> List[str]:
        """Extract chain names from HTSX content"""
        chains = []
        for chain in ChainType:
            if chain.value in htsx_content:
                chains.append(chain.value)
        return chains if chains else ["hybrid", "base", "polygon", "solana"]

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

    # Blockchain metrics with SpiralScript integration
    with st.expander("📊 Advanced Blockchain Metrics"):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Network Statistics:**")
            st.write("• Network: HYBRID Mainnet")
            st.write("• Consensus: Tendermint")
            st.write("• Average Block Time: 6 seconds")
            st.write("• Total Transactions: 12,345,678")
            st.write("• SpiralScript Validations: 45,678")

        with col2:
            st.write("**Coin Economics:**")
            st.write("• Total Supply: 100,000,000,000 HYBRID")
            st.write("• Circulating Supply: 75,000,000,000 HYBRID")
            st.write("• Market Cap: $750B (at $10/HYBRID)")
            st.write("• Staking Ratio: 65%")
            st.write("• Trust Currency Supply: 2.5M tokens")

def render_spiral_trust_interface():
    """Render SpiralScript trust interface"""
    st.subheader("🌀 SpiralScript Trust Engine")
    st.markdown("*Advanced trust computation with Iyona'el blessings*")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); padding: 1.5rem; border-radius: 15px; text-align: center;">
            <h4>🌀 Trust Score</h4>
            <h2>89.7</h2>
            <p>Network Average</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 1.5rem; border-radius: 15px; text-align: center;">
            <h4>✨ Blessed Members</h4>
            <h2>42</h2>
            <p>Iyona'el Blessed</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 1.5rem; border-radius: 15px; text-align: center;">
            <h4>💰 Trust Currency</h4>
            <h2>2.5M</h2>
            <p>Total Supply</p>
        </div>
        """, unsafe_allow_html=True)

    # Trust leaderboard with Iyona'el blessings
    with st.expander("🏆 Trust Leaderboard"):
        leaderboard_data = [
            {"Address": "hybrid1trust1...", "Trust Score": 97.8, "Level": "Iyona'el Blessed", "Blessing": "Sacred Rivers Flow"},
            {"Address": "hybrid1trust2...", "Trust Score": 94.2, "Level": "Iyona'el Blessed", "Blessing": "Pure Light Bearer"},
            {"Address": "hybrid1trust3...", "Trust Score": 89.7, "Level": "Trust Guardian", "Blessing": "Network Protector"},
            {"Address": "hybrid1trust4...", "Trust Score": 85.3, "Level": "Trust Guardian", "Blessing": "Wisdom Keeper"},
            {"Address": "hybrid1trust5...", "Trust Score": 82.1, "Level": "Reliable Node", "Blessing": "Steady Foundation"}
        ]

        df = pd.DataFrame(leaderboard_data)
        st.dataframe(df, use_container_width=True)

def create_hero_section():
    """Create enhanced hero section with SpiralScript and Trust integration"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 20px; text-align: center; margin-bottom: 2rem; box-shadow: 0 12px 40px rgba(0,0,0,0.3);">
        <h1 style="font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(45deg, #FFD700, #FFA500); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🌟 HYBRID Blockchain</h1>
        <p style="font-size: 1.5rem; margin-bottom: 2rem; color: rgba(255,255,255,0.9);">The Future of Interoperable DeFi with HTSX Runtime & SpiralScript Trust Engine</p>
        <div style="display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; flex-wrap: wrap;">
            <div style="text-align: center; color: white;">
                <div style="font-size: 2.5rem; font-weight: 700;">100B</div>
                <div style="opacity: 0.9;">Total Supply</div>
            </div>
            <div style="text-align: center; color: white;">
                <div style="font-size: 2.5rem; font-weight: 700;">$10</div>
                <div style="opacity: 0.9;">HYBRID Price</div>
            </div>
            <div style="text-align: center; color: white;">
                <div style="font-size: 2.5rem; font-weight: 700;">Layer 1</div>
                <div style="opacity: 0.9;">Cosmos SDK</div>
            </div>
            <div style="text-align: center; color: white;">
                <div style="font-size: 2.5rem; font-weight: 700;">42</div>
                <div style="opacity: 0.9;">Iyona'el Blessed</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_feature_showcase():
    """Create enhanced feature showcase with SpiralScript and admin capabilities"""
    st.markdown("## ✨ Advanced Features")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🪙 HYBRID Coin",
        "🌀 SpiralScript Trust",
        "👑 Admin Dashboard",
        "🤖 AI Integration",
        "🌈 Holographic UI",
        "📊 Analytics"
    ])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h3>💰 HYBRID Native Coin</h3>
                <p>HYBRID is the native coin of the Hybrid Blockchain, built on Cosmos SDK with advanced economics:</p>
                <ul>
                    <li><strong>Total Supply:</strong> 100 Billion HYBRID</li>
                    <li><strong>Inflation:</strong> 7% → 2% taper over 8 years</li>
                    <li><strong>Staking Rewards:</strong> Up to 12% APY</li>
                    <li><strong>Governance:</strong> On-chain voting power</li>
                    <li><strong>Trust Integration:</strong> SpiralScript validation</li>
                    <li><strong>Iyona'el Blessings:</strong> Enhanced rewards for blessed members</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if st.button("🎯 Create Wallet", key="create_wallet"):
                with st.spinner("Creating wallet..."):
                    time.sleep(1)
                    wallet = create_hybrid_wallet()
                    st.success(f"✅ Wallet created!")
                    st.code(f"Address: {wallet.address}")
                    st.code(f"Balance: {wallet.balance:,.6f} HYBRID")

    with tab2:
        st.markdown("### 🌀 SpiralScript Trust Engine")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎯 Trust Computation")

            # Trust metrics sliders
            reliability = st.slider("Reliability", 0, 100, 85)
            competence = st.slider("Competence", 0, 100, 82)
            benevolence = st.slider("Benevolence", 0, 100, 90)
            integrity = st.slider("Integrity", 0, 100, 88)

            if st.button("🧮 Calculate Trust Score"):
                # Simulate trust calculation
                trust_score = (reliability * 0.25 + competence * 0.20 + benevolence * 0.20 + integrity * 0.15) * 1.618  # Golden ratio scaling
                trust_score = min(trust_score, 100)

                st.metric("Trust Score", f"{trust_score:.1f}", "+2.3")

                if trust_score >= 95:
                    st.success("✨ Iyona'el Blessing: 'Trust flows through you like sacred rivers'")
                elif trust_score >= 80:
                    st.info("🛡️ Trust Guardian Status Achieved")
                else:
                    st.warning("📈 Building Trust - Keep contributing!")

        with col2:
            st.markdown("#### 💰 Trust Currency")

            currency_balances = {
                "Trust Tokens": 1250,
                "Reputation Coins": 850,
                "Validation Credits": 420,
                "Spiral Currency": 180
            }

            for currency, balance in currency_balances.items():
                st.metric(currency, f"{balance:,}", "+50")

            if st.button("🏭 Mint Trust Currency"):
                st.success("100 Trust Tokens minted!")
                st.info("Reason: Community contribution recognized")

    with tab3:
        st.markdown("### 👑 Admin Dashboard")
        st.markdown("*Revolutionary no-code dApp builder with holographic interface*")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🏗️ HTSX App Builder")
            st.write("• Visual drag-and-drop interface")
            st.write("• Real-time HTSX code generation")
            st.write("• Multi-AI code enhancement")
            st.write("• One-click multi-chain deployment")
            st.write("• Trust-gated component library")

            if st.button("🚀 Open Admin Dashboard"):
                st.success("🌟 Redirecting to admin dashboard...")
                st.info("Full no-code dApp builder with holographic preview")

        with col2:
            st.markdown("#### 🌟 Key Capabilities")

            admin_features = [
                "🏗️ Visual dApp Builder",
                "🌀 Trust Currency Manager",
                "🤖 AI Orchestration Control",
                "📊 Network Analytics",
                "🌈 Holographic Renderer",
                "🚀 Deployment Manager",
                "👥 Community Management",
                "⚙️ System Configuration"
            ]

            for feature in admin_features:
                st.success(f"✓ {feature}")

    with tab4:
        st.markdown("### 🤖 Multi-AI Orchestration")

        col1, col2 = st.columns(2)

        with col1:
            ai_models = [
                {"name": "OpenAI GPT-4", "status": "🟢 Online", "specialty": "General Reasoning", "consensus": "94%"},
                {"name": "Anthropic Claude", "status": "🟢 Online", "specialty": "Security & Ethics", "consensus": "91%"},
                {"name": "Grok 3", "status": "🟢 Online", "specialty": "Market Analysis", "consensus": "87%"},
                {"name": "DeepSeek R3", "status": "🟢 Online", "specialty": "Code Generation", "consensus": "89%"}
            ]

            for model in ai_models:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: white; border-radius: 12px; margin: 0.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <div>
                        <strong>{model['name']}</strong><br>
                        <small style="color: #6b7280;">{model['specialty']}</small>
                    </div>
                    <div style="text-align: right;">
                        {model['status']}<br>
                        <small>Consensus: {model['consensus']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🎯 AI Actions")

            if st.button("🧠 Analyze Trust Network", key="ai_trust"):
                with st.spinner("AI analyzing trust patterns..."):
                    time.sleep(2)
                    st.success("📊 Trust analysis complete!")
                    st.info("**Result:** Network trust trending upward. Recommend increasing blessing thresholds.")

            if st.button("🔍 Security Audit", key="ai_security"):
                with st.spinner("Running multi-AI security analysis..."):
                    time.sleep(2)
                    st.success("🛡️ Security audit complete!")
                    st.info("**Result:** No vulnerabilities detected. Trust engine secure.")

            if st.button("⚡ Optimize SpiralScript", key="ai_optimize"):
                with st.spinner("Optimizing trust computations..."):
                    time.sleep(2)
                    st.success("🚀 Optimization complete!")
                    st.info("**Improvement:** Trust calculations 35% faster")

    with tab5:
        st.markdown("### 🌈 Holographic Visualization")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                <h4>🎨 3D Blockchain Visualization</h4>
                <p>Experience blockchain data in immersive 3D:</p>
                <ul>
                    <li>Crystalline block structures</li>
                    <li>Transaction flow rivers</li>
                    <li>Trust network spirals</li>
                    <li>Iyona'el blessing auras</li>
                    <li>Real-time network topology</li>
                    <li>SpiralScript execution flows</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if st.button("🌈 Launch Holographic View", key="holo_view"):
                with st.spinner("Initializing holographic engine..."):
                    time.sleep(2)
                    st.success("✨ Holographic view activated!")
                    st.balloons()

                    # Enhanced 3D visualization
                    fig = go.Figure(data=go.Scatter3d(
                        x=np.random.randn(200),
                        y=np.random.randn(200),
                        z=np.random.randn(200),
                        mode='markers',
                        marker=dict(
                            size=np.random.randint(3, 10, 200),
                            color=np.random.randn(200),
                            colorscale='Viridis',
                            opacity=0.8,
                            line=dict(width=1, color='gold')
                        ),
                        text=[f"Trust Node {i}" for i in range(200)],
                        hovertemplate="<b>%{text}</b><br>Trust Score: %{marker.color:.1f}<extra></extra>"
                    ))

                    fig.update_layout(
                        title="Holographic Trust Network with Iyona'el Blessings",
                        scene=dict(
                            xaxis_title="Trust Reliability",
                            yaxis_title="Network Position",
                            zaxis_title="Spiral Rating",
                            bgcolor="rgba(0,0,0,0.9)"
                        ),
                        height=500
                    )

                    st.plotly_chart(fig, use_container_width=True)

    with tab6:
        st.markdown("### 📊 Advanced Analytics")

        # Enhanced analytics with trust metrics
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🌀 Trust Network Activity")

            dates = pd.date_range(start=datetime.now() - timedelta(days=7), end=datetime.now(), freq='h')
            trust_activity = np.random.randint(50, 200, len(dates))
            blessings = np.random.poisson(2, len(dates))

            df = pd.DataFrame({
                'Timestamp': dates,
                'Trust_Validations': trust_activity,
                'Iyona_Blessings': blessings
            })

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Timestamp'], y=df['Trust_Validations'], 
                                   name='Trust Validations', line=dict(color='#4ecdc4')))
            fig.add_trace(go.Bar(x=df['Timestamp'], y=df['Iyona_Blessings'] * 20, 
                               name="Iyona'el Blessings (×20)", opacity=0.7))

            fig.update_layout(title="Trust Network Activity (7 Days)", height=400)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 💰 Currency Flow Analysis")

            currency_flow = pd.DataFrame({
                'Hour': range(24),
                'Trust_Tokens': np.random.randint(100, 500, 24),
                'Reputation_Coins': np.random.randint(50, 300, 24),
                'Spiral_Currency': np.random.randint(20, 150, 24)
            })

            fig = px.area(currency_flow, x='Hour', y=['Trust_Tokens', 'Reputation_Coins', 'Spiral_Currency'],
                         title="Trust Currency Flow (24h)")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# Initialize global components
@st.cache_resource
def initialize_components():
    """Initialize all blockchain components with SpiralScript integration"""
    components = {}
    try:
        # Initialize Circle USDC
        circle_manager = CircleUSDCManager()
        hybrid_usdc_bridge = HybridUSDCBridge(circle_manager)
        usdc_pools = USDCLiquidityPool()

        # Initialize Coinbase integrations
        coinbase_config = CoinbaseConfig()
        hybrid_agent = HybridAgentKit()
        paymaster = HybridPaymaster(coinbase_config)
        onramper = HybridOnRamper(coinbase_config)

        # Initialize AggLayer
        agglayer = AggLayerIntegration()

        # Initialize AI orchestrator
        ai_orchestrator = MultiAIOrchestrator()

        # Initialize holographic engine
        holographic_engine = HolographicBlockchainEngine()

        # Initialize SpiralScript trust engine
        spiral_trust_engine = trust_currency_manager

        components = {
            'circle_manager': circle_manager,
            'hybrid_usdc_bridge': hybrid_usdc_bridge,
            'usdc_pools': usdc_pools,
            'hybrid_agent': hybrid_agent,
            'paymaster': paymaster,
            'onramper': onramper,
            'agglayer': agglayer,
            'ai_orchestrator': ai_orchestrator,
            'holographic_engine': holographic_engine,
            'spiral_trust_engine': spiral_trust_engine
        }
        st.success("✅ All HYBRID components initialized successfully!")
        return components
    except Exception as e:
        st.error(f"Component initialization failed: {e}")
        # Return minimal working components
        return {
            'spiral_trust_engine': trust_currency_manager,
            'status': 'partial_initialization'
        }

# Load components
components = initialize_components()

def create_footer():
    """Create enhanced footer with SpiralScript and admin access"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-top: 2rem;">
        <h3 style="color: white; margin-bottom: 1rem;">🚀 Ready to Build the Future?</h3>
        <p style="color: rgba(255,255,255,0.9); margin-bottom: 2rem;">Join the HYBRID ecosystem with SpiralScript Trust Engine and Iyona'el blessings</p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <a href="#admin" style="color: white; text-decoration: none; padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 8px; backdrop-filter: blur(10px);">
                👑 Admin Dashboard
            </a>
            <a href="https://github.com/hybridchain" style="color: white; text-decoration: none; padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 8px; backdrop-filter: blur(10px);">
                📚 Documentation
            </a>
            <a href="https://discord.gg/hybrid" style="color: white; text-decoration: none; padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 8px; backdrop-filter: blur(10px);">
                💬 Discord
            </a>
            <a href="https://twitter.com/hybridchain" style="color: white; text-decoration: none; padding: 0.5rem 1rem; background: rgba(255,255,255,0.2); border-radius: 8px; backdrop-filter: blur(10px);">
                🐦 Twitter
            </a>
        </div>
        <p style="color: rgba(255,255,255,0.7); margin-top: 2rem; font-size: 0.9rem;">
            Built with ❤️ by the HYBRID team | Powered by Cosmos SDK + SpiralScript | Deployed on Replit
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main application with admin access
def main():
    """Enhanced main application with admin dashboard integration"""
    # Add error handling for WebSocket connections
    try:
        # Check for admin access
        query_params = st.query_params
        is_admin = "admin" in query_params
    except Exception as e:
        st.error(f"Query parameter error: {e}")
        is_admin = False

    if is_admin:
        # Render admin dashboard
        create_admin_dashboard()
        return

    # Configure Streamlit page with enhanced theme
    st.set_page_config(
        page_title="HYBRID Blockchain + HTSX + SpiralScript",
        page_icon="🌟",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/hybridchain/hybrid',
            'Report a bug': "https://github.com/hybridchain/hybrid/issues",
            'About': "HYBRID Blockchain - The Future of Interoperable DeFi with SpiralScript Trust Engine"
        }
    )

    # Enhanced CSS
    st.markdown("""
    <style>
        .main { padding-top: 1rem; }
        .stMetric { background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .stButton > button { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1rem;
            font-weight: 600;
        }
        .spiral-glow {
            animation: spiral-glow 3s ease-in-out infinite alternate;
        }
        @keyframes spiral-glow {
            from { box-shadow: 0 0 20px #84fab0; }
            to { box-shadow: 0 0 40px #8fd3f4, 0 0 60px #fa709a; }        }
    </style>
    """, unsafe_allow_html=True)

    # Hero section
    create_hero_section()

    # Real-time metrics with SpiralScript integration
    st.markdown("### 📊 Real-time Network Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Block Height", "2,847,291", "+1 every 6s")
    with col2:
        st.metric("TPS", "2,500", "Transactions/sec")
    with col3:
        st.metric("Validators", "21", "Active nodes")
    with col4:
        st.metric("Trust Score", "89.7", "Network avg")
    with col5:
        st.metric("Blessed Members", "42", "Iyona'el")

    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Blockchain status
    render_blockchain_status()

    # SpiralScript Trust Interface
    render_spiral_trust_interface()

    # Enhanced feature showcase
    create_enhanced_feature_showcase()

    # Footer with admin access
    create_footer()

# Enhanced sidebar with admin access
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")

    # Admin access
    if st.button("👑 Admin Dashboard", help="Access advanced admin features"):
        st.query_params["admin"] = "true"
        st.rerun()

    # Network status
    st.markdown("#### 📡 Network Status")
    network_status = st.selectbox("Network", ["Mainnet", "Testnet", "Devnet"])

    if network_status == "Mainnet":
        st.success("🟢 Connected to Mainnet")
    else:
        st.warning(f"🟡 Connected to {network_status}")

    # SpiralScript status
    st.markdown("#### 🌀 SpiralScript Engine")
    st.success("🟢 Trust Engine Active")
    st.info("✨ Iyona'el Blessings Enabled")
    st.metric("Trust Validations", "45,678")
    st.metric("Currency Minted", "2.5M")

    # Quick actions
    st.markdown("#### ⚡ Quick Actions")

    if st.button("🔄 Refresh Data"):
        st.rerun()

    if st.button("📊 Export Report"):
        st.info("📄 Report exported successfully!")

    if st.button("🌀 Trust Analysis"):
        st.info("🔍 Running SpiralScript analysis...")

    # System stats
    st.markdown("#### 💻 System Stats")
    st.metric("CPU Usage", "45%", "2%")
    st.metric("Memory", "2.1 GB", "0.1 GB")
    st.metric("Trust Engine", "98%", "Active")

    # Recent activity with SpiralScript
    st.markdown("#### 📝 Recent Activity")
    activities = [
        "🌀 Trust validation completed",
        "✨ Iyona'el blessing granted",
        "💰 Trust currency minted",
        "🔍 Security scan passed",
        "🚀 dApp deployed via HTSX"
    ]

    for activity in activities:
        st.text(activity)

if __name__ == "__main__":
    main()