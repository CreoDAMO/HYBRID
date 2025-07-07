
"""
HYBRID Blockchain Wallet Manager
Advanced wallet management with multi-chain support
"""

import hashlib
import secrets
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519
import mnemonic

@dataclass
class TransactionHistory:
    """Transaction history entry"""
    tx_hash: str
    timestamp: str
    from_address: str
    to_address: str
    amount: float
    fee: float
    status: str
    block_height: int
    memo: str = ""

@dataclass
class WalletMetrics:
    """Wallet performance metrics"""
    total_transactions: int
    total_sent: float
    total_received: float
    average_fee: float
    first_transaction: str
    last_transaction: str
    staking_rewards: float
    nft_count: int

class AdvancedHybridWallet:
    """Advanced HYBRID wallet with full feature set"""
    
    def __init__(self, address: str, private_key: str, public_key: str, mnemonic_phrase: str):
        self.address = address
        self.private_key = private_key
        self.public_key = public_key
        self.mnemonic = mnemonic_phrase
        self.balance = 0.0
        self.label = ""
        self.created_at = datetime.now().isoformat()
        self.is_hardware_wallet = False
        self.is_multisig = False
        self.transaction_history: List[TransactionHistory] = []
        self.staked_amount = 0.0
        self.pending_rewards = 0.0
        self.nft_licenses: List[str] = []
        self.connected_dapps: List[str] = []
        
    def add_transaction(self, tx: TransactionHistory):
        """Add transaction to history"""
        self.transaction_history.append(tx)
        self.transaction_history.sort(key=lambda x: x.timestamp, reverse=True)
        
    def get_metrics(self) -> WalletMetrics:
        """Calculate wallet metrics"""
        if not self.transaction_history:
            return WalletMetrics(0, 0.0, 0.0, 0.0, "", "", 0.0, 0)
        
        total_sent = sum(tx.amount for tx in self.transaction_history if tx.from_address == self.address)
        total_received = sum(tx.amount for tx in self.transaction_history if tx.to_address == self.address)
        average_fee = sum(tx.fee for tx in self.transaction_history) / len(self.transaction_history)
        
        return WalletMetrics(
            total_transactions=len(self.transaction_history),
            total_sent=total_sent,
            total_received=total_received,
            average_fee=average_fee,
            first_transaction=self.transaction_history[-1].timestamp if self.transaction_history else "",
            last_transaction=self.transaction_history[0].timestamp if self.transaction_history else "",
            staking_rewards=self.pending_rewards,
            nft_count=len(self.nft_licenses)
        )
    
    def export_data(self) -> Dict[str, Any]:
        """Export wallet data"""
        return {
            "address": self.address,
            "mnemonic": self.mnemonic,
            "label": self.label,
            "created_at": self.created_at,
            "balance": self.balance,
            "staked_amount": self.staked_amount,
            "transaction_count": len(self.transaction_history),
            "nft_licenses": self.nft_licenses
        }

class WalletManager:
    """Comprehensive wallet management system"""
    
    def __init__(self):
        self.wallets: Dict[str, AdvancedHybridWallet] = {}
        self.founder_address = ""
        self.mnemonic_generator = mnemonic.Mnemonic("english")
        self._initialize_founder_wallet()
        
    def _initialize_founder_wallet(self):
        """Initialize the founder wallet"""
        # Generate founder wallet with specific seed
        founder_mnemonic = "hybrid founder genesis wallet secure blockchain network tokens ecosystem development innovation"
        seed = self.mnemonic_generator.to_seed(founder_mnemonic)
        
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed[:32])
        public_key = private_key.public_key()
        
        address = f"hybrid1{hashlib.sha256(public_key.public_bytes_raw()).hexdigest()[:39]}"
        
        founder_wallet = AdvancedHybridWallet(
            address=address,
            private_key=private_key.private_bytes_raw().hex(),
            public_key=public_key.public_bytes_raw().hex(),
            mnemonic_phrase=founder_mnemonic
        )
        
        founder_wallet.label = "👑 Founder Wallet"
        founder_wallet.balance = 100_000_000 * 1_000_000  # 100M HYBRID in micro-HYBRID
        
        self.wallets[address] = founder_wallet
        self.founder_address = address
        
    def create_wallet(self, label: str = "") -> AdvancedHybridWallet:
        """Create a new HYBRID wallet"""
        # Generate new mnemonic
        mnemonic_phrase = self.mnemonic_generator.generate(strength=256)
        seed = self.mnemonic_generator.to_seed(mnemonic_phrase)
        
        # Generate keys
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed[:32])
        public_key = private_key.public_key()
        
        # Generate address
        address = f"hybrid1{hashlib.sha256(public_key.public_bytes_raw()).hexdigest()[:39]}"
        
        wallet = AdvancedHybridWallet(
            address=address,
            private_key=private_key.private_bytes_raw().hex(),
            public_key=public_key.public_bytes_raw().hex(),
            mnemonic_phrase=mnemonic_phrase
        )
        
        wallet.label = label or f"Wallet {len(self.wallets) + 1}"
        self.wallets[address] = wallet
        
        return wallet
    
    def import_wallet(self, mnemonic_phrase: str, label: str = "") -> AdvancedHybridWallet:
        """Import wallet from mnemonic"""
        if not self.mnemonic_generator.check(mnemonic_phrase):
            raise ValueError("Invalid mnemonic phrase")
        
        seed = self.mnemonic_generator.to_seed(mnemonic_phrase)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed[:32])
        public_key = private_key.public_key()
        
        address = f"hybrid1{hashlib.sha256(public_key.public_bytes_raw()).hexdigest()[:39]}"
        
        if address in self.wallets:
            return self.wallets[address]
        
        wallet = AdvancedHybridWallet(
            address=address,
            private_key=private_key.private_bytes_raw().hex(),
            public_key=public_key.public_bytes_raw().hex(),
            mnemonic_phrase=mnemonic_phrase
        )
        
        wallet.label = label or "Imported Wallet"
        self.wallets[address] = wallet
        
        return wallet
    
    def get_wallet(self, address: str) -> Optional[AdvancedHybridWallet]:
        """Get wallet by address"""
        return self.wallets.get(address)
    
    def list_wallets(self) -> List[AdvancedHybridWallet]:
        """List all wallets"""
        return list(self.wallets.values())
    
    def get_founder_wallet(self) -> AdvancedHybridWallet:
        """Get the founder wallet"""
        return self.wallets[self.founder_address]
    
    def transfer(self, from_address: str, to_address: str, amount: int, memo: str = "") -> bool:
        """Transfer HYBRID between wallets"""
        from_wallet = self.get_wallet(from_address)
        to_wallet = self.get_wallet(to_address)
        
        if not from_wallet:
            return False
        
        if from_wallet.balance < amount:
            return False
        
        # Create transaction
        tx_hash = f"0x{hashlib.sha256(f'{from_address}{to_address}{amount}{datetime.now()}'.encode()).hexdigest()[:16]}"
        fee = max(1000, int(amount * 0.001))  # 0.1% fee, minimum 1000 micro-HYBRID
        
        # Update balances
        from_wallet.balance -= (amount + fee)
        if to_wallet:
            to_wallet.balance += amount
        
        # Add to transaction history
        tx = TransactionHistory(
            tx_hash=tx_hash,
            timestamp=datetime.now().isoformat(),
            from_address=from_address,
            to_address=to_address,
            amount=amount / 1_000_000,  # Convert to HYBRID
            fee=fee / 1_000_000,
            status="confirmed",
            block_height=0,  # Would be actual block height
            memo=memo
        )
        
        from_wallet.add_transaction(tx)
        if to_wallet:
            to_wallet.add_transaction(tx)
        
        return True
    
    def get_balance_hybrid(self, address: str) -> float:
        """Get balance in HYBRID (not micro-HYBRID)"""
        wallet = self.get_wallet(address)
        return wallet.balance / 1_000_000 if wallet else 0.0
    
    def stake_tokens(self, address: str, amount: int) -> bool:
        """Stake HYBRID tokens"""
        wallet = self.get_wallet(address)
        if not wallet or wallet.balance < amount:
            return False
        
        wallet.balance -= amount
        wallet.staked_amount += amount
        return True
    
    def add_nft_license(self, address: str, license_id: str):
        """Add NFT license to wallet"""
        wallet = self.get_wallet(address)
        if wallet:
            wallet.nft_licenses.append(license_id)

# Global wallet manager instance
wallet_manager = WalletManager()

# Export functions for compatibility
def get_founder_wallet() -> AdvancedHybridWallet:
    return wallet_manager.get_founder_wallet()

def create_hybrid_wallet(label: str = "") -> AdvancedHybridWallet:
    return wallet_manager.create_wallet(label)
