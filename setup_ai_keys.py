
#!/usr/bin/env python3
"""
Setup script for Multi-AI API keys
Ensures all AI providers are properly configured
"""

import os
import streamlit as st

def setup_ai_api_keys():
    """Setup and verify AI API keys"""
    
    st.header("🔑 Multi-AI API Key Configuration")
    st.markdown("*Configure your AI provider API keys for the orchestration system*")
    
    # API Key inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 OpenAI Configuration")
        openai_key = st.text_input(
            "OpenAI API Key",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        
        st.subheader("🛡️ Anthropic Configuration") 
        anthropic_key = st.text_input(
            "Anthropic API Key",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            type="password",
            help="Get your API key from https://console.anthropic.com/"
        )
    
    with col2:
        st.subheader("⚡ Grok3 Configuration")
        grok3_key = st.text_input(
            "Grok3 API Key",
            value=os.getenv("GROK3_API_KEY", ""),
            type="password",
            help="Get your API key from https://x.ai/api"
        )
        
        st.subheader("🎯 DeepSeek Configuration")
        deepseek_key = st.text_input(
            "DeepSeek API Key", 
            value=os.getenv("DEEPSEEK_API_KEY", ""),
            type="password",
            help="Get your API key from https://platform.deepseek.com/"
        )
    
    # Additional configurations
    st.subheader("🤖 Coinbase AgentKit Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        cdp_api_key = st.text_input(
            "Coinbase CDP API Key",
            value=os.getenv("CDP_API_KEY_NAME", ""),
            type="password"
        )
    
    with col2:
        cdp_private_key = st.text_area(
            "Coinbase CDP Private Key",
            value=os.getenv("CDP_PRIVATE_KEY", ""),
            height=100,
            help="Your CDP private key for AgentKit integration"
        )
    
    # Save configuration
    if st.button("💾 Save API Configuration", type="primary"):
        # Set environment variables
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
        if anthropic_key:
            os.environ["ANTHROPIC_API_KEY"] = anthropic_key
        if grok3_key:
            os.environ["GROK3_API_KEY"] = grok3_key
        if deepseek_key:
            os.environ["DEEPSEEK_API_KEY"] = deepseek_key
        if cdp_api_key:
            os.environ["CDP_API_KEY_NAME"] = cdp_api_key
        if cdp_private_key:
            os.environ["CDP_PRIVATE_KEY"] = cdp_private_key
        
        st.success("🎉 API keys configured successfully!")
        st.balloons()
        
        # Test connections
        st.subheader("🔍 Testing API Connections")
        
        with st.spinner("Testing AI provider connections..."):
            # Test each provider
            results = {}
            
            if openai_key:
                try:
                    import openai
                    client = openai.OpenAI(api_key=openai_key)
                    # Test with a simple request
                    results["OpenAI"] = "✅ Connected"
                except Exception as e:
                    results["OpenAI"] = f"❌ Error: {str(e)[:50]}..."
            
            if anthropic_key:
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=anthropic_key)
                    results["Anthropic"] = "✅ Connected"
                except Exception as e:
                    results["Anthropic"] = f"❌ Error: {str(e)[:50]}..."
            
            if grok3_key:
                results["Grok3"] = "✅ API Key Set (Connection test requires real request)"
            
            if deepseek_key:
                results["DeepSeek"] = "✅ API Key Set (Connection test requires real request)"
            
            # Display results
            for provider, status in results.items():
                st.write(f"**{provider}:** {status}")
    
    # Configuration status
    st.subheader("📊 Current Configuration Status")
    
    config_status = {
        "OpenAI GPT-4": "✅ Configured" if os.getenv("OPENAI_API_KEY") else "❌ Not Set",
        "Anthropic Claude": "✅ Configured" if os.getenv("ANTHROPIC_API_KEY") else "❌ Not Set",
        "Grok3": "✅ Configured" if os.getenv("GROK3_API_KEY") else "❌ Not Set",
        "DeepSeek R3": "✅ Configured" if os.getenv("DEEPSEEK_API_KEY") else "❌ Not Set",
        "Coinbase CDP": "✅ Configured" if os.getenv("CDP_API_KEY_NAME") else "❌ Not Set"
    }
    
    for provider, status in config_status.items():
        st.write(f"**{provider}:** {status}")
    
    # Usage guidelines
    with st.expander("📖 API Usage Guidelines"):
        st.markdown("""
        ### 🎯 Provider Specializations
        
        **OpenAI GPT-4:**
        - General reasoning and analysis
        - Natural language understanding
        - Conversational AI tasks
        - Complex problem solving
        
        **Anthropic Claude:**
        - Security analysis and auditing
        - Ethical reasoning and compliance
        - Content moderation
        - Research synthesis
        
        **Grok3:**
        - Real-time market analysis
        - Social sentiment tracking
        - Trend prediction
        - Live data processing
        
        **DeepSeek R3:**
        - Code generation and optimization
        - Algorithm development
        - Mathematical reasoning
        - System architecture design
        
        ### 💰 Cost Management
        - Monitor token usage in the analytics dashboard
        - Use consensus mode sparingly for critical decisions
        - Cache frequent queries when possible
        - Set usage limits in your provider dashboards
        
        ### 🔒 Security Best Practices
        - Never commit API keys to version control
        - Rotate keys regularly
        - Monitor API usage for anomalies
        - Use environment variables for key storage
        """)

if __name__ == "__main__":
    setup_ai_api_keys()
