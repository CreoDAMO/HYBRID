
import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import grpc
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import requests
from blockchain.hybrid_wallet import hybrid_wallet_manager, get_founder_wallet
from blockchain.x_licence import licence_module, LicenseType
from blockchain.x_naas import naas_module
from blockchain.x_moe import moe_module

logger = logging.getLogger(__name__)

class NodeType(Enum):
    VALIDATOR = "validator"
    STORAGE = "storage"
    FULL = "full"

@dataclass
class NFTLicense:
    token_id: str
    owner_address: str
    node_type: NodeType
    issued_at: str
    expires_at: Optional[str] = None
    delegated_to: Optional[str] = None

@dataclass
class Transaction:
    tx_hash: str
    from_address: str
    to_address: str
    amount: int
    fee: int
    timestamp: str
    nonce: int

@dataclass
class Block:
    height: int
    hash: str
    prev_hash: str
    timestamp: str
    proposer: str
    transactions: List[Transaction]
    validator_signatures: List[str]

class HybridConsensus:
    """Tendermint-based consensus for HYBRID blockchain"""
    
    def __init__(self, node_id: str, validators: List[str]):
        self.node_id = node_id
        self.validators = validators
        self.current_height = 0
        self.validator_power = {v: 1 for v in validators}  # Equal voting power
        
        # Import real consensus
        from blockchain.consensus import TendermintConsensus, ValidatorSet
        validator_set = ValidatorSet(
            validators={v: 1 for v in validators},
            total_power=len(validators)
        )
        self.real_consensus = TendermintConsensus(node_id, validator_set)
        
    async def propose_block(self, transactions: List[Transaction]) -> Block:
        """Propose a new block"""
        prev_block = await self.get_latest_block()
        
        block = Block(
            height=prev_block.height + 1 if prev_block else 1,
            hash=self._calculate_block_hash(transactions),
            prev_hash=prev_block.hash if prev_block else "genesis",
            timestamp=str(asyncio.get_event_loop().time()),
            proposer=self.node_id,
            transactions=transactions,
            validator_signatures=[]
        )
        
        return block
    
    def _calculate_block_hash(self, transactions: List[Transaction]) -> str:
        """Calculate block hash using SHA-256"""
        content = json.dumps([tx.__dict__ for tx in transactions], sort_keys=True)
        digest = hashes.Hash(hashes.SHA256())
        digest.update(content.encode())
        return digest.finalize().hex()
    
    async def get_latest_block(self) -> Optional[Block]:
        """Get the latest block from the chain"""
        # This would connect to the actual blockchain state
        return None

class NFTLicenseManager:
    """Manages NFT licenses for node operation"""
    
    def __init__(self):
        self.licenses: Dict[str, NFTLicense] = {}
        self.delegations: Dict[str, str] = {}  # license_id -> operator_address
    
    def issue_license(self, token_id: str, owner: str, node_type: NodeType) -> NFTLicense:
        """Issue a new node license NFT"""
        license = NFTLicense(
            token_id=token_id,
            owner_address=owner,
            node_type=node_type,
            issued_at=str(asyncio.get_event_loop().time())
        )
        self.licenses[token_id] = license
        return license
    
    def verify_license(self, operator_address: str, node_type: NodeType) -> bool:
        """Verify if an address can operate a node of given type"""
        # Check direct ownership
        for license in self.licenses.values():
            if license.owner_address == operator_address and license.node_type == node_type:
                return True
        
        # Check delegations
        for license_id, delegated_operator in self.delegations.items():
            if delegated_operator == operator_address:
                license = self.licenses.get(license_id)
                if license and license.node_type == node_type:
                    return True
        
        return False
    
    def delegate_license(self, license_id: str, owner: str, operator: str) -> bool:
        """Delegate license operation to another address"""
        license = self.licenses.get(license_id)
        if not license or license.owner_address != owner:
            return False
        
        self.delegations[license_id] = operator
        license.delegated_to = operator
        return True

class CrossChainBridge:
    """Handles cross-chain interactions with Base, Polygon, and Solana"""
    
    def __init__(self):
        self.supported_chains = {
            "base": {
                "rpc": "https://mainnet.base.org",
                "chain_id": 8453,
                "wallet": "0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79"
            },
            "polygon": {
                "rpc": "https://polygon-rpc.com", 
                "chain_id": 137,
                "wallet": "0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79"
            },
            "solana": {
                "rpc": "https://api.mainnet-beta.solana.com",
                "wallet": "3E8keZHkH1AHvRfbmq44tEmBgJYz1NjkhBE41C4gJHUn"
            }
        }
    
    async def bridge_tokens(self, from_chain: str, to_chain: str, amount: int, token: str) -> str:
        """Bridge tokens between chains using Axelar/IBC"""
        if from_chain not in self.supported_chains or to_chain not in self.supported_chains:
            raise ValueError("Unsupported chain")
        
        # Simulate bridge transaction
        bridge_tx = {
            "from_chain": from_chain,
            "to_chain": to_chain,
            "amount": amount,
            "token": token,
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
        logger.info(f"Bridging {amount} {token} from {from_chain} to {to_chain}")
        return f"bridge_tx_{hash(str(bridge_tx))}"
    
    async def get_balance(self, chain: str, address: str, token: str = "native") -> int:
        """Get balance on external chain"""
        chain_config = self.supported_chains.get(chain)
        if not chain_config:
            return 0
        
        # This would integrate with actual RPC calls
        # For demo, return mock balance
        return 1000000  # 1 token with 6 decimals

class HybridTokenEconomics:
    """Manages HYBRID token economics and rewards"""
    
    def __init__(self):
        self.total_supply = 1_000_000_000 * 10**6  # 1B HYBRID with 6 decimals
        self.balances: Dict[str, int] = {}
        self.staking_pools: Dict[str, Dict] = {}
        self.validator_rewards = 0.05  # 5% annual
        self.storage_rewards = 0.03   # 3% annual
    
    def mint(self, address: str, amount: int):
        """Mint new HYBRID tokens"""
        self.balances[address] = self.balances.get(address, 0) + amount
    
    def transfer(self, from_addr: str, to_addr: str, amount: int) -> bool:
        """Transfer HYBRID tokens"""
        if self.balances.get(from_addr, 0) < amount:
            return False
        
        self.balances[from_addr] -= amount
        self.balances[to_addr] = self.balances.get(to_addr, 0) + amount
        return True
    
    def stake(self, address: str, amount: int, node_type: NodeType) -> bool:
        """Stake HYBRID tokens for node operation"""
        if self.balances.get(address, 0) < amount:
            return False
        
        self.balances[address] -= amount
        
        if address not in self.staking_pools:
            self.staking_pools[address] = {"amount": 0, "type": node_type, "rewards": 0}
        
        self.staking_pools[address]["amount"] += amount
        return True
    
    def calculate_rewards(self, address: str) -> int:
        """Calculate staking rewards"""
        stake_info = self.staking_pools.get(address)
        if not stake_info:
            return 0
        
        rate = self.validator_rewards if stake_info["type"] == NodeType.VALIDATOR else self.storage_rewards
        # Simplified daily rewards calculation
        return int(stake_info["amount"] * rate / 365)

class HTSXRuntimeEngine:
    """HTSX Runtime Engine for parsing and executing HTSX components"""
    
    def __init__(self, hybrid_node):
        self.hybrid_node = hybrid_node
        self.component_registry = {
            "wallet-connector": self._handle_wallet_connector,
            "nft-license": self._handle_nft_license,
            "cross-chain-bridge": self._handle_bridge,
            "node-operator": self._handle_node_operator,
            "hybrid-token": self._handle_hybrid_token,
            "liquidity-pool": self._handle_liquidity_pool,
            "staking-vault": self._handle_staking_vault
        }
    
    async def parse_htsx(self, htsx_content: str) -> Dict[str, Any]:
        """Parse HTSX content and extract components"""
        import re
        
        components = {}
        
        # Extract component definitions
        for component_name, handler in self.component_registry.items():
            pattern = rf'<{component_name}([^>]*?)/?>'
            matches = re.finditer(pattern, htsx_content, re.IGNORECASE)
            
            for match in matches:
                props = self._parse_props(match.group(1))
                component_data = await handler(props)
                
                if component_name not in components:
                    components[component_name] = []
                components[component_name].append(component_data)
        
        return components
    
    def _parse_props(self, props_string: str) -> Dict[str, Any]:
        """Parse component properties"""
        import re
        props = {}
        
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
    
    async def _handle_wallet_connector(self, props: Dict) -> Dict:
        """Handle wallet connector component"""
        chains = props.get('chains', ['hybrid'])
        required = props.get('required', False)
        
        return {
            "type": "wallet-connector",
            "chains": chains,
            "required": required,
            "status": "connected"
        }
    
    async def _handle_nft_license(self, props: Dict) -> Dict:
        """Handle NFT license component"""
        license_type = props.get('type', 'storage')
        price = props.get('price', 100)
        
        return {
            "type": "nft-license", 
            "license_type": license_type,
            "price": price,
            "currency": "HYBRID"
        }
    
    async def _handle_bridge(self, props: Dict) -> Dict:
        """Handle cross-chain bridge component"""
        protocol = props.get('protocol', 'axelar')
        chains = props.get('chains', ['hybrid', 'base', 'polygon'])
        
        return {
            "type": "cross-chain-bridge",
            "protocol": protocol,
            "supported_chains": chains
        }
    
    async def _handle_node_operator(self, props: Dict) -> Dict:
        """Handle node operator component"""
        node_type = props.get('type', 'storage')
        naas_enabled = props.get('naas', False)
        
        return {
            "type": "node-operator",
            "node_type": node_type,
            "naas_enabled": naas_enabled
        }
    
    async def _handle_hybrid_token(self, props: Dict) -> Dict:
        """Handle HYBRID token component"""
        utilities = props.get('utilities', ['fees', 'governance', 'staking'])
        
        return {
            "type": "hybrid-token",
            "symbol": "HYBRID",
            "utilities": utilities
        }
    
    async def _handle_liquidity_pool(self, props: Dict) -> Dict:
        """Handle liquidity pool component"""
        pair = props.get('pair', 'HYBRID/USDC')
        apy = props.get('apy', '12%')
        
        return {
            "type": "liquidity-pool",
            "pair": pair,
            "apy": apy
        }
    
    async def _handle_staking_vault(self, props: Dict) -> Dict:
        """Handle staking vault component"""
        token = props.get('token', 'HYBRID')
        apy = props.get('apy', '5%')
        
        return {
            "type": "staking-vault",
            "token": token,
            "apy": apy
        }

class HybridBlockchainNode:
    """Main HYBRID blockchain node implementation"""
    
    def __init__(self, node_id: str, node_type: NodeType):
        self.node_id = node_id
        self.node_type = node_type
        self.is_running = False
        
        # Core components
        self.consensus = HybridConsensus(node_id, [])
        self.nft_manager = NFTLicenseManager()  # Legacy, now using x/licence
        self.bridge = CrossChainBridge()
        self.token_economics = HybridTokenEconomics()
        self.htsx_runtime = HTSXRuntimeEngine(self)
        
        # Core modules (per technical spec)
        self.licence_module = licence_module
        self.naas_module = naas_module
        self.moe_module = moe_module
        
        # Initialize with founder wallet
        self.wallet_manager = hybrid_wallet_manager
        self.founder_wallet = get_founder_wallet()
        
        # Sync founder balance with token economics
        self.token_economics.balances[self.founder_wallet.address] = self.founder_wallet.balance
        
        # Blockchain state
        self.chain_state = {
            "height": 0,
            "blocks": [],
            "mempool": [],
            "validators": {},
            "accounts": {}
        }
        
        # Network
        self.peers = []
        self.rpc_port = 26657
        self.p2p_port = 26656
        
        # Import P2P networking
        from blockchain.p2p_network import P2PNetwork
        self.p2p_network = P2PNetwork(self.node_id, self.p2p_port)
    
    async def start(self):
        """Start the blockchain node"""
        logger.info(f"Starting HYBRID node {self.node_id} (type: {self.node_type.value})")
        
        # Verify NFT license using x/licence module
        license_type = LicenseType.VALIDATOR if self.node_type == NodeType.VALIDATOR else LicenseType.STORAGE
        if not self.licence_module.verify_license(self.node_id, license_type):
            raise Exception(f"No valid NFT license for {self.node_type.value} node operation")
        
        self.is_running = True
        
        # Start core services
        await asyncio.gather(
            self._start_consensus(),
            self._start_rpc_server(),
            self._start_p2p_network(),
            self._start_block_producer() if self.node_type == NodeType.VALIDATOR else self._start_sync_client()
        )
    
    async def _start_consensus(self):
        """Start consensus mechanism"""
        logger.info("Starting Tendermint consensus...")
        while self.is_running:
            await asyncio.sleep(1)  # Consensus loop
    
    async def _start_rpc_server(self):
        """Start RPC server for client connections"""
        from fastapi import FastAPI
        import uvicorn
        
        app = FastAPI(title="HYBRID Blockchain RPC")
        
        @app.get("/status")
        async def get_status():
            return {
                "node_id": self.node_id,
                "node_type": self.node_type.value,
                "height": self.chain_state["height"],
                "is_running": self.is_running
            }
        
        @app.get("/balance/{address}")
        async def get_balance(address: str):
            # Check both token economics and wallet manager
            wallet_balance = self.wallet_manager.get_balance(address)
            token_balance = self.token_economics.balances.get(address, 0)
            
            # Use wallet manager as primary source
            balance = max(wallet_balance, token_balance)
            
            return {
                "address": address,
                "balance": balance,
                "balance_hybrid": balance / 1_000_000,
                "is_founder": address == self.founder_wallet.address
            }
        
        @app.get("/wallet/{address}")
        async def get_wallet_info(address: str):
            wallet = self.wallet_manager.get_wallet(address)
            if wallet:
                return {
                    "address": wallet.address,
                    "balance": wallet.balance,
                    "balance_hybrid": wallet.balance / 1_000_000,
                    "label": wallet.label,
                    "created_at": wallet.created_at,
                    "is_founder": address == self.founder_wallet.address
                }
            return {"error": "Wallet not found"}
        
        @app.post("/wallet/create")
        async def create_wallet(wallet_data: dict):
            label = wallet_data.get("label", "")
            new_wallet = self.wallet_manager.create_new_wallet(label)
            return {
                "address": new_wallet.address,
                "mnemonic": new_wallet.mnemonic,
                "balance": new_wallet.balance,
                "label": new_wallet.label
            }
        
        @app.get("/founder")
        async def get_founder_info():
            return {
                "address": self.founder_wallet.address,
                "balance": self.founder_wallet.balance,
                "balance_hybrid": self.founder_wallet.balance / 1_000_000,
                "label": self.founder_wallet.label,
                "created_at": self.founder_wallet.created_at
            }
        
        @app.post("/tx/send")
        async def send_transaction(tx_data: dict):
            # Process transaction
            return {"tx_hash": f"hybrid_tx_{hash(str(tx_data))}"}
        
        @app.post("/htsx/execute")
        async def execute_htsx(htsx_content: dict):
            """Execute HTSX content"""
            components = await self.htsx_runtime.parse_htsx(htsx_content.get("content", ""))
            return {"components": components, "status": "executed"}
        
        config = uvicorn.Config(app, host="0.0.0.0", port=self.rpc_port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()
    
    async def _start_p2p_network(self):
        """Start P2P networking"""
        logger.info(f"Starting P2P network on port {self.p2p_port}...")
        
        # Start P2P server
        await self.p2p_network.start_server()
        
        # Connect to seed nodes (in production, these would be known peers)
        seed_nodes = [
            # ("peer1.hybrid.local", 26656),
            # ("peer2.hybrid.local", 26656)
        ]
        
        for address, port in seed_nodes:
            await self.p2p_network.connect_to_peer(address, port)
        
        # P2P maintenance loop
        while self.is_running:
            await asyncio.sleep(30)  # Ping peers every 30 seconds
            await self.p2p_network.ping_peers()
    
    async def _start_block_producer(self):
        """Start block production (validators only)"""
        if self.node_type != NodeType.VALIDATOR:
            return
        
        logger.info("Starting block producer...")
        while self.is_running:
            # Produce blocks every 6 seconds
            await asyncio.sleep(6)
            
            if self.chain_state["mempool"]:
                transactions = self.chain_state["mempool"][:100]  # Max 100 tx per block
                block = await self.consensus.propose_block(transactions)
                
                self.chain_state["blocks"].append(block)
                self.chain_state["height"] = block.height
                self.chain_state["mempool"] = self.chain_state["mempool"][100:]
                
                logger.info(f"Produced block {block.height} with {len(transactions)} transactions")
    
    async def _start_sync_client(self):
        """Start blockchain sync (non-validators)"""
        logger.info("Starting blockchain sync...")
        while self.is_running:
            await asyncio.sleep(2)  # Sync loop
    
    async def stop(self):
        """Stop the blockchain node"""
        logger.info(f"Stopping HYBRID node {self.node_id}")
        self.is_running = False

# Factory function to create different node types
def create_hybrid_node(node_type: str = "storage") -> HybridBlockchainNode:
    """Create a HYBRID blockchain node"""
    import uuid
    
    node_id = f"hybrid_{uuid.uuid4().hex[:8]}"
    node_type_enum = NodeType(node_type)
    
    node = HybridBlockchainNode(node_id, node_type_enum)
    
    # Issue demo NFT license
    node.nft_manager.issue_license(
        token_id=f"license_{node_id}",
        owner=node_id,
        node_type=node_type_enum
    )
    
    return node

if __name__ == "__main__":
    async def main():
        # Create and start a storage node
        node = create_hybrid_node("storage")
        await node.start()
    
    asyncio.run(main())
