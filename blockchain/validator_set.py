
"""
HYBRID Blockchain Validator Set Management
Manages validator registration, selection, and consensus
"""

import time
import hashlib
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class ValidatorStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    JAILED = "jailed"
    UNBONDING = "unbonding"

@dataclass
class Validator:
    """Validator information"""
    address: str
    pub_key: str
    moniker: str
    website: str
    details: str
    commission_rate: float
    max_commission_rate: float
    max_commission_change_rate: float
    min_self_delegation: int
    self_delegation: int
    total_delegation: int
    status: ValidatorStatus
    jailed_until: Optional[float]
    missed_blocks: int
    uptime: float
    nft_license: str
    
    def is_bonded(self) -> bool:
        """Check if validator is bonded"""
        return self.status == ValidatorStatus.ACTIVE
    
    def can_validate(self) -> bool:
        """Check if validator can participate in consensus"""
        if self.status != ValidatorStatus.ACTIVE:
            return False
        
        if self.jailed_until and time.time() < self.jailed_until:
            return False
        
        return True

@dataclass
class Delegation:
    """Delegation information"""
    delegator: str
    validator: str
    amount: int
    shares: float
    creation_time: float

class ValidatorSet:
    """Manages the active validator set"""
    
    def __init__(self, max_validators: int = 21):
        self.validators: Dict[str, Validator] = {}
        self.delegations: Dict[str, List[Delegation]] = {}
        self.max_validators = max_validators
        self.active_set: List[str] = []
        self.proposer_index = 0
        self.round_robin_enabled = True
        
        # Initialize founder validators
        self._initialize_founder_validators()
    
    def _initialize_founder_validators(self):
        """Initialize founder validators for network bootstrap"""
        founder_validators = [
            {
                "address": "hybridvaloper1founder1",
                "moniker": "Genesis Validator 1",
                "pub_key": "hybridpub1founder1",
                "commission": 0.05
            },
            {
                "address": "hybridvaloper1founder2", 
                "moniker": "Genesis Validator 2",
                "pub_key": "hybridpub1founder2",
                "commission": 0.05
            },
            {
                "address": "hybridvaloper1founder3",
                "moniker": "Genesis Validator 3", 
                "pub_key": "hybridpub1founder3",
                "commission": 0.05
            }
        ]
        
        for i, val_info in enumerate(founder_validators):
            validator = Validator(
                address=val_info["address"],
                pub_key=val_info["pub_key"],
                moniker=val_info["moniker"],
                website="https://hybrid.network",
                details="Genesis validator for HYBRID blockchain",
                commission_rate=val_info["commission"],
                max_commission_rate=0.20,
                max_commission_change_rate=0.01,
                min_self_delegation=1_000_000,  # 1 HYBRID
                self_delegation=10_000_000,     # 10 HYBRID
                total_delegation=50_000_000,    # 50 HYBRID
                status=ValidatorStatus.ACTIVE,
                jailed_until=None,
                missed_blocks=0,
                uptime=100.0,
                nft_license=f"VAL-GENESIS-{i+1:03d}"
            )
            
            self.validators[validator.address] = validator
            self.active_set.append(validator.address)
    
    def register_validator(
        self,
        address: str,
        pub_key: str,
        moniker: str,
        commission_rate: float,
        min_self_delegation: int,
        nft_license: str,
        website: str = "",
        details: str = ""
    ) -> bool:
        """Register a new validator"""
        
        # Check if already registered
        if address in self.validators:
            return False
        
        # Validate commission rate
        if commission_rate < 0 or commission_rate > 1:
            return False
        
        # Create validator
        validator = Validator(
            address=address,
            pub_key=pub_key,
            moniker=moniker,
            website=website,
            details=details,
            commission_rate=commission_rate,
            max_commission_rate=min(1.0, commission_rate * 2),
            max_commission_change_rate=0.01,
            min_self_delegation=min_self_delegation,
            self_delegation=0,
            total_delegation=0,
            status=ValidatorStatus.INACTIVE,
            jailed_until=None,
            missed_blocks=0,
            uptime=100.0,
            nft_license=nft_license
        )
        
        self.validators[address] = validator
        return True
    
    def delegate(self, delegator: str, validator_addr: str, amount: int) -> bool:
        """Delegate tokens to validator"""
        validator = self.validators.get(validator_addr)
        if not validator:
            return False
        
        # Create delegation
        delegation = Delegation(
            delegator=delegator,
            validator=validator_addr,
            amount=amount,
            shares=float(amount),  # Simplified: 1:1 token to share ratio
            creation_time=time.time()
        )
        
        # Add to delegations
        if validator_addr not in self.delegations:
            self.delegations[validator_addr] = []
        
        self.delegations[validator_addr].append(delegation)
        
        # Update validator totals
        validator.total_delegation += amount
        if delegator == validator_addr:
            validator.self_delegation += amount
        
        # Activate validator if it meets requirements
        if (validator.status == ValidatorStatus.INACTIVE and 
            validator.self_delegation >= validator.min_self_delegation):
            validator.status = ValidatorStatus.ACTIVE
            self._update_active_set()
        
        return True
    
    def undelegate(self, delegator: str, validator_addr: str, amount: int) -> bool:
        """Undelegate tokens from validator"""
        validator = self.validators.get(validator_addr)
        if not validator:
            return False
        
        delegations = self.delegations.get(validator_addr, [])
        remaining_amount = amount
        
        # Remove delegations
        for delegation in delegations[:]:
            if delegation.delegator == delegator and remaining_amount > 0:
                if delegation.amount <= remaining_amount:
                    # Remove entire delegation
                    remaining_amount -= delegation.amount
                    validator.total_delegation -= delegation.amount
                    if delegator == validator_addr:
                        validator.self_delegation -= delegation.amount
                    delegations.remove(delegation)
                else:
                    # Partial removal
                    delegation.amount -= remaining_amount
                    validator.total_delegation -= remaining_amount
                    if delegator == validator_addr:
                        validator.self_delegation -= remaining_amount
                    remaining_amount = 0
        
        # Check if validator should be deactivated
        if validator.self_delegation < validator.min_self_delegation:
            validator.status = ValidatorStatus.INACTIVE
            self._update_active_set()
        
        return remaining_amount == 0
    
    def jail_validator(self, validator_addr: str, jail_time: float = 600):
        """Jail a validator for misbehavior"""
        validator = self.validators.get(validator_addr)
        if validator:
            validator.status = ValidatorStatus.JAILED
            validator.jailed_until = time.time() + jail_time
            self._update_active_set()
    
    def unjail_validator(self, validator_addr: str) -> bool:
        """Unjail a validator"""
        validator = self.validators.get(validator_addr)
        if not validator or validator.status != ValidatorStatus.JAILED:
            return False
        
        # Check if jail time has passed
        if validator.jailed_until and time.time() < validator.jailed_until:
            return False
        
        validator.status = ValidatorStatus.ACTIVE
        validator.jailed_until = None
        validator.missed_blocks = 0
        self._update_active_set()
        return True
    
    def _update_active_set(self):
        """Update the active validator set"""
        # Get all eligible validators
        eligible = []
        for addr, validator in self.validators.items():
            if validator.can_validate():
                eligible.append((addr, validator.total_delegation))
        
        # Sort by total delegation (descending)
        eligible.sort(key=lambda x: x[1], reverse=True)
        
        # Take top validators
        self.active_set = [addr for addr, _ in eligible[:self.max_validators]]
    
    def get_next_proposer(self) -> Optional[str]:
        """Get next block proposer using round-robin"""
        if not self.active_set:
            return None
        
        if self.round_robin_enabled:
            proposer = self.active_set[self.proposer_index]
            self.proposer_index = (self.proposer_index + 1) % len(self.active_set)
            return proposer
        else:
            # Weighted selection based on stake
            return self._weighted_proposer_selection()
    
    def _weighted_proposer_selection(self) -> Optional[str]:
        """Select proposer based on weighted stake"""
        if not self.active_set:
            return None
        
        # Calculate total stake
        total_stake = sum(self.validators[addr].total_delegation for addr in self.active_set)
        if total_stake == 0:
            return self.active_set[0]
        
        # Generate random selection based on stake weight
        import random
        rand_val = random.random() * total_stake
        
        cumulative = 0
        for addr in self.active_set:
            cumulative += self.validators[addr].total_delegation
            if rand_val <= cumulative:
                return addr
        
        return self.active_set[-1]
    
    def record_block_signature(self, validator_addr: str, signed: bool):
        """Record whether validator signed a block"""
        validator = self.validators.get(validator_addr)
        if not validator:
            return
        
        if not signed:
            validator.missed_blocks += 1
        
        # Calculate uptime (simple rolling average)
        total_blocks = validator.missed_blocks + 1000  # Assume 1000 signed blocks
        validator.uptime = ((total_blocks - validator.missed_blocks) / total_blocks) * 100
        
        # Jail validator if too many missed blocks
        if validator.missed_blocks > 50:  # Configurable threshold
            self.jail_validator(validator_addr, 3600)  # 1 hour jail
    
    def get_validator_set(self) -> List[Validator]:
        """Get current active validator set"""
        return [self.validators[addr] for addr in self.active_set]
    
    def get_validator(self, address: str) -> Optional[Validator]:
        """Get validator by address"""
        return self.validators.get(address)
    
    def get_all_validators(self) -> List[Validator]:
        """Get all registered validators"""
        return list(self.validators.values())
    
    def get_delegations(self, validator_addr: str) -> List[Delegation]:
        """Get delegations for a validator"""
        return self.delegations.get(validator_addr, [])
    
    def get_stats(self) -> Dict:
        """Get validator set statistics"""
        active_count = len(self.active_set)
        total_count = len(self.validators)
        total_stake = sum(v.total_delegation for v in self.validators.values())
        active_stake = sum(self.validators[addr].total_delegation for addr in self.active_set)
        
        return {
            "total_validators": total_count,
            "active_validators": active_count,
            "max_validators": self.max_validators,
            "total_stake": total_stake,
            "active_stake": active_stake,
            "bonded_ratio": active_stake / total_stake if total_stake > 0 else 0
        }

# Global validator set
validator_set = ValidatorSet()
