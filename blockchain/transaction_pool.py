
"""
HYBRID Blockchain Transaction Pool
Manages pending transactions and mempool
"""

import asyncio
import time
import hashlib
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json

class TransactionType(Enum):
    TRANSFER = "transfer"
    STAKE = "stake"
    UNSTAKE = "unstake"
    NFT_MINT = "nft_mint"
    NFT_TRANSFER = "nft_transfer"
    CONTRACT_CALL = "contract_call"
    BRIDGE = "bridge"
    GOVERNANCE = "governance"

@dataclass
class Transaction:
    """HYBRID blockchain transaction"""
    hash: str
    from_address: str
    to_address: str
    amount: int  # in micro-HYBRID
    fee: int
    gas_limit: int
    gas_price: int
    nonce: int
    tx_type: TransactionType
    data: str
    timestamp: float
    signature: str
    memo: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "hash": self.hash,
            "from": self.from_address,
            "to": self.to_address,
            "amount": str(self.amount),
            "fee": str(self.fee),
            "gas_limit": self.gas_limit,
            "gas_price": str(self.gas_price),
            "nonce": self.nonce,
            "type": self.tx_type.value,
            "data": self.data,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "memo": self.memo
        }

class TransactionPool:
    """Transaction pool for managing pending transactions"""
    
    def __init__(self, max_size: int = 10000):
        self.pending_transactions: Dict[str, Transaction] = {}
        self.address_nonces: Dict[str, int] = {}
        self.max_size = max_size
        self.fee_priority_queue: List[Transaction] = []
        self.transaction_cache: Dict[str, Transaction] = {}
        
    def add_transaction(self, tx: Transaction) -> bool:
        """Add transaction to pool"""
        # Check if pool is full
        if len(self.pending_transactions) >= self.max_size:
            self._evict_lowest_fee_tx()
        
        # Validate transaction
        if not self._validate_transaction(tx):
            return False
        
        # Check nonce
        expected_nonce = self.address_nonces.get(tx.from_address, 0)
        if tx.nonce != expected_nonce:
            return False
        
        # Add to pool
        self.pending_transactions[tx.hash] = tx
        self.address_nonces[tx.from_address] = tx.nonce + 1
        
        # Add to priority queue
        self._insert_by_fee(tx)
        
        return True
    
    def _validate_transaction(self, tx: Transaction) -> bool:
        """Validate transaction"""
        # Basic validation
        if tx.amount < 0 or tx.fee < 0:
            return False
        
        if tx.gas_limit <= 0 or tx.gas_price <= 0:
            return False
        
        if not tx.from_address or not tx.to_address:
            return False
        
        # Check for duplicate
        if tx.hash in self.pending_transactions:
            return False
        
        return True
    
    def _insert_by_fee(self, tx: Transaction):
        """Insert transaction in fee priority order"""
        fee_per_gas = tx.fee / tx.gas_limit
        
        # Binary search insertion
        left, right = 0, len(self.fee_priority_queue)
        while left < right:
            mid = (left + right) // 2
            mid_fee_per_gas = self.fee_priority_queue[mid].fee / self.fee_priority_queue[mid].gas_limit
            if fee_per_gas > mid_fee_per_gas:
                right = mid
            else:
                left = mid + 1
        
        self.fee_priority_queue.insert(left, tx)
    
    def _evict_lowest_fee_tx(self):
        """Remove transaction with lowest fee"""
        if not self.fee_priority_queue:
            return
        
        lowest_fee_tx = self.fee_priority_queue.pop()
        del self.pending_transactions[lowest_fee_tx.hash]
        
        # Adjust nonce
        self.address_nonces[lowest_fee_tx.from_address] -= 1
    
    def get_transactions_for_block(self, max_transactions: int = 1000, max_gas: int = 20_000_000) -> List[Transaction]:
        """Get transactions for next block"""
        selected_transactions = []
        total_gas = 0
        used_addresses = set()
        
        for tx in self.fee_priority_queue:
            # Skip if address already used in this block
            if tx.from_address in used_addresses:
                continue
            
            # Check gas limit
            if total_gas + tx.gas_limit > max_gas:
                continue
            
            # Check transaction limit
            if len(selected_transactions) >= max_transactions:
                break
            
            selected_transactions.append(tx)
            total_gas += tx.gas_limit
            used_addresses.add(tx.from_address)
        
        return selected_transactions
    
    def remove_transactions(self, tx_hashes: List[str]):
        """Remove transactions from pool (after inclusion in block)"""
        for tx_hash in tx_hashes:
            if tx_hash in self.pending_transactions:
                tx = self.pending_transactions[tx_hash]
                del self.pending_transactions[tx_hash]
                
                # Remove from priority queue
                self.fee_priority_queue = [t for t in self.fee_priority_queue if t.hash != tx_hash]
                
                # Cache transaction
                self.transaction_cache[tx_hash] = tx
    
    def get_transaction(self, tx_hash: str) -> Optional[Transaction]:
        """Get transaction by hash"""
        # Check pending first
        if tx_hash in self.pending_transactions:
            return self.pending_transactions[tx_hash]
        
        # Check cache
        return self.transaction_cache.get(tx_hash)
    
    def get_pending_count(self) -> int:
        """Get number of pending transactions"""
        return len(self.pending_transactions)
    
    def get_address_transactions(self, address: str) -> List[Transaction]:
        """Get all transactions for an address"""
        transactions = []
        
        # Pending transactions
        for tx in self.pending_transactions.values():
            if tx.from_address == address or tx.to_address == address:
                transactions.append(tx)
        
        # Cached transactions
        for tx in self.transaction_cache.values():
            if tx.from_address == address or tx.to_address == address:
                transactions.append(tx)
        
        return sorted(transactions, key=lambda x: x.timestamp, reverse=True)
    
    def get_pool_stats(self) -> Dict:
        """Get transaction pool statistics"""
        total_fees = sum(tx.fee for tx in self.pending_transactions.values())
        avg_fee = total_fees / len(self.pending_transactions) if self.pending_transactions else 0
        
        type_distribution = {}
        for tx in self.pending_transactions.values():
            tx_type = tx.tx_type.value
            type_distribution[tx_type] = type_distribution.get(tx_type, 0) + 1
        
        return {
            "pending_count": len(self.pending_transactions),
            "total_fees": total_fees,
            "average_fee": avg_fee,
            "type_distribution": type_distribution,
            "max_size": self.max_size,
            "cached_transactions": len(self.transaction_cache)
        }
    
    def cleanup_old_transactions(self, max_age_hours: int = 24):
        """Remove old transactions from pool"""
        current_time = time.time()
        cutoff_time = current_time - (max_age_hours * 3600)
        
        old_hashes = []
        for tx_hash, tx in self.pending_transactions.items():
            if tx.timestamp < cutoff_time:
                old_hashes.append(tx_hash)
        
        for tx_hash in old_hashes:
            tx = self.pending_transactions[tx_hash]
            del self.pending_transactions[tx_hash]
            self.fee_priority_queue = [t for t in self.fee_priority_queue if t.hash != tx_hash]
            
            # Adjust nonce
            self.address_nonces[tx.from_address] -= 1

def create_transaction(
    from_address: str,
    to_address: str,
    amount: int,
    fee: int,
    tx_type: TransactionType = TransactionType.TRANSFER,
    data: str = "",
    memo: str = ""
) -> Transaction:
    """Create a new transaction"""
    timestamp = time.time()
    nonce = 0  # Would be fetched from account state
    
    # Create transaction hash
    tx_data = f"{from_address}{to_address}{amount}{fee}{timestamp}{nonce}"
    tx_hash = f"0x{hashlib.sha256(tx_data.encode()).hexdigest()}"
    
    # Calculate gas
    base_gas = 21000
    gas_limit = base_gas + len(data) * 68
    gas_price = max(1, fee // gas_limit)
    
    return Transaction(
        hash=tx_hash,
        from_address=from_address,
        to_address=to_address,
        amount=amount,
        fee=fee,
        gas_limit=gas_limit,
        gas_price=gas_price,
        nonce=nonce,
        tx_type=tx_type,
        data=data,
        timestamp=timestamp,
        signature="",  # Would be actual signature
        memo=memo
    )

# Global transaction pool
transaction_pool = TransactionPool()
