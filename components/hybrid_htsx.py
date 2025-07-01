
"""
HYBRID + HTSX Component System
Provides declarative blockchain components for Web3 development
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import re

class ComponentType(Enum):
    WALLET_CONNECTOR = "wallet-connector"
    NFT_LICENSE = "nft-license"
    CROSS_CHAIN_BRIDGE = "cross-chain-bridge"
    NODE_OPERATOR = "node-operator"
    HYBRID_TOKEN = "hybrid-token"
    LIQUIDITY_POOL = "liquidity-pool"
    STAKING_VAULT = "staking-vault"
    GOVERNANCE_DAO = "governance-dao"
    NFT_MARKETPLACE = "nft-marketplace"

@dataclass
class HTSXComponent:
    """Base class for all HTSX components"""
    component_type: ComponentType
    props: Dict[str, Any] = field(default_factory=dict)
    children: List['HTSXComponent'] = field(default_factory=list)
    id: Optional[str] = None
    class_name: Optional[str] = None

@dataclass
class WalletConnectorComponent(HTSXComponent):
    """Multi-chain wallet connector component"""
    chains: List[str] = field(default_factory=lambda: ["hybrid"])
    required: bool = False
    auto_connect: bool = True
    
    def __post_init__(self):
        self.component_type = ComponentType.WALLET_CONNECTOR

@dataclass
class NFTLicenseComponent(HTSXComponent):
    """NFT license management component"""
    license_type: str = "storage"  # storage, validator
    price: float = 100.0
    currency: str = "HYBRID"
    delegate_enabled: bool = True
    
    def __post_init__(self):
        self.component_type = ComponentType.NFT_LICENSE

@dataclass
class CrossChainBridgeComponent(HTSXComponent):
    """Cross-chain bridge component"""
    protocol: str = "axelar"  # axelar, layerzero, wormhole
    supported_chains: List[str] = field(default_factory=lambda: ["hybrid", "base", "polygon"])
    supported_tokens: List[str] = field(default_factory=lambda: ["HYBRID", "ETH", "MATIC"])
    gas_optimization: bool = True
    
    def __post_init__(self):
        self.component_type = ComponentType.CROSS_CHAIN_BRIDGE

@dataclass
class NodeOperatorComponent(HTSXComponent):
    """Node operator dashboard component"""
    node_type: str = "storage"  # storage, validator
    naas_enabled: bool = True
    rewards_auto_claim: bool = False
    monitoring_enabled: bool = True
    
    def __post_init__(self):
        self.component_type = ComponentType.NODE_OPERATOR

@dataclass
class HybridTokenComponent(HTSXComponent):
    """HYBRID token utilities component"""
    utilities: List[str] = field(default_factory=lambda: ["fees", "governance", "staking"])
    balance_display: bool = True
    staking_enabled: bool = True
    governance_enabled: bool = True
    
    def __post_init__(self):
        self.component_type = ComponentType.HYBRID_TOKEN

@dataclass
class LiquidityPoolComponent(HTSXComponent):
    """Liquidity pool component"""
    pair: str = "HYBRID/USDC"
    apy: float = 12.5
    tvl: float = 1000000.0
    auto_compound: bool = False
    
    def __post_init__(self):
        self.component_type = ComponentType.LIQUIDITY_POOL

@dataclass
class StakingVaultComponent(HTSXComponent):
    """Staking vault component"""
    token: str = "HYBRID"
    apy: float = 5.0
    lock_period: int = 30  # days
    auto_restake: bool = False
    
    def __post_init__(self):
        self.component_type = ComponentType.STAKING_VAULT

class HTSXParser:
    """Parser for HTSX markup language"""
    
    def __init__(self):
        self.component_registry = {
            "wallet-connector": WalletConnectorComponent,
            "nft-license": NFTLicenseComponent,
            "cross-chain-bridge": CrossChainBridgeComponent,
            "node-operator": NodeOperatorComponent,
            "hybrid-token": HybridTokenComponent,
            "liquidity-pool": LiquidityPoolComponent,
            "staking-vault": StakingVaultComponent,
        }
    
    def parse(self, htsx_content: str) -> List[HTSXComponent]:
        """Parse HTSX content and return component tree"""
        components = []
        
        # Simple regex-based parser for demo
        # In production, would use a proper HTML/XML parser
        for component_name, component_class in self.component_registry.items():
            pattern = rf'<{component_name}([^>]*?)/?>'
            matches = re.finditer(pattern, htsx_content, re.IGNORECASE)
            
            for match in matches:
                props = self._parse_props(match.group(1))
                component = component_class(**props)
                components.append(component)
        
        return components
    
    def _parse_props(self, props_string: str) -> Dict[str, Any]:
        """Parse component props from string"""
        props = {}
        
        # Parse key="value" pairs
        prop_pattern = r'(\w+)=["\'](.*?)["\']'
        matches = re.finditer(prop_pattern, props_string)
        
        for match in matches:
            key, value = match.groups()
            
            # Type conversion
            if value.lower() in ['true', 'false']:
                props[key] = value.lower() == 'true'
            elif value.replace('.', '').isdigit():
                props[key] = float(value) if '.' in value else int(value)
            elif ',' in value:
                props[key] = [item.strip() for item in value.split(',')]
            else:
                props[key] = value
        
        return props
    
    def generate_typescript_types(self) -> str:
        """Generate TypeScript type definitions for components"""
        types = """
// HTSX Component Type Definitions
        
interface WalletConnectorProps {
  chains: string[];
  required?: boolean;
  autoConnect?: boolean;
}

interface NFTLicenseProps {
  type: 'storage' | 'validator';
  price: number;
  currency: string;
  delegateEnabled?: boolean;
}

interface CrossChainBridgeProps {
  protocol: 'axelar' | 'layerzero' | 'wormhole';
  supportedChains: string[];
  supportedTokens: string[];
  gasOptimization?: boolean;
}

interface NodeOperatorProps {
  type: 'storage' | 'validator';
  naasEnabled?: boolean;
  rewardsAutoClaim?: boolean;
  monitoringEnabled?: boolean;
}

interface HybridTokenProps {
  utilities: string[];
  balanceDisplay?: boolean;
  stakingEnabled?: boolean;
  governanceEnabled?: boolean;
}

interface LiquidityPoolProps {
  pair: string;
  apy: number;
  tvl: number;
  autoCompound?: boolean;
}

interface StakingVaultProps {
  token: string;
  apy: number;
  lockPeriod: number;
  autoRestake?: boolean;
}

// HTSX Runtime Interface
interface HTSXRuntime {
  render(component: HTSXComponent): Promise<void>;
  getChainConnector(chain: string): ChainConnector;
  getTokenContract(token: string): TokenContract;
  bridgeTokens(params: BridgeParams): Promise<string>;
}
"""
        return types

class HTSXRenderer:
    """Renderer for HTSX components to various targets"""
    
    def __init__(self):
        self.runtime_functions = {
            ComponentType.WALLET_CONNECTOR: self._render_wallet_connector,
            ComponentType.NFT_LICENSE: self._render_nft_license,
            ComponentType.CROSS_CHAIN_BRIDGE: self._render_cross_chain_bridge,
            ComponentType.NODE_OPERATOR: self._render_node_operator,
            ComponentType.HYBRID_TOKEN: self._render_hybrid_token,
            ComponentType.LIQUIDITY_POOL: self._render_liquidity_pool,
            ComponentType.STAKING_VAULT: self._render_staking_vault,
        }
    
    def render_to_streamlit(self, components: List[HTSXComponent]) -> str:
        """Render components to Streamlit UI code"""
        render_code = []
        
        for component in components:
            if component.component_type in self.runtime_functions:
                code = self.runtime_functions[component.component_type](component)
                render_code.append(code)
        
        return "\n\n".join(render_code)
    
    def _render_wallet_connector(self, component: WalletConnectorComponent) -> str:
        """Render wallet connector component"""
        return f"""
# Wallet Connector Component
st.subheader("🔗 Wallet Connector")
chains = {component.chains}
for chain in chains:
    st.success(f"✅ Connected to {{chain.upper()}}")
"""
    
    def _render_nft_license(self, component: NFTLicenseComponent) -> str:
        """Render NFT license component"""
        return f"""
# NFT License Component
st.subheader("🎫 NFT License System")
license_type = "{component.license_type}"
price = {component.price}
st.info(f"License Type: {{license_type}} - Price: {{price}} HYBRID")
if st.button("Purchase License"):
    st.success("License purchase initiated!")
""" str:
        """Render NFT license component"""
        return f"""
# NFT License Component
st.subheader("🎫 NFT License System")
st.info(f"License Type: {component.license_type.title()}")
st.info(f"Price: {component.price} {component.currency}")
if st.button("Purchase License"):
    st.success("License purchased successfully!")
"""
    
    def _render_cross_chain_bridge(self, component: CrossChainBridgeComponent) -> str:
        """Render cross-chain bridge component"""
        return f"""
# Cross-Chain Bridge Component
st.subheader("🌉 Cross-Chain Bridge")
st.selectbox("From Chain", {component.supported_chains})
st.selectbox("To Chain", {component.supported_chains})
st.selectbox("Token", {component.supported_tokens})
st.number_input("Amount", min_value=0.0)
if st.button("Bridge Tokens"):
    st.success("Bridge transaction initiated!")
"""
    
    def _render_node_operator(self, component: NodeOperatorComponent) -> str:
        """Render node operator component"""
        return f"""
# Node Operator Component
st.subheader("⚙️ Node Operator Dashboard")
st.metric("Node Type", "{component.node_type.title()}", "Active")
st.metric("NaaS Enabled", "{component.naas_enabled}")
if st.button("Claim Rewards"):
    st.success("Rewards claimed!")
"""
    
    def _render_hybrid_token(self, component: HybridTokenComponent) -> str:
        """Render HYBRID token component"""
        return f"""
# HYBRID Token Component
st.subheader("💰 HYBRID Token")
if {component.balance_display}:
    st.metric("Balance", "1,000 HYBRID", "+50")
utilities = {component.utilities}
st.write("Utilities:", ", ".join(utilities))
"""
    
    def _render_liquidity_pool(self, component: LiquidityPoolComponent) -> str:
        """Render liquidity pool component"""
        return f"""
# Liquidity Pool Component
st.subheader("💧 Liquidity Pool")
st.metric("Pair", "{component.pair}")
st.metric("APY", "{component.apy}%")
st.metric("TVL", "${component.tvl:,.0f}")
if st.button("Add Liquidity"):
    st.success("Liquidity added!")
"""
    
    def _render_staking_vault(self, component: StakingVaultComponent) -> str:
        """Render staking vault component"""
        return f"""
# Staking Vault Component
st.subheader("🏦 Staking Vault")
st.metric("Token", "{component.token}")
st.metric("APY", "{component.apy}%")
st.metric("Lock Period", "{component.lock_period} days")
if st.button("Stake Tokens"):
    st.success("Tokens staked!")
"""

class HTSXCompiler:
    """Compiler for HTSX to various target platforms"""
    
    def __init__(self):
        self.parser = HTSXParser()
        self.renderer = HTSXRenderer()
    
    def compile_to_streamlit(self, htsx_content: str) -> str:
        """Compile HTSX to Streamlit application"""
        components = self.parser.parse(htsx_content)
        return self.renderer.render_to_streamlit(components)
    
    def compile_to_react(self, htsx_content: str) -> str:
        """Compile HTSX to React components (future implementation)"""
        # TODO: Implement React compilation
        pass
    
    def validate(self, htsx_content: str) -> List[str]:
        """Validate HTSX content and return any errors"""
        errors = []
        
        # Check for required components
        if "wallet-connector" not in htsx_content:
            errors.append("Warning: No wallet connector found")
        
        # Check for malformed tags
        open_tags = re.findall(r'<(\w+(?:-\w+)*)', htsx_content)
        close_tags = re.findall(r'</(\w+(?:-\w+)*)', htsx_content)
        
        for tag in open_tags:
            if tag not in self.parser.component_registry and not htsx_content.count(f'<{tag}') == htsx_content.count(f'</{tag}>') + htsx_content.count(f'<{tag}'):
                errors.append(f"Unclosed tag: {tag}")
        
        return errors

# Export main classes
__all__ = [
    'HTSXComponent', 'WalletConnectorComponent', 'NFTLicenseComponent',
    'CrossChainBridgeComponent', 'NodeOperatorComponent', 'HybridTokenComponent',
    'LiquidityPoolComponent', 'StakingVaultComponent', 'HTSXParser', 
    'HTSXRenderer', 'HTSXCompiler', 'ComponentType'
]
