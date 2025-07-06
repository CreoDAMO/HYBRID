
"""
HybridScan UI - Advanced Blockchain Explorer Interface
Modern UI/UX with AR/VR integration for virtual worlds
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import asyncio
import json

from blockchain.hybridscan import HybridScan, VirtualWorldData
from blockchain.hybrid_node import create_hybrid_node

def create_hybridscan_interface():
    """Create the main HybridScan interface"""
    
    # Initialize HybridScan
    if 'hybridscan' not in st.session_state:
        node = create_hybrid_node("storage")
        st.session_state.hybridscan = HybridScan(node)
    
    hybridscan = st.session_state.hybridscan
    
    # Custom CSS for modern UI
    st.markdown("""
    <style>
    .hybridscan-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 0.5rem 0;
    }
    .block-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
    }
    .tx-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
    }
    .vr-world-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    .ar-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        color: white;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .ar-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="hybridscan-header">
        <h1>🔍 HybridScan Explorer</h1>
        <p>Advanced Blockchain Analytics with AR/VR Integration</p>
        <p>Explore the HYBRID blockchain in immersive virtual worlds</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Dashboard", "🔍 Explorer", "🌐 Virtual Worlds", 
        "🥽 AR/VR Experience", "📊 Analytics", "🔧 Tools"
    ])
    
    with tab1:
        render_dashboard(hybridscan)
    
    with tab2:
        render_blockchain_explorer(hybridscan)
    
    with tab3:
        render_virtual_worlds(hybridscan)
    
    with tab4:
        render_ar_vr_experience(hybridscan)
    
    with tab5:
        render_advanced_analytics(hybridscan)
    
    with tab6:
        render_developer_tools(hybridscan)

def render_dashboard(hybridscan):
    """Render the main dashboard"""
    st.subheader("📊 Network Overview")
    
    # Get dashboard data
    dashboard_data = asyncio.run(hybridscan.get_explorer_dashboard())
    network_stats = dashboard_data["network_stats"]
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🔗 Total Blocks",
            f"{network_stats['total_blocks']:,}",
            delta=f"+{np.random.randint(1, 5)}"
        )
    
    with col2:
        st.metric(
            "💸 Total Transactions",
            f"{network_stats['total_transactions']:,}",
            delta=f"+{np.random.randint(50, 200)}"
        )
    
    with col3:
        st.metric(
            "⚡ Current TPS",
            f"{network_stats['current_tps']:,}",
            delta=f"{np.random.randint(-100, 200)}"
        )
    
    with col4:
        st.metric(
            "🏛️ Active Validators",
            f"{network_stats['active_validators']}",
            delta="0"
        )
    
    with col5:
        st.metric(
            "🌍 Virtual Worlds",
            f"{len(dashboard_data['virtual_worlds'])}",
            delta=f"+{np.random.randint(0, 2)}"
        )
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Network Activity")
        
        # Generate sample data for chart
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        activity_data = pd.DataFrame({
            'Date': dates,
            'Transactions': np.random.poisson(15000, len(dates)),
            'Active Addresses': np.random.poisson(5000, len(dates)),
            'Block Production': np.random.poisson(14400, len(dates))  # ~1 block per 6 seconds
        })
        
        fig = px.line(activity_data, x='Date', y=['Transactions', 'Active Addresses'], 
                     title="Daily Network Activity")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Token Economics")
        
        token_data = pd.DataFrame({
            'Category': ['Staking', 'Liquidity Pools', 'Treasury', 'Circulation', 'Burned'],
            'Amount': [65, 20, 10, 4, 1],
            'Value_USD': [48.75, 15, 7.5, 3, 0.75]
        })
        
        fig = px.pie(token_data, values='Amount', names='Category',
                    title="HYBRID Token Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Latest blocks and transactions
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔗 Latest Blocks")
        latest_blocks = dashboard_data["latest_blocks"][:5]
        
        for block in latest_blocks:
            st.markdown(f"""
            <div class="block-card">
                <strong>Block #{block.height}</strong><br>
                <small>{block.hash[:16]}...{block.hash[-8:]}</small><br>
                <small>{len(block.transactions)} transactions • {block.size_bytes:,} bytes</small>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💸 Recent Transactions")
        recent_txs = dashboard_data["recent_transactions"][-5:]
        
        for tx in recent_txs:
            amount_hybrid = tx.amount / 1_000_000
            st.markdown(f"""
            <div class="tx-card">
                <strong>{amount_hybrid:.2f} HYBRID</strong><br>
                <small>{tx.tx_hash[:16]}...{tx.tx_hash[-8:]}</small><br>
                <small>{tx.from_address[:12]}... → {tx.to_address[:12]}...</small>
            </div>
            """, unsafe_allow_html=True)

def render_blockchain_explorer(hybridscan):
    """Render blockchain explorer interface"""
    st.subheader("🔍 Blockchain Explorer")
    
    # Search interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 Search",
            placeholder="Enter block height, transaction hash, or address...",
            help="Search for blocks, transactions, or addresses"
        )
    
    with col2:
        if st.button("🔍 Search", type="primary"):
            if search_query:
                results = asyncio.run(hybridscan.search_blockchain(search_query))
                st.session_state.search_results = results
    
    # Display search results
    if hasattr(st.session_state, 'search_results'):
        results = st.session_state.search_results
        
        if results['blocks']:
            st.subheader("📦 Blocks Found")
            for block in results['blocks']:
                with st.expander(f"Block #{block.height}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Hash:** {block.hash}")
                        st.write(f"**Proposer:** {block.proposer}")
                        st.write(f"**Timestamp:** {block.timestamp}")
                    with col2:
                        st.write(f"**Transactions:** {len(block.transactions)}")
                        st.write(f"**Gas Used:** {block.gas_used:,}")
                        st.write(f"**Size:** {block.size_bytes:,} bytes")
        
        if results['transactions']:
            st.subheader("💸 Transactions Found")
            for tx in results['transactions']:
                with st.expander(f"Transaction {tx.tx_hash[:16]}..."):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Amount:** {tx.amount / 1_000_000:.6f} HYBRID")
                        st.write(f"**From:** {tx.from_address}")
                        st.write(f"**To:** {tx.to_address}")
                    with col2:
                        st.write(f"**Block:** #{tx.block_height}")
                        st.write(f"**Fee:** {tx.fee / 1_000_000:.6f} HYBRID")
                        st.write(f"**Status:** {tx.status}")
        
        if results['addresses']:
            st.subheader("👤 Addresses Found")
            for addr in results['addresses']:
                with st.expander(f"Address {addr.address[:16]}..."):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Balance:** {addr.balance / 1_000_000:,.2f} HYBRID")
                        st.write(f"**Transactions:** {addr.transaction_count:,}")
                        st.write(f"**Type:** {'Contract' if addr.is_contract else 'EOA'}")
                    with col2:
                        st.write(f"**First Seen:** {addr.first_seen}")
                        st.write(f"**Validator:** {'Yes' if addr.is_validator else 'No'}")
                        st.write(f"**NFT Licenses:** {len(addr.nft_licenses)}")
    
    # Recent activity
    st.subheader("⚡ Live Activity")
    
    # Auto-refresh latest data
    if st.button("🔄 Refresh Data"):
        latest_blocks = asyncio.run(hybridscan.get_latest_blocks(20))
        
        # Display in a more detailed format
        blocks_df = pd.DataFrame([
            {
                "Height": block.height,
                "Hash": f"{block.hash[:16]}...",
                "Proposer": f"{block.proposer[:16]}...",
                "Transactions": len(block.transactions),
                "Gas Used": f"{block.gas_used:,}",
                "Size (bytes)": f"{block.size_bytes:,}"
            }
            for block in latest_blocks
        ])
        
        st.dataframe(blocks_df, use_container_width=True)

def render_virtual_worlds(hybridscan):
    """Render virtual worlds interface"""
    st.subheader("🌐 HYBRID Virtual Worlds")
    st.write("Explore blockchain data in immersive virtual environments")
    
    # Get virtual worlds data
    virtual_worlds = asyncio.run(hybridscan.get_virtual_worlds())
    
    # World selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        world_options = {world.name: world.world_id for world in virtual_worlds}
        selected_world_name = st.selectbox("🌍 Select Virtual World", list(world_options.keys()))
        selected_world_id = world_options[selected_world_name]
    
    with col2:
        if st.button("🚀 Enter Virtual World", type="primary"):
            st.session_state.active_world = selected_world_id
            st.success(f"Entering {selected_world_name}...")
    
    # Display virtual worlds
    for world in virtual_worlds:
        st.markdown(f"""
        <div class="vr-world-card">
            <h3>🌍 {world.name}</h3>
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <p><strong>Creator:</strong> {world.creator_address[:20]}...</p>
                    <p><strong>Land Plots:</strong> {world.land_plots:,}</p>
                    <p><strong>Active Users:</strong> {world.active_users:,}</p>
                </div>
                <div>
                    <p><strong>Economic Activity:</strong> ${world.economic_activity:,.0f}</p>
                    <p><strong>VR Ready:</strong> {'✅ Yes' if world.vr_ready else '❌ No'}</p>
                    <p><strong>NFT Assets:</strong> {len(world.nft_assets)}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # World details
        with st.expander(f"🔍 Explore {world.name}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**📊 Statistics**")
                st.metric("Active Users", world.active_users, f"+{np.random.randint(5, 25)}")
                st.metric("Land Plots", f"{world.land_plots:,}", "0")
                st.metric("Economic Activity", f"${world.economic_activity:,.0f}", f"+${np.random.randint(1000, 5000)}")
            
            with col2:
                st.write("**🎨 NFT Assets**")
                for asset in world.nft_assets:
                    st.write(f"• {asset['type'].title()}: {asset['count']:,}")
            
            with col3:
                st.write("**🎮 Actions**")
                if st.button(f"🥽 VR View", key=f"vr_{world.world_id}"):
                    st.info("Launching VR experience...")
                if st.button(f"📱 AR View", key=f"ar_{world.world_id}"):
                    st.info("Starting AR visualization...")
                if st.button(f"🏗️ Build Mode", key=f"build_{world.world_id}"):
                    st.info("Entering build mode...")
    
    # Create new world
    st.subheader("🏗️ Create New Virtual World")
    
    with st.expander("➕ Create Virtual World"):
        col1, col2 = st.columns(2)
        
        with col1:
            world_name = st.text_input("🏷️ World Name", "My HYBRID World")
            land_plots = st.number_input("🏞️ Land Plots", min_value=100, max_value=50000, value=1000)
            vr_ready = st.checkbox("🥽 VR Ready", value=True)
        
        with col2:
            world_type = st.selectbox("🌍 World Type", ["Trading Floor", "NFT Gallery", "Social Hub", "Gaming Arena"])
            coordinates_x = st.number_input("📍 X Coordinate", value=0.0)
            coordinates_z = st.number_input("📍 Z Coordinate", value=0.0)
        
        if st.button("🚀 Create World", type="primary"):
            world_config = {
                "name": world_name,
                "land_plots": land_plots,
                "vr_ready": vr_ready,
                "coordinates": {"x": coordinates_x, "y": 0, "z": coordinates_z},
                "type": world_type
            }
            
            creator_address = "hybrid1creator123"  # Would be from connected wallet
            world_id = asyncio.run(hybridscan.create_virtual_world(creator_address, world_config))
            
            st.success(f"✅ Virtual world '{world_name}' created with ID: {world_id}")
            st.balloons()

def render_ar_vr_experience(hybridscan):
    """Render AR/VR experience interface"""
    st.subheader("🥽 AR/VR Blockchain Experience")
    st.write("Immersive blockchain visualization and interaction")
    
    # AR/VR status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🥽 VR Sessions", hybridscan.ar_vr_features["active_vr_sessions"], "+2")
    with col2:
        st.metric("🌍 Virtual Worlds", hybridscan.ar_vr_features["virtual_worlds_count"], "+1")
    with col3:
        st.metric("📱 AR Visualizations", len(hybridscan.ar_vr_features["ar_visualizations"]), "0")
    
    # Platform support
    st.subheader("📱 Supported Platforms")
    platforms = hybridscan.ar_vr_features["supported_platforms"]
    
    cols = st.columns(len(platforms))
    for i, platform in enumerate(platforms):
        with cols[i]:
            st.info(f"✅ {platform}")
    
    # AR Visualizations
    st.subheader("📱 AR Visualizations")
    
    viz_options = hybridscan.ar_vr_features["ar_visualizations"]
    selected_viz = st.selectbox("🎨 Choose Visualization", viz_options)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate AR visualization data
        ar_data = asyncio.run(hybridscan.get_ar_visualization_data(selected_viz))
        
        if selected_viz == "Transaction Flow":
            st.write("**💸 Live Transaction Flow**")
            st.write("Visualize real-time transaction flow between addresses in 3D space")
            
            # Create network graph
            fig = go.Figure()
            
            for edge in ar_data["edges"]:
                fig.add_trace(go.Scatter3d(
                    x=[0, edge["value"]/1000],
                    y=[0, np.random.uniform(-5, 5)],
                    z=[0, np.random.uniform(-5, 5)],
                    mode='lines',
                    line=dict(color='cyan', width=edge["value"]/500),
                    showlegend=False
                ))
            
            fig.update_layout(
                title="3D Transaction Flow",
                scene=dict(
                    xaxis_title="Transaction Volume",
                    yaxis_title="Network Position Y",
                    zaxis_title="Network Position Z"
                ),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif selected_viz == "Network Topology":
            st.write("**🌐 Network Topology**")
            st.write("Explore validator connections and network structure in 3D")
            
            # Create 3D network topology
            validators = ar_data["validators"]
            
            fig = go.Figure()
            
            # Add validator nodes
            fig.add_trace(go.Scatter3d(
                x=[v["position"]["x"] for v in validators],
                y=[v["position"]["y"] for v in validators],
                z=[v["position"]["z"] for v in validators],
                mode='markers',
                marker=dict(
                    size=[v["stake"]/500000 for v in validators],
                    color=[v["stake"] for v in validators],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=[f"Validator {v['id']}<br>Stake: {v['stake']:,}" for v in validators],
                name="Validators"
            ))
            
            fig.update_layout(
                title="3D Network Topology",
                scene=dict(
                    xaxis_title="Network Position X",
                    yaxis_title="Network Position Y", 
                    zaxis_title="Network Position Z"
                ),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif selected_viz == "Token Distribution":
            st.write("**💰 Token Distribution**")
            st.write("Interactive 3D visualization of HYBRID token allocation")
            
            # Create 3D pie chart equivalent
            segments = ar_data["segments"]
            
            fig = go.Figure(data=[go.Pie(
                labels=[s["label"] for s in segments],
                values=[s["value"] for s in segments],
                hole=.3,
                marker_colors=[s["color"] for s in segments]
            )])
            
            fig.update_layout(
                title="Token Distribution",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**🎮 AR Controls**")
        
        if st.button("📱 Launch Mobile AR", key="mobile_ar"):
            st.success("📱 Opening AR camera view...")
            st.code("""
            // AR.js integration
            <a-scene embedded arjs>
                <a-box position="0 0.5 0" material="color: red;"></a-box>
                <a-sphere position="2 1.25 -5" radius="1.25" color="#EF2D5E"></a-sphere>
                <a-camera-static position="0 1.2 0"></a-camera-static>
            </a-scene>
            """, language="html")
        
        if st.button("🥽 Launch WebXR", key="webxr"):
            st.success("🥽 Starting WebXR session...")
            st.info("WebXR session would start in a compatible browser")
        
        if st.button("🎯 Calibrate AR", key="calibrate"):
            st.success("🎯 AR calibration complete!")
        
        st.markdown("---")
        st.write("**⚙️ AR Settings**")
        
        ar_scale = st.slider("📏 Scale", 0.1, 5.0, 1.0, 0.1)
        ar_opacity = st.slider("👻 Opacity", 0.1, 1.0, 0.8, 0.1)
        ar_animation = st.checkbox("🔄 Animation", value=True)
    
    # VR Worlds Integration
    st.subheader("🌍 VR World Integration")
    
    virtual_worlds = asyncio.run(hybridscan.get_virtual_worlds())
    
    for world in virtual_worlds[:2]:  # Show first 2 worlds
        with st.expander(f"🥽 VR Experience: {world.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**🌍 World:** {world.name}")
                st.write(f"**👥 Active Users:** {world.active_users}")
                st.write(f"**💰 Economic Activity:** ${world.economic_activity:,.0f}")
                
                if st.button(f"🚀 Enter VR World", key=f"enter_vr_{world.world_id}"):
                    vr_data = asyncio.run(hybridscan.get_vr_world_data(world.world_id))
                    st.session_state.vr_data = vr_data
                    st.success("🥽 Loading VR environment...")
            
            with col2:
                # VR world preview (simplified)
                st.write("**🏗️ World Features:**")
                st.write("• 3D blockchain visualization")
                st.write("• Interactive NFT gallery")
                st.write("• Multi-user collaboration")
                st.write("• Real-time data updates")
                
                if hasattr(st.session_state, 'vr_data'):
                    st.write("**🎮 VR Session Active**")
                    st.success("Connected to VR world!")

def render_advanced_analytics(hybridscan):
    """Render advanced analytics interface"""
    st.subheader("📊 Advanced Blockchain Analytics")
    
    # Time range selector
    col1, col2, col3 = st.columns(3)
    
    with col1:
        time_range = st.selectbox("📅 Time Range", ["24h", "7d", "30d", "90d", "1y"])
    with col2:
        metric_type = st.selectbox("📈 Metric", ["Transactions", "Volume", "Active Addresses", "Gas Usage"])
    with col3:
        chart_type = st.selectbox("📊 Chart Type", ["Line", "Bar", "Area", "Heatmap"])
    
    # Generate analytics data based on selections
    days = {"24h": 1, "7d": 7, "30d": 30, "90d": 90, "1y": 365}[time_range]
    dates = pd.date_range(start=datetime.now() - timedelta(days=days), end=datetime.now(), freq='H' if days == 1 else 'D')
    
    if metric_type == "Transactions":
        values = np.random.poisson(1500 if days == 1 else 25000, len(dates))
        title = "Transaction Count Over Time"
    elif metric_type == "Volume":
        values = np.random.lognormal(10, 1, len(dates))
        title = "Transaction Volume (HYBRID)"
    elif metric_type == "Active Addresses":
        values = np.random.poisson(5000 if days == 1 else 15000, len(dates))
        title = "Active Addresses"
    else:  # Gas Usage
        values = np.random.normal(1500000, 300000, len(dates))
        title = "Gas Usage"
    
    analytics_data = pd.DataFrame({
        'Time': dates,
        'Value': values
    })
    
    # Create chart based on type
    if chart_type == "Line":
        fig = px.line(analytics_data, x='Time', y='Value', title=title)
    elif chart_type == "Bar":
        fig = px.bar(analytics_data, x='Time', y='Value', title=title)
    elif chart_type == "Area":
        fig = px.area(analytics_data, x='Time', y='Value', title=title)
    else:  # Heatmap
        # Reshape data for heatmap
        analytics_data['Hour'] = analytics_data['Time'].dt.hour
        analytics_data['Day'] = analytics_data['Time'].dt.day
        pivot_data = analytics_data.pivot_table(values='Value', index='Hour', columns='Day', aggfunc='mean')
        fig = px.imshow(pivot_data, title=f"{title} Heatmap")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Performance Metrics")
        
        metrics_data = {
            "Metric": ["Average Block Time", "Network TPS", "Validator Uptime", "Storage Efficiency"],
            "Current": ["6.2s", "2,847", "99.8%", "94.2%"],
            "Target": ["6.0s", "3,000", "99.9%", "95.0%"],
            "Status": ["🟢 Good", "🟡 Fair", "🟢 Excellent", "🟡 Good"]
        }
        
        st.dataframe(metrics_data, use_container_width=True)
    
    with col2:
        st.subheader("🔄 Network Health")
        
        health_data = pd.DataFrame({
            'Component': ['Consensus', 'P2P Network', 'RPC Endpoints', 'Storage Nodes', 'Validators'],
            'Status': [98, 96, 99, 94, 97],
            'Trend': ['+2%', '-1%', '+0%', '+3%', '+1%']
        })
        
        fig = px.bar(health_data, x='Component', y='Status', 
                    title="Network Component Health (%)",
                    color='Status', color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

def render_developer_tools(hybridscan):
    """Render developer tools interface"""
    st.subheader("🔧 Developer Tools")
    
    # API endpoints
    st.subheader("🔌 API Endpoints")
    
    endpoints = [
        {"Method": "GET", "Endpoint": "/api/blocks/latest", "Description": "Get latest blocks"},
        {"Method": "GET", "Endpoint": "/api/tx/{hash}", "Description": "Get transaction details"},
        {"Method": "GET", "Endpoint": "/api/address/{addr}", "Description": "Get address analytics"},
        {"Method": "GET", "Endpoint": "/api/stats/network", "Description": "Get network statistics"},
        {"Method": "POST", "Endpoint": "/api/vr/worlds", "Description": "Create virtual world"},
        {"Method": "GET", "Endpoint": "/api/ar/visualize/{type}", "Description": "Get AR visualization data"}
    ]
    
    st.dataframe(endpoints, use_container_width=True)
    
    # WebSocket connections
    st.subheader("🔌 Real-time Connections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.code("""
        // WebSocket for real-time block updates
        const ws = new WebSocket('wss://hybridscan.io/ws/blocks');
        
        ws.onmessage = function(event) {
            const blockData = JSON.parse(event.data);
            console.log('New block:', blockData);
        };
        """, language="javascript")
    
    with col2:
        st.code("""
        # Python client for HybridScan API
        import requests
        
        response = requests.get('https://hybridscan.io/api/blocks/latest')
        blocks = response.json()
        
        for block in blocks:
            print(f"Block {block['height']}: {block['hash']}")
        """, language="python")
    
    # GraphQL API
    st.subheader("📊 GraphQL API")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sample Query:**")
        st.code("""
        query GetBlockWithTransactions($height: Int!) {
            block(height: $height) {
                height
                hash
                timestamp
                proposer
                transactions {
                    hash
                    from
                    to
                    amount
                    fee
                }
            }
        }
        """, language="graphql")
    
    with col2:
        st.write("**Virtual World Query:**")
        st.code("""
        query GetVirtualWorlds {
            virtualWorlds {
                worldId
                name
                creatorAddress
                activeUsers
                economicActivity
                nftAssets {
                    type
                    count
                }
            }
        }
        """, language="graphql")
    
    # SDK Integration
    st.subheader("🛠️ SDK Integration")
    
    tab1, tab2, tab3 = st.tabs(["JavaScript", "Python", "React"])
    
    with tab1:
        st.code("""
        // HybridScan JavaScript SDK
        import { HybridScan } from '@hybrid/scan-sdk';
        
        const scanner = new HybridScan({
            apiKey: 'your-api-key',
            network: 'mainnet'
        });
        
        // Get latest blocks
        const blocks = await scanner.getLatestBlocks(10);
        
        // Search blockchain
        const results = await scanner.search('hybrid1q2w3e4r5t6y7u8i9o0p');
        
        // Enter virtual world
        const worldData = await scanner.enterVirtualWorld('hybrid_metaverse_1');
        """, language="javascript")
    
    with tab2:
        st.code("""
        # HybridScan Python SDK
        from hybridscan import HybridScan
        
        scanner = HybridScan(
            api_key='your-api-key',
            network='mainnet'
        )
        
        # Get network statistics
        stats = scanner.get_network_stats()
        
        # Analyze address
        analytics = scanner.analyze_address('hybrid1q2w3e4r5t6y7u8i9o0p')
        
        # Create AR visualization
        ar_data = scanner.get_ar_visualization('Transaction Flow')
        """, language="python")
    
    with tab3:
        st.code("""
        // HybridScan React Components
        import { HybridExplorer, VirtualWorld, ARVisualization } from '@hybrid/scan-react';
        
        function App() {
            return (
                <div>
                    <HybridExplorer 
                        apiKey="your-api-key"
                        network="mainnet"
                        theme="dark"
                    />
                    
                    <VirtualWorld 
                        worldId="hybrid_metaverse_1"
                        enableVR={true}
                        enableAR={true}
                    />
                    
                    <ARVisualization 
                        type="Transaction Flow"
                        realTime={true}
                    />
                </div>
            );
        }
        """, language="jsx")

def main():
    """Main HybridScan application"""
    st.set_page_config(
        page_title="HybridScan - Blockchain Explorer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Create the main interface
    create_hybridscan_interface()

if __name__ == "__main__":
    main()
