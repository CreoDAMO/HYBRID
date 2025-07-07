
"""
HYBRID Blockchain Block Producer
Handles block creation and validation
"""

import asyncio
import time
import hashlib
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from blockchain.transaction_pool import transaction_pool, Transaction

@dataclass
class BlockHeader:
    """Block header structure"""
    height: int
    hash: str
    previous_hash: str
    merkle_root: str
    timestamp: float
    validator: str
    signature: str
    gas_limit: int
    gas_used: int
    transactions_count: int

@dataclass
class Block:
    """Complete block structure"""
    header: BlockHeader
    transactions: List[Transaction]
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            "header": asdict(self.header),
            "transactions": [tx.to_dict() for tx in self.transactions]
        }

class BlockProducer:
    """Handles block production for HYBRID blockchain"""
    
    def __init__(self, validator_address: str):
        self.validator_address = validator_address
        self.current_height = 0
        self.previous_hash = "0x0"
        self.target_block_time = 6.0  # 6 seconds
        self.max_block_size = 1_000_000  # 1MB
        self.max_gas_limit = 20_000_000
        self.blocks_produced = 0
        self.total_gas_used = 0
        
    async def produce_block(self) -> Optional[Block]:
        """Produce a new block"""
        try:
            # Get transactions from pool
            transactions = transaction_pool.get_transactions_for_block(
                max_transactions=1000,
                max_gas=self.max_gas_limit
            )
            
            # Calculate gas used
            gas_used = sum(tx.gas_limit for tx in transactions)
            
            # Create merkle root
            merkle_root = self._calculate_merkle_root(transactions)
            
            # Create block header
            header = BlockHeader(
                height=self.current_height + 1,
                hash="",  # Will be calculated
                previous_hash=self.previous_hash,
                merkle_root=merkle_root,
                timestamp=time.time(),
                validator=self.validator_address,
                signature="",  # Would be actual signature
                gas_limit=self.max_gas_limit,
                gas_used=gas_used,
                transactions_count=len(transactions)
            )
            
            # Calculate block hash
            header.hash = self._calculate_block_hash(header)
            header.signature = self._sign_block(header)
            
            # Create block
            block = Block(header=header, transactions=transactions)
            
            # Update state
            self.current_height += 1
            self.previous_hash = header.hash
            self.blocks_produced += 1
            self.total_gas_used += gas_used
            
            # Remove transactions from pool
            tx_hashes = [tx.hash for tx in transactions]
            transaction_pool.remove_transactions(tx_hashes)
            
            return block
            
        except Exception as e:
            print(f"Error producing block: {e}")
            return None
    
    def _calculate_merkle_root(self, transactions: List[Transaction]) -> str:
        """Calculate merkle root of transactions"""
        if not transactions:
            return "0x0"
        
        # Simple merkle root calculation (in production, use proper merkle tree)
        tx_hashes = [tx.hash for tx in transactions]
        combined = "".join(tx_hashes)
        return f"0x{hashlib.sha256(combined.encode()).hexdigest()}"
    
    def _calculate_block_hash(self, header: BlockHeader) -> str:
        """Calculate block hash"""
        header_data = {
            "height": header.height,
            "previous_hash": header.previous_hash,
            "merkle_root": header.merkle_root,
            "timestamp": header.timestamp,
            "validator": header.validator,
            "gas_used": header.gas_used
        }
        
        header_json = json.dumps(header_data, sort_keys=True)
        return f"0x{hashlib.sha256(header_json.encode()).hexdigest()}"
    
    def _sign_block(self, header: BlockHeader) -> str:
        """Sign block header"""
        # In production, this would use the validator's private key
        signature_data = f"{header.hash}{header.validator}{header.timestamp}"
        return f"0x{hashlib.sha256(signature_data.encode()).hexdigest()[:32]}"
    
    def validate_block(self, block: Block) -> bool:
        """Validate a block"""
        try:
            header = block.header
            
            # Check height
            if header.height != self.current_height + 1:
                return False
            
            # Check previous hash
            if header.previous_hash != self.previous_hash:
                return False
            
            # Check transaction count
            if header.transactions_count != len(block.transactions):
                return False
            
            # Check merkle root
            calculated_merkle = self._calculate_merkle_root(block.transactions)
            if header.merkle_root != calculated_merkle:
                return False
            
            # Check gas limit
            total_gas = sum(tx.gas_limit for tx in block.transactions)
            if total_gas != header.gas_used:
                return False
            
            if header.gas_used > header.gas_limit:
                return False
            
            # Check block hash
            calculated_hash = self._calculate_block_hash(header)
            if header.hash != calculated_hash:
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating block: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get block producer statistics"""
        return {
            "current_height": self.current_height,
            "blocks_produced": self.blocks_produced,
            "total_gas_used": self.total_gas_used,
            "validator_address": self.validator_address,
            "target_block_time": self.target_block_time,
            "max_gas_limit": self.max_gas_limit
        }

class BlockchainState:
    """Manages blockchain state"""
    
    def __init__(self):
        self.blocks: Dict[int, Block] = {}
        self.block_hashes: Dict[str, int] = {}
        self.latest_block: Optional[Block] = None
        self.total_supply = 100_000_000_000 * 1_000_000  # 100B HYBRID in micro-HYBRID
        self.circulating_supply = 75_000_000_000 * 1_000_000  # 75B HYBRID
        
    def add_block(self, block: Block) -> bool:
        """Add block to blockchain"""
        try:
            height = block.header.height
            block_hash = block.header.hash
            
            # Store block
            self.blocks[height] = block
            self.block_hashes[block_hash] = height
            self.latest_block = block
            
            # Process transactions
            self._process_block_transactions(block)
            
            return True
            
        except Exception as e:
            print(f"Error adding block: {e}")
            return False
    
    def _process_block_transactions(self, block: Block):
        """Process transactions in block"""
        for tx in block.transactions:
            # In production, this would update account balances,
            # execute smart contracts, etc.
            pass
    
    def get_block_by_height(self, height: int) -> Optional[Block]:
        """Get block by height"""
        return self.blocks.get(height)
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Block]:
        """Get block by hash"""
        height = self.block_hashes.get(block_hash)
        return self.blocks.get(height) if height is not None else None
    
    def get_latest_block(self) -> Optional[Block]:
        """Get latest block"""
        return self.latest_block
    
    def get_blockchain_stats(self) -> Dict:
        """Get blockchain statistics"""
        total_transactions = sum(len(block.transactions) for block in self.blocks.values())
        total_gas_used = sum(block.header.gas_used for block in self.blocks.values())
        
        return {
            "total_blocks": len(self.blocks),
            "total_transactions": total_transactions,
            "total_gas_used": total_gas_used,
            "latest_height": self.latest_block.header.height if self.latest_block else 0,
            "total_supply": self.total_supply,
            "circulating_supply": self.circulating_supply
        }

# Global blockchain state
blockchain_state = BlockchainState()

async def start_block_production(validator_address: str, block_time: float = 6.0):
    """Start block production loop"""
    producer = BlockProducer(validator_address)
    
    print(f"🚀 Starting block production with validator {validator_address}")
    
    while True:
        try:
            start_time = time.time()
            
            # Produce block
            block = await producer.produce_block()
            
            if block:
                # Add to blockchain
                success = blockchain_state.add_block(block)
                
                if success:
                    print(f"📦 Block {block.header.height} produced with {len(block.transactions)} transactions")
                else:
                    print(f"❌ Failed to add block {block.header.height}")
            
            # Wait for next block time
            elapsed = time.time() - start_time
            sleep_time = max(0, block_time - elapsed)
            await asyncio.sleep(sleep_time)
            
        except Exception as e:
            print(f"Error in block production: {e}")
            await asyncio.sleep(1)
