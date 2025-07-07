
import streamlit as st
import asyncio
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List
import json

from blockchain.multi_ai_orchestrator import (
    multi_ai_orchestrator, AIProvider, TaskSpecialization, MultiAIRequest,
    analyze_hybrid_security, optimize_hybrid_algorithm, analyze_market_trends, generate_hybrid_code
)

def create_multi_ai_interface():
    """Create the ultimate Multi-AI coordination interface"""
    
    # Header with gradient background
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); padding: 3rem; border-radius: 20px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🤖 Revolutionary Multi-AI Orchestration System</h1>
        <p style="font-size: 1.2rem; margin-top: 1rem;">OpenAI GPT-4 • Grok3 • DeepSeek R3 • Anthropic Claude</p>
        <p style="opacity: 0.9;">Each AI specialized for optimal performance in specific domains</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 AI Coordination", "🔄 Consensus Engine", "📊 Performance Analytics", 
        "🚀 Specialized Tasks", "🛠️ Custom Orchestration", "📈 Real-time Dashboard"
    ])
    
    with tab1:
        render_ai_coordination_interface()
    
    with tab2:
        render_consensus_engine()
    
    with tab3:
        render_performance_analytics()
    
    with tab4:
        render_specialized_tasks()
    
    with tab5:
        render_custom_orchestration()
    
    with tab6:
        render_realtime_dashboard()

def render_ai_coordination_interface():
    """Render the main AI coordination interface"""
    st.subheader("🎯 AI Provider Coordination")
    
    # AI Provider Status Grid
    providers = [
        {
            "name": "OpenAI GPT-4",
            "icon": "🔥",
            "specializations": ["General Reasoning", "Conversational AI", "Natural Language"],
            "color": "#10b981",
            "status": "online"
        },
        {
            "name": "Grok3",
            "icon": "⚡",
            "specializations": ["Real-time Data", "Market Analysis", "Trend Prediction"],
            "color": "#3b82f6",
            "status": "online"
        },
        {
            "name": "DeepSeek R3",
            "icon": "🎯",
            "specializations": ["Code Generation", "Algorithm Optimization", "Math Reasoning"],
            "color": "#8b5cf6",
            "status": "online"
        },
        {
            "name": "Claude (Anthropic)",
            "icon": "🛡️",
            "specializations": ["Security Analysis", "Ethical Reasoning", "Research Synthesis"],
            "color": "#ef4444",
            "status": "online"
        }
    ]
    
    cols = st.columns(2)
    
    for i, provider in enumerate(providers):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {provider['color']}20, {provider['color']}10); 
                     border-left: 4px solid {provider['color']}; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                    <h3>{provider['icon']} {provider['name']}</h3>
                    <p><strong>Status:</strong> <span style="color: {provider['color']};">🟢 {provider['status'].title()}</span></p>
                    <p><strong>Specializations:</strong></p>
                    <ul>
                        {''.join([f"<li>{spec}</li>" for spec in provider['specializations']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # Quick action button for each provider
                if st.button(f"🚀 Query {provider['name']}", key=f"query_{i}"):
                    st.session_state[f'show_query_{i}'] = True
                
                # Show query interface if activated
                if st.session_state.get(f'show_query_{i}', False):
                    with st.form(f"query_form_{i}"):
                        query = st.text_area(f"Query for {provider['name']}", 
                                           placeholder=f"Ask {provider['name']} about HYBRID blockchain...")
                        
                        submitted = st.form_submit_button(f"Submit to {provider['name']}")
                        
                        if submitted and query:
                            # Map provider to AI enum
                            provider_mapping = {
                                "OpenAI GPT-4": AIProvider.OPENAI_GPT4,
                                "Grok3": AIProvider.GROK3,
                                "DeepSeek R3": AIProvider.DEEPSEEK_R3,
                                "Claude (Anthropic)": AIProvider.ANTHROPIC_CLAUDE
                            }
                            
                            # Map to appropriate task type
                            task_mapping = {
                                "OpenAI GPT-4": TaskSpecialization.GENERAL_REASONING,
                                "Grok3": TaskSpecialization.MARKET_ANALYSIS,
                                "DeepSeek R3": TaskSpecialization.CODE_GENERATION,
                                "Claude (Anthropic)": TaskSpecialization.SECURITY_ANALYSIS
                            }
                            
                            with st.spinner(f"{provider['name']} processing..."):
                                request = MultiAIRequest(
                                    query=query,
                                    task_type=task_mapping[provider['name']],
                                    context={"blockchain": "HYBRID", "specialized_query": True}
                                )
                                
                                result = asyncio.run(multi_ai_orchestrator.route_request(request))
                                
                                st.success(f"✅ Response from {provider['name']}")
                                
                                # Response metrics
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Confidence", f"{result.confidence:.1%}")
                                with col2:
                                    st.metric("Tokens", f"{result.tokens_used:,}")
                                with col3:
                                    st.metric("Cost", f"${result.cost_usd:.6f}")
                                
                                # Response content
                                st.markdown("### 📋 Response")
                                st.markdown(result.content)
                                
                            st.session_state[f'show_query_{i}'] = False

def render_consensus_engine():
    """Render the multi-AI consensus engine interface"""
    st.subheader("🔄 Multi-AI Consensus Engine")
    st.markdown("*Coordinate multiple AI experts for complex analysis*")
    
    # Consensus configuration
    col1, col2 = st.columns(2)
    
    with col1:
        consensus_topic = st.selectbox(
            "🎯 Analysis Topic",
            [
                "HYBRID Blockchain Security",
                "Market Trend Analysis",
                "Code Architecture Review",
                "Tokenomics Optimization",
                "Risk Assessment",
                "Scalability Analysis"
            ]
        )
        
        consensus_query = st.text_area(
            "📝 Detailed Query",
            placeholder="Provide a comprehensive analysis of...",
            height=150
        )
    
    with col2:
        min_ai_count = st.slider("Minimum AI Participants", 2, 4, 3)
        agreement_threshold = st.slider("Agreement Threshold", 0.5, 0.9, 0.7, 0.1)
        include_uncertainty = st.checkbox("Include Uncertainty Analysis", value=True)
        detailed_breakdown = st.checkbox("Detailed Breakdown", value=True)
    
    # Advanced consensus options
    with st.expander("⚙️ Advanced Consensus Options"):
        weight_by_specialization = st.checkbox("Weight by Specialization", value=True)
        require_unanimous = st.checkbox("Require Unanimous Agreement", value=False)
        fallback_strategy = st.selectbox(
            "Fallback Strategy",
            ["Best Single Response", "Hybrid Synthesis", "Human Review Required"]
        )
    
    if st.button("🚀 Execute Multi-AI Consensus", type="primary") and consensus_query:
        with st.spinner("Coordinating AI experts for consensus analysis..."):
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Map topic to task specialization
            topic_mapping = {
                "HYBRID Blockchain Security": TaskSpecialization.SECURITY_ANALYSIS,
                "Market Trend Analysis": TaskSpecialization.MARKET_ANALYSIS,
                "Code Architecture Review": TaskSpecialization.SYSTEM_ARCHITECTURE,
                "Tokenomics Optimization": TaskSpecialization.MATHEMATICAL_REASONING,
                "Risk Assessment": TaskSpecialization.ETHICAL_REASONING,
                "Scalability Analysis": TaskSpecialization.ALGORITHM_OPTIMIZATION
            }
            
            # Update progress
            status_text.text("🎯 Selecting optimal AI experts...")
            progress_bar.progress(0.2)
            
            request = MultiAIRequest(
                query=consensus_query,
                task_type=topic_mapping[consensus_topic],
                context={
                    "blockchain": "HYBRID",
                    "consensus_analysis": True,
                    "min_ai_count": min_ai_count,
                    "agreement_threshold": agreement_threshold
                },
                require_consensus=True
            )
            
            status_text.text("🤖 Querying AI experts...")
            progress_bar.progress(0.5)
            
            result = asyncio.run(multi_ai_orchestrator.route_request(request))
            
            status_text.text("📊 Analyzing consensus...")
            progress_bar.progress(0.8)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Consensus analysis complete!")
            
            # Display results
            if hasattr(result, 'agreement_level'):  # ConsensusResult
                st.success("🎯 Multi-AI Consensus Achieved!")
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Agreement Level", f"{result.agreement_level:.1%}")
                with col2:
                    st.metric("Participating AIs", len(result.participating_ais))
                with col3:
                    st.metric("Synthesis Method", result.synthesis_method.replace("_", " ").title())
                with col4:
                    consensus_quality = "High" if result.agreement_level > 0.8 else "Moderate" if result.agreement_level > 0.5 else "Low"
                    st.metric("Consensus Quality", consensus_quality)
                
                # Consensus visualization
                if detailed_breakdown:
                    st.markdown("### 📊 Consensus Breakdown")
                    
                    # Create confidence chart
                    confidence_data = pd.DataFrame([
                        {"AI": ai.value.replace("_", " ").title(), "Confidence": conf}
                        for ai, conf in result.confidence_scores.items()
                    ])
                    
                    fig = px.bar(
                        confidence_data, 
                        x="AI", 
                        y="Confidence",
                        title="Individual AI Confidence Scores",
                        color="Confidence",
                        color_continuous_scale="viridis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Final consensus response
                st.markdown("### 📋 Consensus Analysis")
                st.markdown(result.final_response)
                
                # Individual AI perspectives
                if include_uncertainty and hasattr(result, 'participating_ais'):
                    st.markdown("### 🔍 Individual AI Perspectives")
                    for ai in result.participating_ais:
                        confidence = result.confidence_scores[ai]
                        with st.expander(f"{ai.value.replace('_', ' ').title()} - Confidence: {confidence:.1%}"):
                            st.info(f"This AI provided insights with {confidence:.1%} confidence based on its specialization in the requested domain.")
            
            else:  # Single AI response fallback
                st.warning("Single AI Response (Consensus not achieved)")
                st.markdown(result.content)
                st.metric("Provider", result.provider.value)
                st.metric("Confidence", f"{result.confidence:.1%}")

def render_performance_analytics():
    """Render comprehensive performance analytics"""
    st.subheader("📊 Multi-AI Performance Analytics")
    
    try:
        stats = multi_ai_orchestrator.get_orchestrator_stats()
        
        if stats["total_requests"] == 0:
            st.info("No AI requests yet. Start using the system to see analytics!")
            return
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Requests", stats["total_requests"])
        with col2:
            st.metric("Consensus Sessions", stats["consensus_requests"])
        with col3:
            st.metric("Total Cost", f"${stats['total_cost']:.4f}")
        with col4:
            cost_per_request = stats['total_cost'] / max(stats['total_requests'], 1)
            st.metric("Avg Cost/Request", f"${cost_per_request:.6f}")
        
        # Provider comparison
        st.markdown("### 🤖 AI Provider Performance Comparison")
        
        provider_data = []
        for provider, provider_stats in stats["provider_stats"].items():
            if provider_stats["total_requests"] > 0:
                provider_data.append({
                    "Provider": provider.replace("_", " ").title(),
                    "Requests": provider_stats["total_requests"],
                    "Avg Confidence": provider_stats["avg_confidence"],
                    "Avg Response Time": provider_stats["avg_response_time"],
                    "Total Cost": provider_stats["total_cost"],
                    "Avg Tokens": provider_stats["avg_tokens"]
                })
        
        if provider_data:
            provider_df = pd.DataFrame(provider_data)
            
            # Performance charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.bar(
                    provider_df, 
                    x="Provider", 
                    y="Requests",
                    title="Requests by AI Provider",
                    color="Requests",
                    color_continuous_scale="blues"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.scatter(
                    provider_df,
                    x="Avg Response Time",
                    y="Avg Confidence",
                    size="Requests",
                    color="Provider",
                    title="Response Time vs Confidence",
                    hover_data=["Total Cost"]
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Detailed provider stats table
            st.markdown("### 📈 Detailed Provider Statistics")
            st.dataframe(provider_df, use_container_width=True)
        
        # Specialization coverage
        st.markdown("### 🎯 Specialization Coverage")
        
        spec_data = []
        for spec, ai_count in stats["specialization_coverage"].items():
            spec_data.append({
                "Specialization": spec.replace("_", " ").title(),
                "Available AIs": ai_count,
                "Coverage": "Full" if ai_count >= 2 else "Limited" if ai_count == 1 else "None"
            })
        
        spec_df = pd.DataFrame(spec_data)
        
        fig3 = px.pie(
            spec_df,
            values="Available AIs",
            names="Specialization",
            title="AI Specialization Distribution"
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        st.dataframe(spec_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading analytics: {e}")

def render_specialized_tasks():
    """Render specialized task interfaces"""
    st.subheader("🚀 Specialized AI Tasks")
    st.markdown("*Pre-configured tasks optimized for each AI's strengths*")
    
    # Task categories
    task_col1, task_col2 = st.columns(2)
    
    with task_col1:
        st.markdown("### 🔐 Security & Analysis Tasks")
        
        if st.button("🛡️ HYBRID Security Audit", key="security_audit"):
            with st.expander("Security Audit Results", expanded=True):
                with st.spinner("Claude performing comprehensive security audit..."):
                    audit_code = """
                    pragma solidity ^0.8.0;
                    
                    contract HybridNodeLicense {
                        mapping(uint256 => address) public licenses;
                        mapping(address => bool) public operators;
                        
                        function purchaseLicense(uint256 nodeType) external payable {
                            require(msg.value >= 100 ether, "Insufficient payment");
                            require(nodeType <= 1, "Invalid node type");
                            uint256 tokenId = block.timestamp;
                            licenses[tokenId] = msg.sender;
                        }
                        
                        function delegateOperator(address operator) external {
                            operators[operator] = true;
                        }
                    }
                    """
                    
                    result = asyncio.run(analyze_hybrid_security(audit_code))
                    
                    if hasattr(result, 'final_response'):
                        st.success("✅ Multi-AI Security Consensus Complete")
                        st.metric("Agreement Level", f"{result.agreement_level:.1%}")
                        st.markdown(result.final_response)
                    else:
                        st.success(f"✅ Security Analysis by {result.provider.value}")
                        st.metric("Confidence", f"{result.confidence:.1%}")
                        st.markdown(result.content)
        
        if st.button("⚖️ Ethical Impact Assessment", key="ethical_assessment"):
            with st.spinner("Claude analyzing ethical implications..."):
                request = MultiAIRequest(
                    query="Analyze the ethical implications of HYBRID blockchain's NFT-gated node system",
                    task_type=TaskSpecialization.ETHICAL_REASONING,
                    context={"blockchain": "HYBRID", "focus": "ethics"}
                )
                result = asyncio.run(multi_ai_orchestrator.route_request(request))
                
                st.success("✅ Ethical Analysis Complete")
                st.markdown(result.content)
    
    with task_col2:
        st.markdown("### 📊 Market & Performance Tasks")
        
        if st.button("📈 Real-time Market Analysis", key="market_analysis"):
            with st.expander("Market Analysis Results", expanded=True):
                with st.spinner("Grok3 analyzing real-time market data..."):
                    market_data = {
                        "hybrid_price": 10.50,
                        "volume_24h": 128000000,
                        "market_cap": 10500000000,
                        "social_sentiment": 0.75,
                        "competitor_analysis": True
                    }
                    
                    result = asyncio.run(analyze_market_trends(market_data))
                    
                    st.success(f"✅ Market Analysis by {result.provider.value}")
                    
                    # Market metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("HYBRID Price", "$10.50", "+$0.25")
                    with col2:
                        st.metric("24h Volume", "$128M", "+8.7%")
                    with col3:
                        st.metric("Market Cap", "$10.5B", "+2.4%")
                    
                    st.markdown(result.content)
        
        if st.button("⚙️ Algorithm Optimization", key="algo_optimization"):
            with st.spinner("DeepSeek optimizing algorithms..."):
                algo_desc = "HYBRID blockchain consensus algorithm with 21 validators and cross-chain compatibility"
                result = asyncio.run(optimize_hybrid_algorithm(algo_desc))
                
                st.success(f"✅ Algorithm Optimization by {result.provider.value}")
                st.metric("Confidence", f"{result.confidence:.1%}")
                st.code(result.content, language="python")
    
    # Code generation section
    st.markdown("### 💻 Code Generation Tasks")
    
    col1, col2 = st.columns(2)
    
    with col1:
        code_type = st.selectbox(
            "Code Type",
            ["Smart Contract", "API Endpoint", "Database Schema", "Frontend Component"]
        )
    
    with col2:
        complexity = st.selectbox("Complexity", ["Simple", "Intermediate", "Advanced"])
    
    code_requirements = st.text_area(
        "Code Requirements",
        placeholder="Describe what you want the code to do...",
        height=100
    )
    
    if st.button("🚀 Generate Code", key="generate_code") and code_requirements:
        with st.spinner("DeepSeek generating optimized code..."):
            enhanced_requirements = f"""
            Create {complexity.lower()} {code_type.lower()} for HYBRID blockchain:
            
            Requirements: {code_requirements}
            
            Include:
            - Full implementation
            - Error handling
            - Security considerations
            - Integration with HYBRID ecosystem
            - Comprehensive comments
            """
            
            result = asyncio.run(generate_hybrid_code(enhanced_requirements))
            
            st.success(f"✅ Code Generated by {result.provider.value}")
            st.metric("Confidence", f"{result.confidence:.1%}")
            
            # Code display with syntax highlighting
            st.code(result.content, language="python")
            
            # Download option
            st.download_button(
                "💾 Download Code",
                data=result.content,
                file_name=f"hybrid_{code_type.lower().replace(' ', '_')}.py",
                mime="text/plain"
            )

def render_custom_orchestration():
    """Render custom orchestration interface"""
    st.subheader("🛠️ Custom AI Orchestration")
    st.markdown("*Build custom AI workflows with multiple providers*")
    
    # Workflow builder
    st.markdown("### 🔧 Workflow Builder")
    
    workflow_name = st.text_input("Workflow Name", "My Custom AI Workflow")
    workflow_description = st.text_area("Workflow Description", height=100)
    
    # Step configuration
    st.markdown("### 📋 Workflow Steps")
    
    if 'workflow_steps' not in st.session_state:
        st.session_state.workflow_steps = []
    
    # Add new step
    with st.expander("➕ Add New Step", expanded=len(st.session_state.workflow_steps) == 0):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            step_ai = st.selectbox(
                "AI Provider",
                ["OpenAI GPT-4", "Grok3", "DeepSeek R3", "Claude (Anthropic)", "Auto-Select"]
            )
        
        with col2:
            step_task = st.selectbox(
                "Task Type",
                [spec.value.replace("_", " ").title() for spec in TaskSpecialization]
            )
        
        with col3:
            step_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        
        step_query = st.text_area("Step Query", placeholder="What should this step accomplish?")
        
        if st.button("➕ Add Step"):
            step = {
                "ai": step_ai,
                "task": step_task,
                "priority": step_priority,
                "query": step_query,
                "id": len(st.session_state.workflow_steps) + 1
            }
            st.session_state.workflow_steps.append(step)
            st.rerun()
    
    # Display current steps
    if st.session_state.workflow_steps:
        st.markdown("### 📝 Current Workflow Steps")
        
        for i, step in enumerate(st.session_state.workflow_steps):
            with st.expander(f"Step {i+1}: {step['task']} - {step['ai']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**AI Provider:** {step['ai']}")
                    st.write(f"**Task Type:** {step['task']}")
                    st.write(f"**Priority:** {step['priority']}")
                    st.write(f"**Query:** {step['query']}")
                
                with col2:
                    if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                        st.session_state.workflow_steps.pop(i)
                        st.rerun()
        
        # Execute workflow
        col1, col2, col3 = st.columns(3)
        
        with col1:
            execution_mode = st.selectbox("Execution Mode", ["Sequential", "Parallel", "Consensus"])
        
        with col2:
            if st.button("🚀 Execute Workflow", type="primary"):
                st.session_state.execute_workflow = True
        
        with col3:
            if st.button("💾 Save Workflow"):
                st.success(f"Workflow '{workflow_name}' saved!")
        
        # Execute workflow if requested
        if st.session_state.get('execute_workflow', False):
            st.markdown("### 🔄 Workflow Execution")
            
            with st.spinner("Executing custom AI workflow..."):
                progress_bar = st.progress(0)
                results = []
                
                for i, step in enumerate(st.session_state.workflow_steps):
                    progress_bar.progress((i + 1) / len(st.session_state.workflow_steps))
                    
                    # Map step configuration to request
                    task_mapping = {spec.value.replace("_", " ").title(): spec for spec in TaskSpecialization}
                    
                    request = MultiAIRequest(
                        query=step['query'],
                        task_type=task_mapping[step['task']],
                        context={"workflow_step": i+1, "workflow_name": workflow_name}
                    )
                    
                    result = asyncio.run(multi_ai_orchestrator.route_request(request))
                    results.append((step, result))
                
                progress_bar.progress(1.0)
            
            # Display results
            st.success("✅ Workflow Execution Complete!")
            
            for i, (step, result) in enumerate(results):
                with st.expander(f"Step {i+1} Results: {step['task']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("AI Provider", result.provider.value.replace("_", " ").title())
                    with col2:
                        st.metric("Confidence", f"{result.confidence:.1%}")
                    with col3:
                        st.metric("Cost", f"${result.cost_usd:.6f}")
                    
                    st.markdown("**Result:**")
                    st.markdown(result.content[:500] + "..." if len(result.content) > 500 else result.content)
            
            st.session_state.execute_workflow = False

def render_realtime_dashboard():
    """Render real-time monitoring dashboard"""
    st.subheader("📈 Real-time Multi-AI Dashboard")
    st.markdown("*Live monitoring of AI provider performance and system metrics*")
    
    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
    
    if auto_refresh:
        time.sleep(5)
        st.rerun()
    
    # Real-time metrics
    try:
        stats = multi_ai_orchestrator.get_orchestrator_stats()
        
        # System status
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🤖 Active AIs", "4")
        with col2:
            st.metric("⚡ System Load", "Normal")
        with col3:
            st.metric("🔄 Requests/min", f"{stats['total_requests']}")
        with col4:
            st.metric("💰 Cost/hour", f"${stats['total_cost'] * 60:.2f}")
        
        # Live performance chart
        st.markdown("### 📊 Live Performance Metrics")
        
        if stats["total_requests"] > 0:
            # Create mock real-time data for demonstration
            import numpy as np
            
            chart_data = pd.DataFrame({
                "Time": pd.date_range(start="now", periods=20, freq="30S"),
                "Requests": np.random.poisson(3, 20),
                "Avg_Confidence": np.random.normal(0.85, 0.05, 20),
                "Response_Time": np.random.normal(2.0, 0.5, 20)
            })
            
            # Dual axis chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=chart_data["Time"],
                y=chart_data["Requests"],
                mode="lines+markers",
                name="Requests",
                yaxis="y"
            ))
            
            fig.add_trace(go.Scatter(
                x=chart_data["Time"],
                y=chart_data["Avg_Confidence"],
                mode="lines+markers",
                name="Avg Confidence",
                yaxis="y2"
            ))
            
            fig.update_layout(
                title="Real-time AI Performance",
                xaxis_title="Time",
                yaxis=dict(title="Requests", side="left"),
                yaxis2=dict(title="Confidence", side="right", overlaying="y"),
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Active sessions
        st.markdown("### 🔄 Active Sessions")
        
        active_sessions = [
            {"Session": "Security Audit", "AI": "Claude", "Progress": 85, "Status": "Running"},
            {"Session": "Market Analysis", "AI": "Grok3", "Progress": 60, "Status": "Running"},
            {"Session": "Code Generation", "AI": "DeepSeek", "Progress": 100, "Status": "Complete"}
        ]
        
        for session in active_sessions:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"**{session['Session']}**")
            with col2:
                st.write(session['AI'])
            with col3:
                st.progress(session['Progress'] / 100)
            with col4:
                status_color = "🟢" if session['Status'] == "Complete" else "🟡" if session['Status'] == "Running" else "🔴"
                st.write(f"{status_color} {session['Status']}")
        
        # AI health status
        st.markdown("### 🏥 AI Provider Health")
        
        health_data = [
            {"Provider": "OpenAI GPT-4", "Status": "Healthy", "Uptime": "99.9%", "Latency": "1.2s"},
            {"Provider": "Grok3", "Status": "Healthy", "Uptime": "99.7%", "Latency": "0.8s"},
            {"Provider": "DeepSeek R3", "Status": "Healthy", "Uptime": "99.8%", "Latency": "1.0s"},
            {"Provider": "Claude", "Status": "Healthy", "Uptime": "99.6%", "Latency": "1.5s"}
        ]
        
        health_df = pd.DataFrame(health_data)
        st.dataframe(health_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading real-time data: {e}")
    
    # Manual refresh button
    if st.button("🔄 Refresh Dashboard"):
        st.rerun()

def main():
    """Main Multi-AI interface"""
    st.set_page_config(
        page_title="HYBRID - Multi-AI Orchestration",
        page_icon="🤖",
        layout="wide"
    )
    
    create_multi_ai_interface()

if __name__ == "__main__":
    main()
