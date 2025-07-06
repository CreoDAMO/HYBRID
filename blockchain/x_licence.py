
#!/usr/bin/env python3
"""
x/licence module - NFT license validation for node operations
Core module for HYBRID blockchain NFT-gated participation
"""
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import requests

class LicenseType(Enum):
    VALIDATOR = "HNL-VAL"
    STORAGE = "HNL-STR"

@dataclass
class NFTLicenseProof:
    """Proof of NFT license ownership for cross-chain validation"""
    license_id: str
    owner_address: str
    license_type: LicenseType
    chain: str  # "base", "polygon", etc.
    contract_address: str
    token_id: str
    block_height: int
    tx_hash: str
    signature: str

@dataclass
class LicenseDelegation:
    """Delegation of license rights to node operator"""
    license_id: str
    owner: str
    delegate: str
    expires_at: Optional[str] = None
    revenue_split: int = 70  # Owner gets 70%, operator 30% (per spec)

class LicenceModule:
    """
    x/licence module implementation
    Validates NFT ownership before allowing node operations
    """
    
    def __init__(self):
        self.license_proofs: Dict[str, NFTLicenseProof] = {}
        self.delegations: Dict[str, LicenseDelegation] = {}
        self.blacklisted_licenses: set = set()
        
        # Contract addresses on different chains
        self.hnl_contracts = {
            "base": "0x...",  # HNL contract on Base
            "polygon": "0x...",  # HNL contract on Polygon
            "hybrid": "hybrid1..."  # Native NFT module
        }
    
    def register_nft_proof(self, proof: NFTLicenseProof) -> bool:
        """Register NFT license proof from external chain"""
        # Validate proof against external chain
        if not self._validate_external_ownership(proof):
            return False
        
        # Check if license is blacklisted
        if proof.license_id in self.blacklisted_licenses:
            return False
        
        self.license_proofs[proof.license_id] = proof
        return True
    
    def _validate_external_ownership(self, proof: NFTLicenseProof) -> bool:
        """Validate NFT ownership on external chain (Base/Polygon)"""
        # In production, this would use web3 RPC calls
        # For now, return True for valid structure
        return all([
            proof.owner_address,
            proof.contract_address,
            proof.token_id,
            proof.tx_hash
        ])
    
    def verify_license(self, operator_address: str, license_type: LicenseType) -> bool:
        """Verify if address can operate node of given type"""
        # Check direct ownership
        for proof in self.license_proofs.values():
            if (proof.owner_address == operator_address and 
                proof.license_type == license_type and
                proof.license_id not in self.blacklisted_licenses):
                return True
        
        # Check delegations
        for delegation in self.delegations.values():
            if (delegation.delegate == operator_address and
                delegation.license_id in self.license_proofs):
                proof = self.license_proofs[delegation.license_id]
                if (proof.license_type == license_type and
                    proof.license_id not in self.blacklisted_licenses):
                    return True
        
        return False
    
    def delegate_license(self, license_id: str, owner: str, delegate: str, 
                        expires_at: Optional[str] = None) -> bool:
        """Delegate license operation rights"""
        # Verify ownership
        proof = self.license_proofs.get(license_id)
        if not proof or proof.owner_address != owner:
            return False
        
        delegation = LicenseDelegation(
            license_id=license_id,
            owner=owner,
            delegate=delegate,
            expires_at=expires_at
        )
        
        self.delegations[f"{license_id}:{delegate}"] = delegation
        return True
    
    def blacklist_license(self, license_id: str, reason: str = "slashing"):
        """Blacklist license (e.g., due to double-signing)"""
        self.blacklisted_licenses.add(license_id)
        print(f"License {license_id} blacklisted: {reason}")
    
    def get_license_info(self, license_id: str) -> Optional[Dict]:
        """Get license information"""
        proof = self.license_proofs.get(license_id)
        if not proof:
            return None
        
        delegations = [
            d for d in self.delegations.values() 
            if d.license_id == license_id
        ]
        
        return {
            "proof": proof,
            "delegations": delegations,
            "blacklisted": license_id in self.blacklisted_licenses
        }

# Global licence module instance
licence_module = LicenceModule()

def verify_node_license(operator: str, node_type: str) -> bool:
    """Helper function to verify node license"""
    license_type = LicenseType.VALIDATOR if node_type == "validator" else LicenseType.STORAGE
    return licence_module.verify_license(operator, license_type)

if __name__ == "__main__":
    # Demo usage
    module = LicenceModule()
    
    # Register a sample license proof
    proof = NFTLicenseProof(
        license_id="HNL-VAL-001",
        owner_address="hybrid1abc123...",
        license_type=LicenseType.VALIDATOR,
        chain="base",
        contract_address="0x1234...",
        token_id="1",
        block_height=12345,
        tx_hash="0xabcd...",
        signature="0x..."
    )
    
    success = module.register_nft_proof(proof)
    print(f"License registered: {success}")
    
    # Verify license
    can_validate = module.verify_license("hybrid1abc123...", LicenseType.VALIDATOR)
    print(f"Can operate validator: {can_validate}")
