
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json

class ComponentType(Enum):
    WALLET_CONNECTOR = "wallet-connector"
    NFT_LICENSE = "nft-license"
    NODE_OPERATOR = "node-operator"
    CROSS_CHAIN_BRIDGE = "cross-chain-bridge"
    HYBRID_TOKEN = "hybrid-token"
    GOVERNANCE = "governance"
    STAKING = "staking"

@dataclass
class HybridComponent:
    type: ComponentType
    props: Dict[str, Any]
    children: List['HybridComponent'] = None

class HybridHTSXParser:
    """Parser for HTSX components specific to HYBRID Blockchain"""
    
    def __init__(self):
        self.components = []
        self.state = {}
    
    def parse_component(self, tag: str, props: Dict[str, Any]) -> HybridComponent:
        """Parse HTSX tag into HYBRID component"""
        
        component_map = {
            "wallet-connector": ComponentType.WALLET_CONNECTOR,
            "nft-license": ComponentType.NFT_LICENSE,
            "node-operator": ComponentType.NODE_OPERATOR,
            "cross-chain-bridge": ComponentType.CROSS_CHAIN_BRIDGE,
            "hybrid-token": ComponentType.HYBRID_TOKEN,
            "governance": ComponentType.GOVERNANCE,
            "staking": ComponentType.STAKING
        }
        
        component_type = component_map.get(tag, ComponentType.WALLET_CONNECTOR)
        return HybridComponent(type=component_type, props=props)
    
    def render_wallet_connector(self, component: HybridComponent) -> str:
        """Render wallet connector component"""
        chains = component.props.get('chains', 'hybrid').split(',')
        required = component.props.get('required', False)
        
        return f"""
        <div class="wallet-connector">
            <h3>Multi-Chain Wallet Connection</h3>
            <div class="chains">
                {' '.join([f'<button class="chain-btn">{chain.title()}</button>' for chain in chains])}
            </div>
            {'<p class="required">Wallet connection required</p>' if required else ''}
        </div>
        """
    
    def render_nft_license(self, component: HybridComponent) -> str:
        """Render NFT license component"""
        license_type = component.props.get('type', 'storage')
        price = component.props.get('price', '100')
        currency = component.props.get('currency', 'HYBRID')
        
        return f"""
        <div class="nft-license">
            <h3>{license_type.title()} Node License</h3>
            <div class="license-info">
                <p>Price: {price} {currency}</p>
                <p>Type: {license_type.title()} Node</p>
                <button class="purchase-btn">Purchase License</button>
            </div>
        </div>
        """
    
    def render_node_operator(self, component: HybridComponent) -> str:
        """Render node operator component"""
        node_type = component.props.get('type', 'storage')
        naas = component.props.get('naas', False)
        
        return f"""
        <div class="node-operator">
            <h3>{node_type.title()} Node Dashboard</h3>
            <div class="node-stats">
                <div class="stat">
                    <label>Status:</label>
                    <span class="status active">Active</span>
                </div>
                <div class="stat">
                    <label>Uptime:</label>
                    <span>99.9%</span>
                </div>
                <div class="stat">
                    <label>Rewards:</label>
                    <span>50 HYBRID/day</span>
                </div>
            </div>
            {'<p class="naas-info">NaaS enabled - Passive rewards active</p>' if naas else ''}
        </div>
        """
    
    def render_cross_chain_bridge(self, component: HybridComponent) -> str:
        """Render cross-chain bridge component"""
        protocol = component.props.get('protocol', 'axelar')
        chains = component.props.get('chains', 'hybrid,base').split(',')
        
        return f"""
        <div class="cross-chain-bridge">
            <h3>Cross-Chain Bridge ({protocol.title()})</h3>
            <div class="bridge-form">
                <select class="from-chain">
                    {' '.join([f'<option value="{chain}">{chain.title()}</option>' for chain in chains])}
                </select>
                <span class="arrow">→</span>
                <select class="to-chain">
                    {' '.join([f'<option value="{chain}">{chain.title()}</option>' for chain in chains])}
                </select>
                <input type="number" placeholder="Amount" class="amount-input" />
                <button class="bridge-btn">Bridge Tokens</button>
            </div>
        </div>
        """
    
    def render_hybrid_token(self, component: HybridComponent) -> str:
        """Render HYBRID token component"""
        utilities = component.props.get('utilities', 'fees,governance').split(',')
        balance = component.props.get('balance', '0')
        
        return f"""
        <div class="hybrid-token">
            <h3>$HYBRID Token</h3>
            <div class="token-info">
                <p class="balance">Balance: {balance} HYBRID</p>
                <div class="utilities">
                    <h4>Token Utilities:</h4>
                    <ul>
                        {' '.join([f'<li>{utility.title()}</li>' for utility in utilities])}
                    </ul>
                </div>
            </div>
        </div>
        """
    
    def render_component(self, component: HybridComponent) -> str:
        """Render any HYBRID component"""
        renderers = {
            ComponentType.WALLET_CONNECTOR: self.render_wallet_connector,
            ComponentType.NFT_LICENSE: self.render_nft_license,
            ComponentType.NODE_OPERATOR: self.render_node_operator,
            ComponentType.CROSS_CHAIN_BRIDGE: self.render_cross_chain_bridge,
            ComponentType.HYBRID_TOKEN: self.render_hybrid_token
        }
        
        renderer = renderers.get(component.type, lambda x: "Unknown component")
        return renderer(component)

class HybridBlockchainAPI:
    """API for interacting with HYBRID Blockchain from HTSX"""
    
    def __init__(self):
        self.wallets = {
            'hybrid': 'hybrid1q2w3e4r5t6y7u8i9o0p',
            'base': '0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79',
            'polygon': '0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79',
            'solana': '3E8keZHkH1AHvRfbmq44tEmBgJYz1NjkhBE41C4gJHUn'
        }
        self.rpc_endpoints = {
            'hybrid': 'http://localhost:26657',
            'base': 'https://mainnet.base.org',
            'polygon': 'https://polygon-rpc.com',
            'solana': 'https://api.mainnet-beta.solana.com'
        }
    
    def connect_wallet(self, chain: str) -> Dict[str, Any]:
        """Connect to wallet on specified chain"""
        return {
            'success': True,
            'address': self.wallets.get(chain),
            'chain': chain,
            'rpc': self.rpc_endpoints.get(chain)
        }
    
    def get_nft_licenses(self, address: str) -> List[Dict[str, Any]]:
        """Get NFT licenses owned by address"""
        return [
            {
                'id': 'storage_license_1',
                'type': 'storage',
                'active': True,
                'rewards_earned': '1500 HYBRID'
            }
        ]
    
    def purchase_nft_license(self, license_type: str, price: int) -> Dict[str, Any]:
        """Purchase NFT license"""
        return {
            'success': True,
            'transaction_hash': '0x1234567890abcdef',
            'license_id': f'{license_type}_license_{len(self.get_nft_licenses("dummy")) + 1}',
            'cost': f'{price} HYBRID'
        }
    
    def get_node_stats(self, license_id: str) -> Dict[str, Any]:
        """Get node statistics"""
        return {
            'uptime': 99.9,
            'daily_rewards': 50,
            'total_transactions': 1234,
            'status': 'active',
            'naas_enabled': True
        }
    
    def bridge_tokens(self, from_chain: str, to_chain: str, amount: float, token: str) -> Dict[str, Any]:
        """Bridge tokens between chains"""
        return {
            'success': True,
            'transaction_hash': '0xabcdef1234567890',
            'from_chain': from_chain,
            'to_chain': to_chain,
            'amount': amount,
            'token': token,
            'estimated_time': '5-10 minutes'
        }

# Export for use in main application
__all__ = ['HybridHTSXParser', 'HybridBlockchainAPI', 'ComponentType', 'HybridComponent']
