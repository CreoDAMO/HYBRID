
"""
Holographic Blockchain Interface for HYBRID + HTSX
Streamlit-powered 3D blockchain visualization with adaptive learning
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from typing import Dict, Any
import sys
import os

# Add blockchain module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blockchain'))

try:
    from blockchain.holographic_blockchain_engine import (
        holographic_engine, LearningStage, VisualizationMode
    )
except ImportError:
    st.error("Holographic blockchain engine not available")

def create_holographic_interface():
    """Create the revolutionary holographic blockchain interface"""
    
    st.header("🌈 HYBRID Holographic Blockchain Visualization")
    st.markdown("*Revolutionary 3D Blockchain Visualization with Adaptive Learning*")
    
    # Learning stage selector
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        learning_stage = st.selectbox(
            "🎓 Learning Stage",
            options=[stage.value.title() for stage in LearningStage],
            index=0,
            help="Adaptive complexity based on your blockchain knowledge"
        )
    
    with col2:
        visualization_mode = st.selectbox(
            "👁️ Visualization Mode",
            options=[mode.value.replace('_', ' ').title() for mode in VisualizationMode],
            index=0
        )
    
    with col3:
        auto_update = st.checkbox("🔄 Live Update", value=True)
    
    # Adaptive settings based on learning stage
    stage_enum = LearningStage(learning_stage.lower())
    adaptations = holographic_engine.adapt_to_user_level(stage_enum)
    
    # Learning stage information
    with st.expander("📚 Learning Stage Information", expanded=adaptations["tutorial_mode"]):
        if stage_enum == LearningStage.BEGINNER:
            st.info("""
            **🌱 Beginner Stage - Simple Room Environment**
            - Focus on single transactions as glowing orbs
            - Basic wallet interactions
            - Foundational blockchain concepts
            - Clean, minimal holographic space
            """)
        elif stage_enum == LearningStage.INTERMEDIATE:
            st.info("""
            **🌿 Intermediate Stage - Expanded Environment**
            - Multiple transaction streams visible
            - Block formation with 10-20 nodes
            - Smart contract introduction
            - Basic economic concept visualization
            """)
        elif stage_enum == LearningStage.ADVANCED:
            st.info("""
            **🌳 Advanced Stage - Full Blockchain Metropolis**
            - Complete ecosystem visualization
            - DeFi protocol navigation
            - MEV bot racing and arbitrage
            - Cross-chain bridge interactions
            """)
        else:  # EXPERT
            st.info("""
            **🔬 Expert Stage - Mathematical Visualization**
            - Raw cryptographic function visualization
            - Hash function manipulation
            - Zero-knowledge proof puzzles
            - Real-time protocol development
            """)
    
    # Generate sample data
    sample_data = holographic_engine.generate_sample_data()
    
    # Apply adaptive filtering
    max_transactions = adaptations["max_transactions"]
    max_blocks = adaptations["max_blocks"]
    
    filtered_transactions = sample_data["transactions"][:max_transactions]
    filtered_blocks = sample_data["blocks"][:max_blocks]
    
    # Main visualization tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌊 Transaction Rivers", "💎 Crystalline Blocks", "🏗️ Smart Contracts", "🌀 DeFi Vortexes", "📊 Analytics"
    ])
    
    with tab1:
        st.subheader("🌊 Live Transaction Rivers")
        st.markdown("*Flowing streams of blockchain transactions in 3D space*")
        
        if visualization_mode.replace(' ', '_').lower() == "transaction_flows" or True:
            # Create transaction river
            river_fig = holographic_engine.create_transaction_river(filtered_transactions)
            st.plotly_chart(river_fig, use_container_width=True)
            
            # Transaction statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_value = sum(tx.value for tx in filtered_transactions)
                st.metric("Total Value", f"{total_value:.2f} ETH")
            with col2:
                avg_gas = np.mean([tx.gas_used for tx in filtered_transactions])
                st.metric("Avg Gas Used", f"{avg_gas:,.0f}")
            with col3:
                st.metric("Active Transactions", len(filtered_transactions))
            with col4:
                st.metric("Flow Speed", f"{adaptations['animation_speed']}x")
    
    with tab2:
        st.subheader("💎 Crystalline Block Architecture")
        st.markdown("*Each block as an explorable 3D crystalline structure*")
        
        # Create crystalline blocks
        blocks_fig = holographic_engine.create_crystalline_blocks(filtered_blocks)
        st.plotly_chart(blocks_fig, use_container_width=True)
        
        # Block information
        if filtered_blocks:
            latest_block = filtered_blocks[-1]
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Latest Block", f"#{latest_block.height}")
            with col2:
                st.metric("Block Transactions", len(latest_block.transactions))
            with col3:
                st.metric("Validator", latest_block.validator)
    
    with tab3:
        st.subheader("🏗️ Smart Contract Holographic City")
        st.markdown("*Interactive buildings representing smart contracts*")
        
        # Create smart contract environment
        contracts_fig = holographic_engine.create_smart_contract_environment(sample_data["contracts"])
        st.plotly_chart(contracts_fig, use_container_width=True)
        
        # Contract details
        st.markdown("### 📋 Active Smart Contracts")
        for contract in sample_data["contracts"]:
            with st.expander(f"🏢 {contract['name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Type", contract['type'])
                with col2:
                    st.metric("TVL", f"${contract['tvl']:,.0f}")
                with col3:
                    st.metric("Gas Usage", f"{contract['gas_usage']:,.0f}")
    
    with tab4:
        st.subheader("🌀 DeFi Protocol Energy Vortexes")
        st.markdown("*Liquidity pools as swirling energy vortexes*")
        
        # Create DeFi vortex
        defi_fig = holographic_engine.create_defi_vortex(sample_data["defi_pools"])
        st.plotly_chart(defi_fig, use_container_width=True)
        
        # DeFi pool information
        st.markdown("### 💰 Active Liquidity Pools")
        for pool in sample_data["defi_pools"]:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pool", pool['name'])
            with col2:
                st.metric("Liquidity", f"${pool['liquidity']:,.0f}")
            with col3:
                st.metric("APY", f"{pool['apy']:.1f}%")
    
    with tab5:
        st.subheader("📊 Holographic Learning Analytics")
        st.markdown("*Adaptive learning progress and comprehension tracking*")
        
        # Learning progress simulation
        progress_data = {
            "Concept": ["Transactions", "Blocks", "Smart Contracts", "DeFi", "Cross-Chain"],
            "Mastery": [85, 72, 45, 30, 15],
            "Time Spent": [120, 95, 60, 30, 10]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Mastery radar chart
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=progress_data["Mastery"],
                theta=progress_data["Concept"],
                fill='toself',
                name='Concept Mastery'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                title="🎯 Concept Mastery Progress"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # Time spent analysis
            fig_bar = go.Figure([go.Bar(
                x=progress_data["Concept"],
                y=progress_data["Time Spent"],
                marker_color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7']
            )])
            fig_bar.update_layout(
                title="⏱️ Learning Time Distribution",
                xaxis_title="Blockchain Concepts",
                yaxis_title="Time Spent (minutes)"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Adaptive recommendations
        st.markdown("### 🎯 Personalized Learning Recommendations")
        if stage_enum == LearningStage.BEGINNER:
            st.success("✅ Focus on understanding single transactions before moving to blocks")
            st.info("💡 Try interacting with the transaction river to follow individual payments")
        elif stage_enum == LearningStage.INTERMEDIATE:
            st.success("✅ Ready to explore smart contract interactions")
            st.info("💡 Examine how blocks form from transaction pools")
        else:
            st.success("✅ Advanced DeFi concepts and cross-chain protocols available")
            st.info("💡 Experiment with complex multi-protocol interactions")
    
    # Real-time controls
    st.divider()
    st.subheader("🎛️ Holographic Environment Controls")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        particle_density = st.slider(
            "✨ Particle Density",
            min_value=50,
            max_value=500,
            value=int(100 * adaptations["complexity_multiplier"]),
            help="Number of visual particles in the holographic environment"
        )
    
    with col2:
        animation_speed = st.slider(
            "⚡ Animation Speed",
            min_value=0.1,
            max_value=3.0,
            value=adaptations["animation_speed"],
            step=0.1,
            help="Speed of holographic animations"
        )
    
    with col3:
        environment_complexity = st.slider(
            "🌐 Environment Complexity",
            min_value=0.1,
            max_value=1.0,
            value=adaptations["complexity_multiplier"],
            step=0.1,
            help="Overall complexity of the holographic environment"
        )
    
    with col4:
        show_labels = st.toggle(
            "🏷️ Show Labels",
            value=adaptations["show_labels"],
            help="Display informational labels on holographic elements"
        )
    
    # Performance metrics
    with st.expander("⚡ Performance Metrics"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Render FPS", "60")
        with col2:
            st.metric("Particles Rendered", f"{particle_density:,}")
        with col3:
            st.metric("Memory Usage", "245 MB")
        with col4:
            st.metric("GPU Utilization", "67%")
    
    # Achievement system preview
    st.divider()
    st.subheader("🏆 Holographic Achievement NFTs")
    st.markdown("*Blockchain-verified learning credentials as tradeable NFTs*")
    
    achievements = [
        {"name": "First Transaction", "description": "Successfully traced your first blockchain transaction", "unlocked": True},
        {"name": "Block Explorer", "description": "Explored crystalline block structures", "unlocked": True},
        {"name": "Smart Contract Navigator", "description": "Interacted with holographic smart contracts", "unlocked": False},
        {"name": "DeFi Master", "description": "Mastered DeFi protocol visualization", "unlocked": False},
        {"name": "Cross-Chain Pioneer", "description": "Completed cross-chain bridge interactions", "unlocked": False}
    ]
    
    achievement_cols = st.columns(len(achievements))
    for i, achievement in enumerate(achievements):
        with achievement_cols[i]:
            if achievement["unlocked"]:
                st.success(f"🏆 {achievement['name']}")
                st.caption(achievement['description'])
            else:
                st.info(f"🔒 {achievement['name']}")
                st.caption(achievement['description'])

def main():
    """Main holographic interface"""
    st.set_page_config(
        page_title="HYBRID - Holographic Blockchain",
        page_icon="🌈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    create_holographic_interface()

if __name__ == "__main__":
    main()
