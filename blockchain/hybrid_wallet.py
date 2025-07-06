
#!/usr/bin/env python3
import hashlib
import secrets
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bech32
from typing import Dict, List, Optional, Tuple
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class HybridWallet:
    """HYBRID Blockchain native wallet"""
    address: str
    private_key: str
    public_key: str
    mnemonic: str
    balance: int = 0  # in micro-HYBRID (1 HYBRID = 1,000,000 micro-HYBRID)
    label: str = ""
    created_at: str = ""

class HybridWalletManager:
    """Manages HYBRID blockchain native wallets"""
    
    def __init__(self):
        self.wallets: Dict[str, HybridWallet] = {}
        self.founder_address = None
        self._initialize_founder_wallet()
    
    def _initialize_founder_wallet(self):
        """Initialize the founder wallet with pre-funded HYBRID tokens"""
        # Create founder wallet with fixed seed for consistency
        founder_seed = "hybrid blockchain founder lead engineer developer genesis wallet seed phrase"
        founder_wallet = self.create_wallet_from_seed(
            seed_phrase=founder_seed,
            label="🚀 HYBRID Founder - Lead Engineer & Developer"
        )
        
        # Pre-fund with initial supply allocation
        founder_initial_supply = 100_000_000 * 1_000_000  # 100M HYBRID tokens
        founder_wallet.balance = founder_initial_supply
        
        self.founder_address = founder_wallet.address
        self.wallets[founder_wallet.address] = founder_wallet
        
        print(f"✅ Founder wallet initialized: {founder_wallet.address}")
        print(f"💰 Pre-funded with: {founder_initial_supply / 1_000_000:,.0f} HYBRID")
    
    def generate_mnemonic(self) -> str:
        """Generate a 24-word mnemonic phrase"""
        # Simplified mnemonic generation for demo
        wordlist = [
            "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
            "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
            "acoustic", "acquire", "across", "action", "actor", "actress", "actual", "adapt",
            "add", "addict", "address", "adjust", "admit", "adult", "advance", "advice",
            "aerobic", "affair", "afford", "afraid", "again", "against", "age", "agent",
            "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
            "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
            "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among"
        ]
        
        words = []
        for _ in range(24):
            words.append(secrets.choice(wordlist))
        
        return " ".join(words)
    
    def create_wallet_from_seed(self, seed_phrase: str, label: str = "") -> HybridWallet:
        """Create wallet from seed phrase"""
        # Generate private key from seed
        seed_bytes = seed_phrase.encode('utf-8')
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
            hashlib.sha256(seed_bytes).digest()[:32]
        )
        
        # Get public key
        public_key = private_key.public_key()
        
        # Generate HYBRID address (bech32 with 'hybrid' prefix)
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Create bech32 address
        address = self._create_bech32_address(public_key_bytes)
        
        # Encode keys for storage
        private_key_hex = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        ).hex()
        
        public_key_hex = public_key_bytes.hex()
        
        wallet = HybridWallet(
            address=address,
            private_key=private_key_hex,
            public_key=public_key_hex,
            mnemonic=seed_phrase,
            label=label,
            created_at=datetime.now().isoformat()
        )
        
        return wallet
    
    def create_new_wallet(self, label: str = "") -> HybridWallet:
        """Create a new HYBRID wallet with random mnemonic"""
        mnemonic = self.generate_mnemonic()
        wallet = self.create_wallet_from_seed(mnemonic, label)
        self.wallets[wallet.address] = wallet
        return wallet
    
    def _create_bech32_address(self, public_key_bytes: bytes) -> str:
        """Create bech32 address with 'hybrid' prefix"""
        # Hash the public key
        hash_obj = hashlib.sha256(public_key_bytes).digest()
        ripemd_hash = hashlib.new('ripemd160', hash_obj).digest()
        
        # Convert to 5-bit groups for bech32
        converted = bech32.convertbits(ripemd_hash, 8, 5)
        
        # Create bech32 address
        address = bech32.bech32_encode('hybrid', converted)
        return address
    
    def get_wallet(self, address: str) -> Optional[HybridWallet]:
        """Get wallet by address"""
        return self.wallets.get(address)
    
    def get_founder_wallet(self) -> HybridWallet:
        """Get the founder wallet"""
        return self.wallets[self.founder_address]
    
    def list_wallets(self) -> List[HybridWallet]:
        """List all wallets"""
        return list(self.wallets.values())
    
    def transfer(self, from_address: str, to_address: str, amount: int) -> bool:
        """Transfer HYBRID tokens between wallets"""
        from_wallet = self.get_wallet(from_address)
        to_wallet = self.get_wallet(to_address)
        
        if not from_wallet:
            return False
        
        if from_wallet.balance < amount:
            return False
        
        # Deduct from sender
        from_wallet.balance -= amount
        
        # Add to receiver (create wallet if doesn't exist)
        if not to_wallet:
            # Create basic wallet entry for external address
            to_wallet = HybridWallet(
                address=to_address,
                private_key="",
                public_key="",
                mnemonic="",
                balance=amount
            )
            self.wallets[to_address] = to_wallet
        else:
            to_wallet.balance += amount
        
        return True
    
    def get_balance(self, address: str) -> int:
        """Get wallet balance in micro-HYBRID"""
        wallet = self.get_wallet(address)
        return wallet.balance if wallet else 0
    
    def get_balance_hybrid(self, address: str) -> float:
        """Get wallet balance in HYBRID (decimal)"""
        return self.get_balance(address) / 1_000_000
    
    def export_wallet(self, address: str) -> Optional[Dict]:
        """Export wallet data"""
        wallet = self.get_wallet(address)
        if wallet:
            return asdict(wallet)
        return None
    
    def save_wallets(self, filepath: str = "hybrid_wallets.json"):
        """Save wallets to file"""
        wallet_data = {addr: asdict(wallet) for addr, wallet in self.wallets.items()}
        with open(filepath, 'w') as f:
            json.dump(wallet_data, f, indent=2)
    
    def load_wallets(self, filepath: str = "hybrid_wallets.json"):
        """Load wallets from file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                wallet_data = json.load(f)
            
            for addr, data in wallet_data.items():
                self.wallets[addr] = HybridWallet(**data)

# Global wallet manager instance
hybrid_wallet_manager = HybridWalletManager()

def get_founder_wallet() -> HybridWallet:
    """Get the founder wallet"""
    return hybrid_wallet_manager.get_founder_wallet()

def create_hybrid_wallet(label: str = "") -> HybridWallet:
    """Create a new HYBRID wallet"""
    return hybrid_wallet_manager.create_new_wallet(label)

def get_hybrid_balance(address: str) -> float:
    """Get HYBRID balance for address"""
    return hybrid_wallet_manager.get_balance_hybrid(address)

if __name__ == "__main__":
    # Demo wallet creation
    print("🚀 HYBRID Blockchain Wallet System")
    print("=" * 50)
    
    # Show founder wallet
    founder = get_founder_wallet()
    print(f"👑 Founder Wallet: {founder.address}")
    print(f"💰 Balance: {founder.balance / 1_000_000:,.0f} HYBRID")
    print(f"🏷️ Label: {founder.label}")
    
    # Create a new wallet
    print("\n📱 Creating new wallet...")
    new_wallet = create_hybrid_wallet("Test User Wallet")
    print(f"✅ New Wallet: {new_wallet.address}")
    print(f"🔐 Mnemonic: {new_wallet.mnemonic}")
    
    # Transfer some tokens
    print("\n💸 Transferring 1000 HYBRID from founder to new wallet...")
    success = hybrid_wallet_manager.transfer(
        founder.address, 
        new_wallet.address, 
        1000 * 1_000_000  # 1000 HYBRID
    )
    
    if success:
        print(f"✅ Transfer successful!")
        print(f"👑 Founder balance: {hybrid_wallet_manager.get_balance_hybrid(founder.address):,.0f} HYBRID")
        print(f"📱 New wallet balance: {hybrid_wallet_manager.get_balance_hybrid(new_wallet.address):,.0f} HYBRID")
