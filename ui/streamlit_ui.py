
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def create_hybrid_dashboard():
    """Create the main HYBRID + HTSX dashboard"""
    
    st.header("📊 HYBRID Blockchain Analytics")
    
    # Generate sample data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    # Network metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active Nodes",
            value="1,234",
            delta="12"
        )
    
    with col2:
        st.metric(
            label="Total $HYBRID Staked",
            value="10.5M",
            delta="2.3%"
        )
    
    with col3:
        st.metric(
            label="Cross-Chain Txns",
            value="45,678",
            delta="8.7%"
        )
    
    with col4:
        st.metric(
            label="NFT Licenses Sold",
            value="567",
            delta="15"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Network Growth")
        growth_data = pd.DataFrame({
            'Date': dates,
            'Nodes': np.cumsum(np.random.randint(5, 20, len(dates))) + 1000,
            'Transactions': np.cumsum(np.random.randint(100, 500, len(dates))) + 10000
        })
        
        fig = px.line(growth_data, x='Date', y=['Nodes', 'Transactions'], 
                     title="Network Metrics Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Token Distribution")
        token_data = pd.DataFrame({
            'Category': ['Staking', 'Node Rewards', 'Cross-Chain', 'Governance', 'Treasury'],
            'Amount': [35, 25, 20, 10, 10]
        })
        
        fig = px.pie(token_data, values='Amount', names='Category',
                    title="$HYBRID Token Allocation")
        st.plotly_chart(fig, use_container_width=True)

def create_htsx_playground():
    """Create HTSX code playground"""
    
    st.header("🛠️ HTSX Playground")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("HTSX Code")
        
        default_code = """<htsx>
  <html>
    <head>
      <title>My HYBRID dApp</title>
    </head>
    <body>
      <wallet-connector 
        chains="hybrid,base,polygon"
        required="true"
      />
      
      <nft-license 
        type="storage"
        price="100"
        currency="HYBRID"
      />
      
      <node-dashboard 
        type="storage"
        rewards="daily"
      />
      
      <cross-chain-bridge 
        from="hybrid"
        to="base"
        token="HYBRID"
      />
      
      <script lang="hybrid">
        type NodeStats = {
          uptime: number;
          rewards: number;
          transactions: number;
        };
        
        class NodeOperator {
          stats: NodeStats = {
            uptime: 99.9,
            rewards: 50,
            transactions: 1234
          };
          
          async claimRewards() {
            const tx = await hybridChain.sendTransaction({
              to: this.address,
              amount: this.stats.rewards,
              token: "HYBRID"
            });
            return tx;
          }
          
          render() {
            return (
              <div className="node-operator">
                <h2>Node Statistics</h2>
                <p>Uptime: {this.stats.uptime}%</p>
                <p>Rewards: {this.stats.rewards} HYBRID</p>
                <button onClick={() => this.claimRewards()}>
                  Claim Rewards
                </button>
              </div>
            );
          }
        }
      </script>
    </body>
  </html>
</htsx>"""
        
        htsx_code = st.text_area(
            "Enter your HTSX code:",
            value=default_code,
            height=500,
            help="Write HTSX code with blockchain components"
        )
    
    with col2:
        st.subheader("Live Preview")
        
        if st.button("🚀 Compile & Preview"):
            st.success("✅ HTSX compiled successfully!")
            
            # Simulate component rendering
            st.markdown("### Rendered Components:")
            
            with st.container():
                st.info("🔗 **Wallet Connector**: Connected to HYBRID, Base, Polygon")
                
                st.warning("🎫 **NFT License**: Storage Node License - 100 HYBRID")
                if st.button("Purchase License"):
                    st.success("License purchased! Transaction: 0x1234...")
                
                st.success("📊 **Node Dashboard**: Storage Node Active")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Uptime", "99.9%")
                with col_b:
                    st.metric("Rewards", "50 HYBRID")
                with col_c:
                    st.metric("Transactions", "1,234")
                
                st.info("🌉 **Cross-Chain Bridge**: HYBRID → Base ready")

def create_integration_docs():
    """Create integration documentation"""
    
    st.header("📚 Integration Documentation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Components", "API", "Examples"])
    
    with tab1:
        st.markdown("""
        ## HYBRID + HTSX Integration
        
        The integration of HYBRID Blockchain with HTSX creates a powerful ecosystem that solves key Web3 development challenges:
        
        ### Problems Solved:
        1. **Complex Web3 Development** → Declarative HTSX components
        2. **Node Operation Barriers** → NFT-gated licensing with UI
        3. **Cross-Chain Complexity** → Unified multi-chain interface
        4. **Poor Developer Experience** → Type-safe blockchain development
        
        ### Key Features:
        - 🔗 Multi-chain wallet connections (Base, Polygon, Solana, HYBRID)
        - 🎫 NFT-based node licensing system
        - 🌉 Cross-chain token bridging
        - ⚙️ Simplified node operations
        - 💰 Integrated $HYBRID token utilities
        """)
    
    with tab2:
        st.markdown("""
        ## HTSX Components for HYBRID
        
        ### Core Components:
        
        ```htsx
        <!-- Multi-chain wallet connector -->
        <wallet-connector 
          chains="hybrid,base,polygon,solana"
          required="true"
        />
        
        <!-- NFT license management -->
        <nft-license 
          type="storage|validator"
          price="100"
          currency="HYBRID"
        />
        
        <!-- Node operations dashboard -->
        <node-operator 
          type="storage|validator"
          naas="true"
        />
        
        <!-- Cross-chain bridge -->
        <cross-chain-bridge 
          protocol="axelar"
          chains="hybrid,base,polygon"
        />
        
        <!-- HYBRID token utilities -->
        <hybrid-token 
          utilities="fees,governance,staking"
        />
        ```
        """)
    
    with tab3:
        st.markdown("""
        ## API Reference
        
        ### Wallet Connector API
        ```typescript
        interface WalletConnector {
          connect(chain: ChainType): Promise<string>;
          getBalance(token: string): Promise<number>;
          sendTransaction(tx: Transaction): Promise<string>;
        }
        ```
        
        ### NFT License API
        ```typescript
        interface NFTLicense {
          purchase(type: 'storage' | 'validator'): Promise<string>;
          verify(address: string, nftId: string): Promise<boolean>;
          delegate(operator: string): Promise<void>;
        }
        ```
        
        ### Node Operator API
        ```typescript
        interface NodeOperator {
          start(config: NodeConfig): Promise<void>;
          getStats(): Promise<NodeStats>;
          claimRewards(): Promise<string>;
        }
        ```
        """)
    
    with tab4:
        st.markdown("""
        ## Usage Examples
        
        ### 1. Basic HYBRID dApp
        ```htsx
        <htsx>
          <wallet-connector chains="hybrid" />
          <hybrid-token balance="1000" />
        </htsx>
        ```
        
        ### 2. Node Operator Dashboard
        ```htsx
        <htsx>
          <nft-license type="storage" required="true" />
          <node-operator type="storage" naas="true" />
        </htsx>
        ```
        
        ### 3. Cross-Chain Application
        ```htsx
        <htsx>
          <wallet-connector chains="hybrid,base,polygon" />
          <cross-chain-bridge protocol="axelar" />
        </htsx>
        ```
        """)

def main():
    st.set_page_config(
        page_title="HYBRID + HTSX Integration",
        page_icon="🚀",
        layout="wide"
    )
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🚀 HYBRID + HTSX")
        
        page = st.selectbox(
            "Choose a page:",
            ["Dashboard", "HTSX Playground", "Documentation"]
        )
    
    # Main content
    if page == "Dashboard":
        create_hybrid_dashboard()
    elif page == "HTSX Playground":
        create_htsx_playground()
    elif page == "Documentation":
        create_integration_docs()

if __name__ == "__main__":
    main()
