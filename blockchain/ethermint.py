
#!/usr/bin/env python3
"""
Ethermint EVM subsystem for HYBRID blockchain
Provides EVM compatibility alongside Cosmos SDK
"""
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from eth_account import Account
from eth_utils import to_checksum_address
import web3
from web3 import Web3

@dataclass
class EVMTransaction:
    """EVM transaction on HYBRID chain"""
    tx_hash: str
    from_address: str
    to_address: str
    value: int
    gas_limit: int
    gas_price: int
    gas_used: int
    data: str
    block_height: int
    timestamp: str
    status: str  # "success", "failed", "pending"

@dataclass
class EVMContract:
    """Deployed EVM contract"""
    address: str
    creator: str
    bytecode: str
    abi: List[Dict]
    block_height: int
    tx_hash: str

class HybridEVMPrecompile:
    """
    Custom precompile for NFT license verification
    Deployed at address 0x000...HNL
    """
    
    ADDRESS = "0x0000000000000000000000000000000000000HNL"
    
    @staticmethod
    def verify_license(operator_address: str, license_type: str) -> bool:
        """Precompile function to verify NFT license"""
        from blockchain.x_licence import licence_module, LicenseType
        
        # Convert string to enum
        try:
            lt = LicenseType.VALIDATOR if license_type == "validator" else LicenseType.STORAGE
            return licence_module.verify_license(operator_address, lt)
        except:
            return False
    
    @staticmethod
    def get_license_info(license_id: str) -> Dict:
        """Get license information via precompile"""
        from blockchain.x_licence import licence_module
        
        info = licence_module.get_license_info(license_id)
        return info if info else {}

class EthermintSubsystem:
    """
    Ethermint EVM subsystem implementation
    Provides EVM compatibility on HYBRID blockchain
    """
    
    def __init__(self, chain_id: int = 1):
        self.chain_id = chain_id
        self.evm_height = 1  # EVM starts at block 1
        self.evm_state: Dict[str, Any] = {}
        self.contracts: Dict[str, EVMContract] = {}
        self.transactions: Dict[str, EVMTransaction] = {}
        self.precompiles = {
            HybridEVMPrecompile.ADDRESS: HybridEVMPrecompile()
        }
        
        # Gas configuration
        self.gas_config = {
            "base_gas": 21000,
            "gas_per_byte": 68,
            "gas_price_min": 1000,  # 0.001 uhybrid per gas unit
            "gas_limit_max": 10_000_000
        }
    
    def deploy_contract(self, creator: str, bytecode: str, abi: List[Dict], 
                       gas_limit: int, gas_price: int) -> Optional[str]:
        """Deploy EVM contract"""
        # Calculate contract address
        nonce = len([tx for tx in self.transactions.values() if tx.from_address == creator])
        contract_address = Web3.keccak(
            text=f"{creator}:{nonce}"
        ).hex()[:42]  # First 20 bytes as hex
        
        # Validate gas
        if gas_limit > self.gas_config["gas_limit_max"]:
            return None
        
        if gas_price < self.gas_config["gas_price_min"]:
            return None
        
        # Create contract
        contract = EVMContract(
            address=contract_address,
            creator=creator,
            bytecode=bytecode,
            abi=abi,
            block_height=self.evm_height,
            tx_hash=f"0x{hash(f'{creator}{bytecode}{self.evm_height}'):064x}"
        )
        
        self.contracts[contract_address] = contract
        
        # Create deployment transaction
        tx = EVMTransaction(
            tx_hash=contract.tx_hash,
            from_address=creator,
            to_address="",  # Empty for contract creation
            value=0,
            gas_limit=gas_limit,
            gas_price=gas_price,
            gas_used=gas_limit // 2,  # Simulate gas usage
            data=bytecode,
            block_height=self.evm_height,
            timestamp=str(time.time()),
            status="success"
        )
        
        self.transactions[tx.tx_hash] = tx
        
        print(f"📄 Contract deployed at {contract_address}")
        return contract_address
    
    def call_contract(self, caller: str, contract_address: str, function_data: str,
                     gas_limit: int, gas_price: int, value: int = 0) -> Optional[str]:
        """Call EVM contract function"""
        # Check if contract exists
        if contract_address not in self.contracts:
            # Check precompiles
            if contract_address in self.precompiles:
                return self._call_precompile(contract_address, function_data)
            return None
        
        # Create transaction
        tx_hash = f"0x{hash(f'{caller}{contract_address}{function_data}{self.evm_height}'):064x}"
        
        tx = EVMTransaction(
            tx_hash=tx_hash,
            from_address=caller,
            to_address=contract_address,
            value=value,
            gas_limit=gas_limit,
            gas_price=gas_price,
            gas_used=gas_limit // 3,  # Simulate gas usage
            data=function_data,
            block_height=self.evm_height,
            timestamp=str(time.time()),
            status="success"
        )
        
        self.transactions[tx_hash] = tx
        
        return tx_hash
    
    def _call_precompile(self, precompile_address: str, function_data: str) -> Optional[str]:
        """Call precompiled contract"""
        precompile = self.precompiles.get(precompile_address)
        if not precompile:
            return None
        
        # Simple function selector parsing
        if function_data.startswith("verify_license"):
            # Parse parameters (simplified)
            parts = function_data.split(":")
            if len(parts) >= 3:
                operator = parts[1]
                license_type = parts[2]
                result = precompile.verify_license(operator, license_type)
                return json.dumps({"result": result})
        
        return json.dumps({"error": "Unknown function"})
    
    def get_transaction(self, tx_hash: str) -> Optional[EVMTransaction]:
        """Get EVM transaction by hash"""
        return self.transactions.get(tx_hash)
    
    def get_contract(self, address: str) -> Optional[EVMContract]:
        """Get contract by address"""
        return self.contracts.get(address)
    
    def estimate_gas(self, transaction_data: Dict) -> int:
        """Estimate gas for transaction"""
        base_gas = self.gas_config["base_gas"]
        
        # Add gas for data
        data_length = len(transaction_data.get("data", ""))
        data_gas = data_length * self.gas_config["gas_per_byte"]
        
        # Contract creation costs more
        if not transaction_data.get("to"):
            base_gas *= 2
        
        return base_gas + data_gas
    
    def get_balance(self, address: str) -> int:
        """Get EVM balance (in uhybrid)"""
        # Integrate with token economics
        from blockchain.hybrid_wallet import hybrid_wallet_manager
        return hybrid_wallet_manager.get_balance(address)
    
    def advance_block(self):
        """Advance EVM block height"""
        self.evm_height += 1

# Global Ethermint subsystem
ethermint = EthermintSubsystem(chain_id=1)

# Deploy core contracts on initialization
def deploy_core_contracts():
    """Deploy core HYBRID contracts"""
    # HNL License precompile is already available at 0x000...HNL
    
    # Deploy token bridge contract (simplified)
    bridge_bytecode = "0x608060405234801561001057600080fd5b50..."  # Simplified
    bridge_abi = [
        {
            "name": "bridgeToEVM",
            "type": "function",
            "inputs": [{"name": "amount", "type": "uint256"}],
            "outputs": [{"name": "success", "type": "bool"}]
        }
    ]
    
    bridge_address = ethermint.deploy_contract(
        creator="hybrid1creator...",
        bytecode=bridge_bytecode,
        abi=bridge_abi,
        gas_limit=1_000_000,
        gas_price=1000
    )
    
    if bridge_address:
        print(f"🌉 Bridge contract deployed at {bridge_address}")

# Initialize contracts
deploy_core_contracts()

if __name__ == "__main__":
    import time
    
    print("⚡ Ethermint EVM Subsystem Demo")
    
    # Test contract deployment
    test_bytecode = "0x6080604052348015600f57600080fd5b50..."
    test_abi = [{"name": "test", "type": "function"}]
    
    contract_addr = ethermint.deploy_contract(
        creator="hybrid1test...",
        bytecode=test_bytecode,
        abi=test_abi,
        gas_limit=500_000,
        gas_price=1000
    )
    
    if contract_addr:
        print(f"✅ Test contract deployed: {contract_addr}")
        
        # Test precompile call
        result = ethermint.call_contract(
            caller="hybrid1test...",
            contract_address=HybridEVMPrecompile.ADDRESS,
            function_data="verify_license:hybrid1test...:validator",
            gas_limit=100_000,
            gas_price=1000
        )
        
        if result:
            print(f"🔍 Precompile call result: {result}")
