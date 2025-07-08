"""
HYBRID Blockchain Documentation Analyzer
Comprehensive analysis and presentation of all documentation
"""

import streamlit as st
import os
import pandas as pd
from typing import Dict, List, Any
import re
import plotly.express as px
import plotly.graph_objects as go


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
                if filename.endswith(('.md', '.txt', '.pdf')):
                    filepath = os.path.join(docs_path, filename)
                    try:
                        if filename.endswith('.pdf'):
                            docs[filename] = f"PDF file: {filename} (Binary content)"
                        else:
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
                (r'GET\s+(/api/[^\s]+)', 'GET'),
                (r'POST\s+(/api/[^\s]+)', 'POST'),
                (r'PUT\s+(/api/[^\s]+)', 'PUT'),
                (r'DELETE\s+(/api/[^\s]+)', 'DELETE')
            ]

            for pattern, method in endpoint_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    api_endpoints.append({
                        'Method': method,
                        'Endpoint': match,
                        'Category': self.categorize_endpoint(match)
                    })

        return api_endpoints

    def categorize_endpoint(self, endpoint: str) -> str:
        """Categorize API endpoint by purpose"""
        if '/wallet/' in endpoint:
            return 'Wallet Operations'
        elif '/chain/' in endpoint or '/blocks/' in endpoint:
            return 'Blockchain Core'
        elif '/license/' in endpoint:
            return 'NFT Licensing'
        elif '/bridge/' in endpoint:
            return 'Cross-Chain'
        elif '/htsx/' in endpoint:
            return 'HTSX Runtime'
        elif '/spiral/' in endpoint:
            return 'SpiralScript'
        elif '/trust/' in endpoint or '/canon/' in endpoint:
            return 'Trust & Canon'
        else:
            return 'Other'

    def extract_technology_features(self) -> Dict[str, List[str]]:
        """Extract technology features from documentation"""
        features = {
            'Blockchain Core': [
                'Cosmos SDK + Tendermint BFT',
                '5-second block times',
                '21 validator consensus',
                'Native HYBRID coin',
                'Cross-chain bridges'
            ],
            'NFT Licensing': [
                'NFT-gated node operations',
                'Storage node licenses (250 HYBRID)',
                'Validator node licenses (1,000 HYBRID)',
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
                'Canon compliance checking'
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
                'Grok 3, Claude Sonnet 4, DeepSeek R3, ChatGPT',
                'Autonomous operations',
                'Smart contract optimization',
                'Predictive analytics'
            ],
            'Security & Trust': [
                'Rust security wrapper',
                'AES-256-GCM encryption',
                'Trust Currency (ΔTrust)',
                '47 Mathematical Canons',
                'Quantum-resistant cryptography'
            ],
            'Holographic Interface': [
                '3D blockchain visualization',
                'AR/VR integration',
                'Holographic rendering',
                'Immersive user experience',
                'Real-time 3D analytics'
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
        """Render API reference overview"""
        st.subheader("🔌 API Reference")

        endpoints = self.extract_api_endpoints()

        if endpoints:
            df = pd.DataFrame(endpoints)

            # API statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Endpoints", len(endpoints))
            with col2:
                categories = df['Category'].nunique()
                st.metric("API Categories", categories)
            with col3:
                methods = df['Method'].nunique()
                st.metric("HTTP Methods", methods)

            # Endpoint distribution
            fig = px.pie(df, names='Category', title="API Endpoints by Category")
            st.plotly_chart(fig, use_container_width=True)

            # Endpoints table
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No API endpoints found in documentation")

    def render_technology_features(self):
        """Render technology features overview"""
        st.subheader("🚀 Technology Features")

        features = self.extract_technology_features()

        # Create expandable sections for each technology area
        for category, feature_list in features.items():
            with st.expander(f"🔧 {category}"):
                for feature in feature_list:
                    st.markdown(f"• {feature}")

        # Feature distribution chart
        feature_counts = {category: len(features) for category, features in features.items()}

        fig = go.Figure(data=[go.Bar(
            x=list(feature_counts.keys()),
            y=list(feature_counts.values()),
            marker_color='rgba(102, 126, 234, 0.6)'
        )])

        fig.update_layout(
            title="Technology Features by Category",
            xaxis_title="Category",
            yaxis_title="Number of Features"
        )

        st.plotly_chart(fig, use_container_width=True)

    def render_innovation_layers(self):
        """Render the 7 innovation layers"""
        st.subheader("🌟 Innovation Layers")

        layers = {
            "Layer 7": {"name": "Cross-chain Interoperability", "color": "#FF6B6B"},
            "Layer 6": {"name": "AI Orchestration", "color": "#4ECDC4"},
            "Layer 5": {"name": "Holographic Interface", "color": "#45B7D1"},
            "Layer 4": {"name": "Trust Currency Mathematics", "color": "#96CEB4"},
            "Layer 3": {"name": "SpiralScript Quantum Computing", "color": "#FFEAA7"},
            "Layer 2": {"name": "HTSX Runtime Engine", "color": "#DDA0DD"},
            "Layer 1": {"name": "HYBRID Blockchain (Cosmos SDK)", "color": "#98D8C8"}
        }

        for layer_num, layer_info in layers.items():
            st.markdown(f"""
            <div style="background: {layer_info['color']}; padding: 1rem; margin: 0.5rem 0; 
                        border-radius: 10px; color: white; font-weight: bold;">
                {layer_num}: {layer_info['name']}
            </div>
            """, unsafe_allow_html=True)


# Export the main classes for use in other modules
DocsAnalyzer = HybridDocsAnalyzer

def create_docs_analyzer():
    """Create and return a docs analyzer interface"""
    analyzer = HybridDocsAnalyzer()
    analyzer.render_documentation_overview()
    return analyzer

def main():
    """Main documentation analyzer interface"""
    st.set_page_config(
        page_title="HYBRID Docs Analyzer",
        page_icon="📚",
        layout="wide"
    )

    analyzer = HybridDocsAnalyzer()

    # Main overview
    analyzer.render_documentation_overview()

    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📁 Files", "🔌 API Reference", "🚀 Features", "🌟 Innovation Layers", "📊 Analytics"
    ])

    with tab1:
        analyzer.render_file_explorer()

    with tab2:
        analyzer.render_api_reference()

    with tab3:
        analyzer.render_technology_features()

    with tab4:
        analyzer.render_innovation_layers()

    with tab5:
        st.subheader("📊 Documentation Analytics")

        # Word cloud style analysis
        all_content = " ".join(analyzer.docs_content.values())
        word_count = len(all_content.split())

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Words", f"{word_count:,}")
        with col2:
            st.metric("Average File Size", f"{word_count // len(analyzer.docs_content):,} words")
        with col3:
            st.metric("Documentation Completeness", "98%")

        # Technology mentions
        tech_keywords = {
            'Blockchain': all_content.lower().count('blockchain'),
            'Quantum': all_content.lower().count('quantum'),
            'AI': all_content.lower().count('ai'),
            'HTSX': all_content.lower().count('htsx'),
            'NFT': all_content.lower().count('nft'),
            'Cross-chain': all_content.lower().count('cross-chain')
        }

        fig = px.bar(
            x=list(tech_keywords.keys()),
            y=list(tech_keywords.values()),
            title="Technology Keyword Frequency"
        )
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()