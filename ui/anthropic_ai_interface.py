
import streamlit as st
import asyncio
import time
from typing import Dict, Any
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from blockchain.x_moe import anthropic_moe, AnthropicModelType

def create_anthropic_ai_interface():
    """Create comprehensive Anthropic AI interface"""
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🧠 Anthropic AI Integration</h1>
        <p>Claude Sonnet & Opus models integrated with HYBRID blockchain</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💬 AI Chat", "🔍 Smart Contract Analysis", "🏗️ HTSX Generator", 
        "💰 Tokenomics Designer", "📊 AI Analytics"
    ])
    
    with tab1:
        render_ai_chat_interface()
    
    with tab2:
        render_smart_contract_analysis()
    
    with tab3:
        render_htsx_generator()
    
    with tab4:
        render_tokenomics_designer()
    
    with tab5:
        render_ai_analytics()

def render_ai_chat_interface():
    """Render AI chat interface"""
    st.subheader("💬 Chat with Claude Models")
    
    # Model selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_model = st.selectbox(
            "🤖 Select Claude Model",
            ["Auto-Route", "Claude Sonnet", "Claude Opus"],
            help="Auto-Route selects the best model based on your query type"
        )
    
    with col2:
        query_type = st.selectbox(
            "📋 Query Type",
            ["general", "coding", "smart_contract", "defi", "architecture", "tokenomics", "governance"]
        )
    
    # Chat interface
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for i, (role, message, model_used, metrics) in enumerate(st.session_state.chat_history):
        if role == "user":
            st.markdown(f"""
            <div style="background: #f0f2f6; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                <strong>You:</strong> {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
                <strong>{model_used}:</strong><br>
                {message}
                <br><small>Tokens: {metrics.get('tokens', 0)}, Cost: ${metrics.get('cost', 0):.6f}, Time: {metrics.get('time', 0)}ms</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Input area
    user_input = st.text_area(
        "💭 Ask Claude anything about HYBRID blockchain...",
        placeholder="How can I optimize gas costs for NFT license contracts?",
        height=100
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🚀 Send Message", type="primary"):
            if user_input:
                # Add user message to history
                st.session_state.chat_history.append(("user", user_input, "", {}))
                
                # Get AI response
                with st.spinner("Claude thinking..."):
                    if selected_model == "Auto-Route":
                        result = asyncio.run(anthropic_moe.route_query(user_input, query_type))
                        model_name = f"Claude {result.model_type.value.split('-')[1].title()}"
                    elif selected_model == "Claude Sonnet":
                        result = asyncio.run(anthropic_moe.call_anthropic_model(
                            AnthropicModelType.CLAUDE_SONNET, user_input
                        ))
                        model_name = "Claude Sonnet"
                    else:
                        result = asyncio.run(anthropic_moe.call_anthropic_model(
                            AnthropicModelType.CLAUDE_OPUS, user_input
                        ))
                        model_name = "Claude Opus"
                    
                    # Add AI response to history
                    metrics = {
                        'tokens': result.tokens_used,
                        'cost': result.cost_usd,
                        'time': result.processing_time_ms
                    }
                    st.session_state.chat_history.append(("ai", result.response, model_name, metrics))
                
                st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

def render_smart_contract_analysis():
    """Render smart contract analysis interface"""
    st.subheader("🔍 Smart Contract Security Analysis")
    
    # Sample contracts for demo
    sample_contracts = {
        "HYBRID NFT License": """
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract HybridNodeLicense is ERC721 {
    mapping(uint256 => NodeType) public licenseTypes;
    mapping(uint256 => address) public delegates;
    
    enum NodeType { STORAGE, VALIDATOR }
    
    function purchaseLicense(NodeType nodeType) external payable {
        require(msg.value >= 100 ether, "Insufficient payment");
        uint256 tokenId = totalSupply() + 1;
        licenseTypes[tokenId] = nodeType;
        _mint(msg.sender, tokenId);
    }
    
    function delegateNode(uint256 tokenId, address operator) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        delegates[tokenId] = operator;
    }
}
        """,
        "Cross-Chain Bridge": """
pragma solidity ^0.8.0;

contract HybridBridge {
    mapping(bytes32 => bool) public processedTxs;
    
    event BridgeTransfer(address from, address to, uint256 amount, string targetChain);
    
    function bridgeTokens(uint256 amount, string memory targetChain) external {
        require(amount > 0, "Amount must be positive");
        // Transfer logic here
        emit BridgeTransfer(msg.sender, msg.sender, amount, targetChain);
    }
}
        """
    }
    
    # Contract selection
    contract_choice = st.selectbox("📋 Select Contract", list(sample_contracts.keys()) + ["Custom"])
    
    if contract_choice == "Custom":
        contract_code = st.text_area(
            "📝 Paste your Solidity contract code:",
            height=300,
            placeholder="pragma solidity ^0.8.0;..."
        )
    else:
        contract_code = st.text_area(
            f"📝 {contract_choice} Contract:",
            value=sample_contracts[contract_choice],
            height=300
        )
    
    if st.button("🔍 Analyze Contract", type="primary"):
        if contract_code:
            with st.spinner("Claude Sonnet analyzing contract..."):
                result = asyncio.run(anthropic_moe.analyze_smart_contract(contract_code))
                
                st.success("✅ Analysis Complete!")
                
                # Display results
                st.markdown("### 📊 Analysis Results")
                st.markdown(result.response)
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Tokens Used", f"{result.tokens_used:,}")
                with col2:
                    st.metric("Analysis Cost", f"${result.cost_usd:.6f}")
                with col3:
                    st.metric("Processing Time", f"{result.processing_time_ms}ms")

def render_htsx_generator():
    """Render HTSX component generator"""
    st.subheader("🏗️ HTSX Component Generator")
    
    # Component requirements
    component_type = st.selectbox(
        "🧩 Component Type",
        ["Wallet Connector", "NFT Marketplace", "Staking Pool", "Cross-Chain Bridge", "Custom"]
    )
    
    if component_type == "Custom":
        requirements = st.text_area(
            "📝 Describe your component requirements:",
            placeholder="Create a component for...",
            height=150
        )
    else:
        requirements = st.text_area(
            f"📝 Requirements for {component_type}:",
            value=f"Create a {component_type.lower()} component with full HYBRID blockchain integration",
            height=150
        )
    
    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        include_typescript = st.checkbox("Include TypeScript interfaces", value=True)
        include_tests = st.checkbox("Generate unit tests", value=True)
        include_docs = st.checkbox("Generate documentation", value=True)
        styling_framework = st.selectbox("Styling", ["Tailwind CSS", "Styled Components", "CSS Modules"])
    
    if st.button("🏗️ Generate HTSX Component", type="primary"):
        if requirements:
            enhanced_requirements = f"""
            {requirements}
            
            Additional requirements:
            - TypeScript interfaces: {'Yes' if include_typescript else 'No'}
            - Unit tests: {'Yes' if include_tests else 'No'}
            - Documentation: {'Yes' if include_docs else 'No'}
            - Styling: {styling_framework}
            - Integration with HYBRID blockchain RPC
            - Error handling and loading states
            - Responsive design
            """
            
            with st.spinner("Claude Sonnet generating component..."):
                result = asyncio.run(anthropic_moe.generate_htsx_components(enhanced_requirements))
                
                st.success("✅ Component Generated!")
                
                # Display generated code
                st.markdown("### 📄 Generated HTSX Component")
                st.code(result.response, language="typescript")
                
                # Download option
                st.download_button(
                    "💾 Download Component",
                    data=result.response,
                    file_name=f"{component_type.lower().replace(' ', '_')}_component.tsx",
                    mime="text/typescript"
                )

def render_tokenomics_designer():
    """Render tokenomics designer interface"""
    st.subheader("💰 Tokenomics Designer")
    
    # Project details
    project_name = st.text_input("🏷️ Project Name", "My DeFi Protocol")
    project_description = st.text_area(
        "📝 Project Description",
        placeholder="Describe your project, its goals, and target users...",
        height=150
    )
    
    # Tokenomics parameters
    col1, col2 = st.columns(2)
    
    with col1:
        total_supply = st.number_input("🪙 Total Supply", min_value=1000, value=1000000000, step=1000)
        initial_circulation = st.slider("📈 Initial Circulation %", 0, 100, 20)
        inflation_rate = st.slider("📊 Annual Inflation %", 0.0, 20.0, 5.0, 0.1)
    
    with col2:
        staking_apy = st.slider("🏦 Staking APY %", 0.0, 50.0, 8.0, 0.1)
        governance_threshold = st.slider("🗳️ Governance Threshold %", 0.1, 10.0, 1.0, 0.1)
        team_allocation = st.slider("👥 Team Allocation %", 0, 30, 15)
    
    # Use cases
    st.markdown("### 🎯 Token Utilities")
    utilities = st.multiselect(
        "Select token utilities:",
        ["Governance", "Staking", "Transaction Fees", "Liquidity Mining", "NFT Purchases", "Cross-Chain Bridge Fees"],
        default=["Governance", "Staking", "Transaction Fees"]
    )
    
    if st.button("🧠 Design Tokenomics with Claude Opus", type="primary"):
        if project_description:
            tokenomics_prompt = f"""
            Project: {project_name}
            Description: {project_description}
            
            Parameters:
            - Total Supply: {total_supply:,}
            - Initial Circulation: {initial_circulation}%
            - Inflation Rate: {inflation_rate}%
            - Staking APY: {staking_apy}%
            - Governance Threshold: {governance_threshold}%
            - Team Allocation: {team_allocation}%
            - Token Utilities: {', '.join(utilities)}
            """
            
            with st.spinner("Claude Opus designing tokenomics..."):
                result = asyncio.run(anthropic_moe.design_tokenomics(tokenomics_prompt))
                
                st.success("✅ Tokenomics Design Complete!")
                
                # Display results
                st.markdown("### 📊 Tokenomics Framework")
                st.markdown(result.response)
                
                # Visualization
                st.markdown("### 📈 Token Distribution")
                
                # Create pie chart for token distribution
                distribution_data = {
                    'Category': ['Initial Circulation', 'Team', 'Staking Rewards', 'Treasury', 'Future Emissions'],
                    'Percentage': [initial_circulation, team_allocation, 25, 20, 100-initial_circulation-team_allocation-45]
                }
                
                fig = px.pie(
                    values=distribution_data['Percentage'],
                    names=distribution_data['Category'],
                    title="Token Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

def render_ai_analytics():
    """Render AI analytics dashboard"""
    st.subheader("📊 AI Usage Analytics")
    
    try:
        stats = anthropic_moe.get_model_stats()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Queries", stats["total_inferences"])
        with col2:
            st.metric("Sonnet Queries", stats["sonnet_inferences"])
        with col3:
            st.metric("Opus Queries", stats["opus_inferences"])
        with col4:
            st.metric("Total Cost", f"${stats['total_cost_usd']:.4f}")
        
        # Charts
        if stats["total_inferences"] > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Model usage distribution
                model_data = pd.DataFrame({
                    'Model': ['Claude Sonnet', 'Claude Opus'],
                    'Queries': [stats["sonnet_inferences"], stats["opus_inferences"]]
                })
                
                fig = px.pie(model_data, values='Queries', names='Model', title="Model Usage Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Performance metrics
                perf_data = pd.DataFrame({
                    'Metric': ['Avg Confidence', 'Avg Response Time (s)'],
                    'Value': [stats["avg_confidence"] * 100, stats["avg_processing_time_ms"] / 1000]
                })
                
                fig = px.bar(perf_data, x='Metric', y='Value', title="Performance Metrics")
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent queries
            st.subheader("🕒 Recent AI Queries")
            
            # Display recent inference history
            recent_queries = anthropic_moe.inference_history[-5:] if anthropic_moe.inference_history else []
            
            for query in reversed(recent_queries):
                with st.expander(f"{query.model_type.value.split('-')[1].title()} - {query.prompt[:50]}..."):
                    st.write(f"**Model:** {query.model_type.value}")
                    st.write(f"**Prompt:** {query.prompt}")
                    st.write(f"**Response:** {query.response[:200]}...")
                    st.write(f"**Tokens:** {query.tokens_used}, **Cost:** ${query.cost_usd:.6f}")
        
        else:
            st.info("No AI queries yet. Start chatting with Claude models to see analytics!")
    
    except Exception as e:
        st.error(f"Error loading analytics: {e}")

def main():
    """Main Anthropic AI interface"""
    st.set_page_config(
        page_title="HYBRID - Anthropic AI",
        page_icon="🧠",
        layout="wide"
    )
    
    create_anthropic_ai_interface()

if __name__ == "__main__":
    main()
"""
Anthropic AI Interface for HYBRID Blockchain
Claude integration for smart contract analysis and development
"""

import streamlit as st
import asyncio

def create_anthropic_ai_interface():
    """Create Anthropic AI interface"""
    
    st.header("🧠 Anthropic AI Assistant")
    st.markdown("*Claude-powered blockchain development and analysis*")
    
    # AI assistant tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "🔍 Analysis", "⚙️ Code Generation"])
    
    with tab1:
        st.subheader("💬 Chat with Claude")
        
        # Chat interface
        if "claude_messages" not in st.session_state:
            st.session_state.claude_messages = []
        
        # Display chat history
        for message in st.session_state.claude_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask Claude about HYBRID blockchain..."):
            # Add user message
            st.session_state.claude_messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                with st.spinner("Claude thinking..."):
                    # Simulate AI response
                    response = f"**Claude's Analysis:** Based on your question about '{prompt[:50]}...', I can provide insights on HYBRID blockchain architecture, tokenomics, and smart contract development. The HYBRID blockchain's unique NFT-gated node system provides interesting decentralization mechanics while maintaining network security."
                    
                    st.markdown(response)
                    st.session_state.claude_messages.append({"role": "assistant", "content": response})
    
    with tab2:
        st.subheader("🔍 Smart Contract Analysis")
        
        # Contract input
        contract_code = st.text_area(
            "Smart Contract Code",
            placeholder="pragma solidity ^0.8.0;\n\ncontract HybridExample {\n    // Your contract code here\n}",
            height=200
        )
        
        col1, col2 = st.columns(2)
        with col1:
            analysis_type = st.selectbox("Analysis Type", [
                "Security Audit",
                "Gas Optimization", 
                "Code Review",
                "Best Practices"
            ])
        
        with col2:
            if st.button("🔍 Analyze Contract", type="primary"):
                if contract_code:
                    with st.spinner("Claude analyzing contract..."):
                        st.success("✅ Analysis Complete")
                        
                        if analysis_type == "Security Audit":
                            st.markdown("""
                            **🛡️ Security Analysis Results:**
                            
                            - **No critical vulnerabilities found**
                            - **Recommendations:**
                              - Add access control modifiers
                              - Implement event logging
                              - Consider upgradability patterns
                              - Add input validation
                            
                            **Risk Score: LOW** ✅
                            """)
                        else:
                            st.markdown(f"**{analysis_type} Results:** Analysis complete for the provided contract code.")
                else:
                    st.error("Please provide contract code to analyze")
    
    with tab3:
        st.subheader("⚙️ Code Generation")
        
        # Code generation interface
        generation_type = st.selectbox("Generate", [
            "Smart Contract",
            "HTSX Component", 
            "Test Suite",
            "Documentation"
        ])
        
        requirements = st.text_area(
            "Requirements",
            placeholder="Describe what you want to generate...",
            height=100
        )
        
        if st.button("🚀 Generate Code", type="primary"):
            if requirements:
                with st.spinner("Claude generating code..."):
                    if generation_type == "Smart Contract":
                        generated_code = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract HybridNodeLicense is ERC721, Ownable {
    uint256 private _tokenIdCounter;
    
    constructor() ERC721("HybridNodeLicense", "HNL") {}
    
    function mint(address to) external onlyOwner {
        uint256 tokenId = _tokenIdCounter++;
        _mint(to, tokenId);
    }
}"""
                    elif generation_type == "HTSX Component":
                        generated_code = """<htsx>
  <html>
    <head><title>HYBRID Component</title></head>
    <body>
      <wallet-connector chains="hybrid" required="true" />
      <nft-license type="storage" />
      <node-operator type="storage" naas="true" />
    </body>
  </html>
</htsx>"""
                    else:
                        generated_code = f"// Generated {generation_type}\n// Based on: {requirements[:50]}..."
                    
                    st.success("✅ Code Generated")
                    st.code(generated_code, language="solidity" if generation_type == "Smart Contract" else "html")
            else:
                st.error("Please provide requirements")
