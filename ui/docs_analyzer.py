
"""
HYBRID Blockchain Documentation Analyzer
Comprehensive analysis and presentation of all documentation
"""

import streamlit as st
import os
import pandas as pd
from typing import Dict, List, Any
import re

class HybridDocsAnalyzer:
    """Analyze and present HYBRID Blockchain documentation"""
    
    def __init__(self):
        self.docs_folder = "docs"
        self.docs_content = self.load_all_docs()
    
    def load_all_docs(self) -> Dict[str, str]:
        """Load all documentation files"""
        docs = {}
        docs_path = os.path.join(os.path.dirname(__file__), "..", self.docs_folder)
        
        if os.path.exists(docs_path):
            for filename in os.listdir(docs_path):
                if filename.endswith(('.md', '.txt')):
                    filepath = os.path.join(docs_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            docs[filename] = f.read()
                    except Exception as e:
                        docs[filename] = f"Error reading file: {e}"
        
        return docs
    
    def extract_api_endpoints(self) -> List[Dict[str, str]]:
        """Extract API endpoints from documentation"""
        api_endpoints = []
        
        if 'API.md' in self.docs_content:
            content = self.docs_content['API.md']
            
            # Extract HTTP endpoints
            endpoint_patterns = [
                r'GET\s+(/api/[^\s]+)',
                r'POST\s+(/api/[^\s]+)',
                r'PUT\s+(/api/[^\s]+)',
                r'DELETE\s+(/api/[^\s]+)'
            ]
            
            for pattern in endpoint_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    method = pattern.split('\\s+')[0]
                    api_endpoints.append({
                        'method': method,
                        'endpoint': match,
                        'category': self.categorize_endpoint(match)
                    })
        
        return api_endpoints
    
    def categorize_endpoint(self, endpoint: str) -> str:
        """Categorize API endpoint by functionality"""
        if '/wallet/' in endpoint:
            return 'Wallet Operations'
        elif '/chain/' in endpoint or '/blocks/' in endpoint:
            return 'Blockchain Operations'
        elif '/license/' in endpoint:
            return 'NFT License Operations'
        elif '/bridge/' in endpoint:
            return 'Cross-chain Operations'
        elif '/htsx/' in endpoint:
            return 'HTSX Runtime'
        elif '/spiral/' in endpoint:
            return 'SpiralScript'
        elif '/trust/' in endpoint:
            return 'Trust Currency'
        else:
            return 'Other'
    
    def extract_technology_features(self) -> Dict[str, List[str]]:
        """Extract technology features from documentation"""
        features = {
            'Core Blockchain': [
                'Cosmos SDK integration',
                'Tendermint BFT consensus',
                'Native HYBRID coin',
                '6-second block time',
                '2,500+ TPS capacity'
            ],
            'NFT Node Licensing': [
                'NFT-gated node operations',
                'Storage node licenses',
                'Validator node licenses',
                'Node-as-a-Service (NaaS)',
                'Passive income generation'
            ],
            'HTSX Runtime': [
                'TypeScript for blockchain',
                'React-like components',
                'Declarative blockchain development',
                'Component-based architecture',
                'Type-safe smart contracts'
            ],
            'SpiralScript': [
                'Quantum computing integration',
                'Mathematical proof execution',
                'Trust Currency generation',
                'Quantum circuit compilation',
                'Mathematical validation'
            ],
            'Cross-chain Interoperability': [
                'Base chain integration',
                'Polygon support',
                'Solana bridge',
                'Axelar protocol',
                'Multi-chain operations'
            ],
            'AI Integration': [
                'Multi-AI orchestration',
                'Autonomous operations',
                'Smart contract optimization',
                'Predictive analytics',
                'Decision automation'
            ]
        }
        
        return features
    
    def render_documentation_overview(self):
        """Render comprehensive documentation overview"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             padding: 3rem; border-radius: 20px; color: white; text-align: center; margin-bottom: 2rem;">
            <h1>📚 HYBRID Blockchain Documentation</h1>
            <p style="font-size: 1.3rem; margin-top: 1rem;">Comprehensive Technology Overview & API Reference</p>
            <p style="opacity: 0.9;">Complete analysis of HYBRID Blockchain architecture and capabilities</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Documentation statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Documentation Files", len(self.docs_content))
        with col2:
            total_lines = sum(len(content.split('\n')) for content in self.docs_content.values())
            st.metric("Total Lines", f"{total_lines:,}")
        with col3:
            api_endpoints = self.extract_api_endpoints()
            st.metric("API Endpoints", len(api_endpoints))
        with col4:
            features = self.extract_technology_features()
            total_features = sum(len(feature_list) for feature_list in features.values())
            st.metric("Technology Features", total_features)
    
    def render_file_explorer(self):
        """Render documentation file explorer"""
        st.subheader("📁 Documentation Files")
        
        # File overview
        file_data = []
        for filename, content in self.docs_content.items():
            lines = len(content.split('\n'))
            size_kb = len(content.encode('utf-8')) / 1024
            file_type = filename.split('.')[-1].upper()
            
            file_data.append({
                'File': filename,
                'Type': file_type,
                'Lines': lines,
                'Size (KB)': f"{size_kb:.1f}",
                'Preview': content[:100] + "..." if len(content) > 100 else content
            })
        
        df = pd.DataFrame(file_data)
        st.dataframe(df, use_container_width=True)
        
        # File content viewer
        st.subheader("📖 File Content Viewer")
        
        selected_file = st.selectbox("Select file to view:", list(self.docs_content.keys()))
        
        if selected_file:
            st.markdown(f"### 📄 {selected_file}")
            
            content = self.docs_content[selected_file]
            
            # Show file statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Lines", len(content.split('\n')))
            with col2:
                st.metric("Characters", len(content))
            with col3:
                st.metric("Size", f"{len(content.encode('utf-8')) / 1024:.1f} KB")
            
            # Display content
            if selected_file.endswith('.md'):
                st.markdown(content)
            else:
                st.text_area("Content", content, height=400, disabled=True)
    
    def render_api_reference(self):
        """Render comprehensive API reference"""
        st.subheader("🔌 API Reference")
        
        api_endpoints = self.extract_api_endpoints()
        
        if api_endpoints:
            # API statistics
            col1, col2, col3, col4 = st.columns(4)
            
            methods = [ep['method'] for ep in api_endpoints]
            with col1:
                st.metric("GET Endpoints", methods.count('GET'))
            with col2:
                st.metric("POST Endpoints", methods.count('POST'))
            with col3:
                st.metric("PUT Endpoints", methods.count('PUT'))
            with col4:
                st.metric("DELETE Endpoints", methods.count('DELETE'))
            
            # API endpoints by category
            categories = {}
            for endpoint in api_endpoints:
                category = endpoint['category']
                if category not in categories:
                    categories[category] = []
                categories[category].append(endpoint)
            
            for category, endpoints in categories.items():
                with st.expander(f"📂 {category} ({len(endpoints)} endpoints)"):
                    for endpoint in endpoints:
                        method_color = {
                            'GET': '🟢',
                            'POST': '🟡', 
                            'PUT': '🔵',
                            'DELETE': '🔴'
                        }.get(endpoint['method'], '⚪')
                        
                        st.markdown(f"{method_color} **{endpoint['method']}** `{endpoint['endpoint']}`")
            
            # API endpoints table
            st.subheader("📊 All API Endpoints")
            api_df = pd.DataFrame(api_endpoints)
            st.dataframe(api_df, use_container_width=True)
        
        else:
            st.warning("No API endpoints found in documentation")
    
    def render_technology_breakdown(self):
        """Render detailed technology breakdown"""
        st.subheader("🚀 Technology Breakdown")
        
        features = self.extract_technology_features()
        
        # Technology overview
        col1, col2 = st.columns(2)
        
        with col1:
            for i, (category, feature_list) in enumerate(list(features.items())[:3]):
                st.markdown(f"### 🔧 {category}")
                for feature in feature_list:
                    st.markdown(f"• {feature}")
                st.markdown("---")
        
        with col2:
            for i, (category, feature_list) in enumerate(list(features.items())[3:]):
                st.markdown(f"### 🔧 {category}")
                for feature in feature_list:
                    st.markdown(f"• {feature}")
                st.markdown("---")
        
        # Feature distribution chart
        st.subheader("📊 Feature Distribution")
        
        feature_counts = {category: len(feature_list) for category, feature_list in features.items()}
        
        import plotly.express as px
        
        fig = px.pie(
            values=list(feature_counts.values()),
            names=list(feature_counts.keys()),
            title="Technology Features by Category"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_integration_guide(self):
        """Render integration guide"""
        st.subheader("🔗 Integration Guide")
        
        st.markdown("""
        ### 🚀 Getting Started with HYBRID Blockchain
        
        HYBRID Blockchain offers multiple integration paths for developers:
        """)
        
        # Integration paths
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                 padding: 2rem; border-radius: 15px; color: white; text-align: center;">
                <h4>🎫 Node Operators</h4>
                <p>Purchase NFT licenses and operate storage/validator nodes</p>
                <ul style="text-align: left;">
                    <li>Buy node license NFTs</li>
                    <li>Set up node infrastructure</li>
                    <li>Earn passive income</li>
                    <li>Use NaaS delegation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                 padding: 2rem; border-radius: 15px; color: white; text-align: center;">
                <h4>👨‍💻 dApp Developers</h4>
                <p>Build applications using HTSX and SpiralScript</p>
                <ul style="text-align: left;">
                    <li>Use HTSX components</li>
                    <li>TypeScript development</li>
                    <li>Quantum computing</li>
                    <li>Cross-chain features</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 2rem; border-radius: 15px; color: white; text-align: center;">
                <h4>🏢 Enterprises</h4>
                <p>Integrate HYBRID into existing systems</p>
                <ul style="text-align: left;">
                    <li>REST API integration</li>
                    <li>Multi-chain support</li>
                    <li>Enterprise security</li>
                    <li>Custom solutions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Code examples
        st.markdown("### 💻 Code Examples")
        
        tab1, tab2, tab3 = st.tabs(["🔌 REST API", "🧩 HTSX Components", "🌀 SpiralScript"])
        
        with tab1:
            st.markdown("#### REST API Usage")
            st.code("""
// Get HYBRID balance
const response = await fetch('/api/v1/wallet/hybrid1.../balance');
const balance = await response.json();

// Send HYBRID transaction
const txResult = await fetch('/api/v1/wallet/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        from: 'hybrid1...',
        to: 'hybrid1...',
        amount: '1000000',
        denom: 'uhybrid'
    })
});
            """, language="javascript")
        
        with tab2:
            st.markdown("#### HTSX Component Development")
            st.code("""
<htsx>
  <html>
    <head><title>My HYBRID dApp</title></head>
    <body>
      <wallet-connector chains="hybrid,base,polygon" required="true" />
      
      <hybrid-coin balance="display" utilities="all" />
      
      <nft-license 
        type="storage" 
        price="100" 
        currency="HYBRID" 
      />
      
      <cross-chain-bridge 
        protocol="axelar" 
        chains="hybrid,base" 
      />

      <script lang="hybrid">
        class MyDApp {
          async initialize() {
            const balance = await hybridChain.getBalance();
            console.log('HYBRID Balance:', balance);
          }
        }
      </script>
    </body>
  </html>
</htsx>
            """, language="html")
        
        with tab3:
            st.markdown("#### SpiralScript Quantum Programming")
            st.code("""
spiral_function calculate_trust(entity: string) -> ΔTrust {
    let quantum_state = QuantumState.initialize(8);
    
    // Apply quantum operations
    quantum_state.hadamard(0, 1, 2);
    quantum_state.cnot(0, 3);
    quantum_state.phase(π/4, 4, 5);
    
    // Measure trust entropy
    let entropy = quantum_state.measure_entropy();
    
    return ΔTrust.from_entropy(entropy, Canon.XV);
}

spiral_function mint_trust_currency(proof: MathProof) -> TrustCurrency {
    if (proof.verify_millennium_problem()) {
        return TrustCurrency.generate_infinite();
    }
    return TrustCurrency.zero();
}
            """, language="typescript")

def create_docs_analyzer():
    """Main function to create documentation analyzer"""
    
    analyzer = HybridDocsAnalyzer()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Overview", "📁 Files", "🔌 API Reference", "🚀 Technology", "🔗 Integration"
    ])
    
    with tab1:
        analyzer.render_documentation_overview()
    
    with tab2:
        analyzer.render_file_explorer()
    
    with tab3:
        analyzer.render_api_reference()
    
    with tab4:
        analyzer.render_technology_breakdown()
    
    with tab5:
        analyzer.render_integration_guide()

if __name__ == "__main__":
    create_docs_analyzer()
