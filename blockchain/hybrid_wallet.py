"""
HYBRID Blockchain Wallet System
Native wallet management for the HYBRID blockchain
"""

import hashlib
import secrets
from typing import Dict, List, Optional
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ed25519

@dataclass
class HybridWallet:
    """HYBRID blockchain wallet"""
    address: str
    private_key: str
    public_key: str
    balance: float = 0.0
    mnemonic: Optional[str] = None

class HybridWalletManager:
    """Manages HYBRID blockchain wallets"""

    def __init__(self):
        self.wallets: Dict[str, HybridWallet] = {}
        self.founder_wallet = self._create_founder_wallet()

    def _create_founder_wallet(self) -> HybridWallet:
        """Create the founder wallet with pre-funded balance"""
        # Generate founder wallet
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        # Create HYBRID address (bech32 format)
        address = f"hybrid1{hashlib.sha256(public_key.public_bytes_raw()).hexdigest()[:39]}"

        wallet = HybridWallet(
            address=address,
            private_key=private_key.private_bytes_raw().hex(),
            public_key=public_key.public_bytes_raw().hex(),
            balance=100_000_000_000,  # 100B HYBRID tokens
            mnemonic="hybrid founder genesis wallet secure blockchain network tokens"
        )

        self.wallets[address] = wallet
        return wallet

    def create_wallet(self) -> HybridWallet:
        """Create a new HYBRID wallet"""
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        address = f"hybrid1{hashlib.sha256(public_key.public_bytes_raw()).hexdigest()[:39]}"

        wallet = HybridWallet(
            address=address,
            private_key=private_key.private_bytes_raw().hex(),
            public_key=public_key.public_bytes_raw().hex(),
            balance=0.0
        )

        self.wallets[address] = wallet
        return wallet

    def get_wallet(self, address: str) -> Optional[HybridWallet]:
        """Get wallet by address"""
        return self.wallets.get(address)

    def transfer(self, from_address: str, to_address: str, amount: float) -> bool:
        """Transfer HYBRID coins between wallets"""
        from_wallet = self.wallets.get(from_address)
        to_wallet = self.wallets.get(to_address)

        if not from_wallet or not to_wallet:
            return False

        if from_wallet.balance < amount:
            return False

        from_wallet.balance -= amount
        to_wallet.balance += amount
        return True

# Global wallet manager
hybrid_wallet_manager = HybridWalletManager()

def get_founder_wallet() -> HybridWallet:
    """Get the founder wallet"""
    return hybrid_wallet_manager.founder_wallet

def create_hybrid_wallet() -> HybridWallet:
    """Create a new HYBRID wallet"""
    return hybrid_wallet_manager.create_wallet()