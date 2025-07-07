
"""
HYBRID Blockchain Staking System
Token staking, delegation, and reward distribution
"""

import time
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class BondStatus(Enum):
    BONDED = "bonded"
    UNBONDING = "unbonding"
    UNBONDED = "unbonded"

@dataclass
class StakingPool:
    """Global staking pool information"""
    bonded_tokens: int
    not_bonded_tokens: int
    
    @property
    def total_supply(self) -> int:
        return self.bonded_tokens + self.not_bonded_tokens

@dataclass
class UnbondingDelegation:
    """Unbonding delegation entry"""
    delegator: str
    validator: str
    creation_height: int
    completion_time: float
    initial_balance: int
    balance: int

@dataclass
class Redelegation:
    """Redelegation entry"""
    delegator: str
    validator_src: str
    validator_dst: str
    creation_height: int
    completion_time: float
    initial_balance: int
    shares_dst: float

class StakingModule:
    """HYBRID blockchain staking system"""
    
    def __init__(self):
        self.pool = StakingPool(bonded_tokens=0, not_bonded_tokens=100_000_000_000 * 1_000_000)
        self.delegations: Dict[Tuple[str, str], int] = {}  # (delegator, validator) -> amount
        self.unbonding_delegations: Dict[str, List[UnbondingDelegation]] = {}
        self.redelegations: Dict[str, List[Redelegation]] = {}
        self.rewards: Dict[Tuple[str, str], int] = {}  # (delegator, validator) -> rewards
        
        # Staking parameters
        self.unbonding_time = 21 * 24 * 3600  # 21 days
        self.max_validators = 21
        self.max_entries = 7  # Max unbonding/redelegation entries per pair
        self.historical_entries = 10000
        
        # Reward parameters
        self.annual_provisions = 7_000_000_000 * 1_000_000  # 7B HYBRID annually
        self.inflation_rate = 0.07  # 7% initial inflation
        self.inflation_min = 0.02  # 2% minimum
        self.inflation_max = 0.20  # 20% maximum
        self.goal_bonded = 0.67  # 67% target bonding ratio
        
    def delegate(self, delegator: str, validator: str, amount: int) -> bool:
        """Delegate tokens to a validator"""
        if amount <= 0:
            return False
        
        # Check if tokens are available
        if amount > self.pool.not_bonded_tokens:
            return False
        
        # Update pool
        self.pool.not_bonded_tokens -= amount
        self.pool.bonded_tokens += amount
        
        # Update delegation
        key = (delegator, validator)
        self.delegations[key] = self.delegations.get(key, 0) + amount
        
        # Initialize rewards
        if key not in self.rewards:
            self.rewards[key] = 0
        
        return True
    
    def undelegate(self, delegator: str, validator: str, amount: int) -> bool:
        """Start unbonding delegation"""
        key = (delegator, validator)
        current_delegation = self.delegations.get(key, 0)
        
        if amount <= 0 or amount > current_delegation:
            return False
        
        # Check max entries
        unbonding_list = self.unbonding_delegations.get(delegator, [])
        validator_entries = [u for u in unbonding_list if u.validator == validator]
        if len(validator_entries) >= self.max_entries:
            return False
        
        # Update delegation
        self.delegations[key] -= amount
        if self.delegations[key] == 0:
            del self.delegations[key]
        
        # Create unbonding entry
        unbonding = UnbondingDelegation(
            delegator=delegator,
            validator=validator,
            creation_height=0,  # Would be actual block height
            completion_time=time.time() + self.unbonding_time,
            initial_balance=amount,
            balance=amount
        )
        
        if delegator not in self.unbonding_delegations:
            self.unbonding_delegations[delegator] = []
        
        self.unbonding_delegations[delegator].append(unbonding)
        
        return True
    
    def redelegate(self, delegator: str, validator_src: str, validator_dst: str, amount: int) -> bool:
        """Redelegate tokens from one validator to another"""
        src_key = (delegator, validator_src)
        dst_key = (delegator, validator_dst)
        
        current_src_delegation = self.delegations.get(src_key, 0)
        
        if amount <= 0 or amount > current_src_delegation:
            return False
        
        # Check max entries
        redelegation_list = self.redelegations.get(delegator, [])
        pair_entries = [r for r in redelegation_list 
                       if r.validator_src == validator_src and r.validator_dst == validator_dst]
        if len(pair_entries) >= self.max_entries:
            return False
        
        # Update delegations
        self.delegations[src_key] -= amount
        if self.delegations[src_key] == 0:
            del self.delegations[src_key]
        
        self.delegations[dst_key] = self.delegations.get(dst_key, 0) + amount
        
        # Create redelegation entry
        redelegation = Redelegation(
            delegator=delegator,
            validator_src=validator_src,
            validator_dst=validator_dst,
            creation_height=0,  # Would be actual block height
            completion_time=time.time() + self.unbonding_time,
            initial_balance=amount,
            shares_dst=float(amount)  # Simplified: 1:1 token to share ratio
        )
        
        if delegator not in self.redelegations:
            self.redelegations[delegator] = []
        
        self.redelegations[delegator].append(redelegation)
        
        return True
    
    def complete_unbonding(self, delegator: str) -> int:
        """Complete mature unbonding delegations"""
        if delegator not in self.unbonding_delegations:
            return 0
        
        current_time = time.time()
        completed_amount = 0
        remaining = []
        
        for unbonding in self.unbonding_delegations[delegator]:
            if current_time >= unbonding.completion_time:
                # Complete unbonding
                completed_amount += unbonding.balance
                self.pool.bonded_tokens -= unbonding.balance
                self.pool.not_bonded_tokens += unbonding.balance
            else:
                remaining.append(unbonding)
        
        self.unbonding_delegations[delegator] = remaining
        if not remaining:
            del self.unbonding_delegations[delegator]
        
        return completed_amount
    
    def complete_redelegation(self, delegator: str) -> bool:
        """Complete mature redelegations"""
        if delegator not in self.redelegations:
            return False
        
        current_time = time.time()
        remaining = []
        
        for redelegation in self.redelegations[delegator]:
            if current_time < redelegation.completion_time:
                remaining.append(redelegation)
        
        self.redelegations[delegator] = remaining
        if not remaining:
            del self.redelegations[delegator]
        
        return True
    
    def distribute_rewards(self, validator: str, rewards_amount: int):
        """Distribute rewards to a validator's delegators"""
        # Find all delegations to this validator
        validator_delegations = {k: v for k, v in self.delegations.items() if k[1] == validator}
        
        if not validator_delegations:
            return
        
        total_delegation = sum(validator_delegations.values())
        
        # Distribute proportionally
        for (delegator, val), amount in validator_delegations.items():
            delegation_reward = int((amount / total_delegation) * rewards_amount)
            key = (delegator, validator)
            self.rewards[key] = self.rewards.get(key, 0) + delegation_reward
    
    def withdraw_rewards(self, delegator: str, validator: str) -> int:
        """Withdraw accumulated rewards"""
        key = (delegator, validator)
        rewards = self.rewards.get(key, 0)
        
        if rewards > 0:
            self.rewards[key] = 0
            self.pool.not_bonded_tokens += rewards
        
        return rewards
    
    def calculate_inflation(self) -> float:
        """Calculate current inflation rate"""
        bonded_ratio = self.pool.bonded_tokens / self.pool.total_supply if self.pool.total_supply > 0 else 0
        
        if bonded_ratio < self.goal_bonded:
            # Increase inflation to incentivize bonding
            inflation_rate_change = (1 - bonded_ratio / self.goal_bonded) * 0.01
            new_rate = self.inflation_rate + inflation_rate_change
        else:
            # Decrease inflation
            inflation_rate_change = (bonded_ratio / self.goal_bonded - 1) * 0.01
            new_rate = self.inflation_rate - inflation_rate_change
        
        return max(self.inflation_min, min(self.inflation_max, new_rate))
    
    def get_delegation(self, delegator: str, validator: str) -> int:
        """Get delegation amount"""
        return self.delegations.get((delegator, validator), 0)
    
    def get_delegations(self, delegator: str) -> Dict[str, int]:
        """Get all delegations for a delegator"""
        return {validator: amount for (del_addr, validator), amount in self.delegations.items() 
                if del_addr == delegator}
    
    def get_validator_delegations(self, validator: str) -> Dict[str, int]:
        """Get all delegations to a validator"""
        return {delegator: amount for (delegator, val), amount in self.delegations.items() 
                if val == validator}
    
    def get_rewards(self, delegator: str, validator: str) -> int:
        """Get accumulated rewards"""
        return self.rewards.get((delegator, validator), 0)
    
    def get_all_rewards(self, delegator: str) -> Dict[str, int]:
        """Get all rewards for a delegator"""
        return {validator: amount for (del_addr, validator), amount in self.rewards.items() 
                if del_addr == delegator}
    
    def get_unbonding_delegations(self, delegator: str) -> List[UnbondingDelegation]:
        """Get unbonding delegations for a delegator"""
        return self.unbonding_delegations.get(delegator, [])
    
    def get_redelegations(self, delegator: str) -> List[Redelegation]:
        """Get redelegations for a delegator"""
        return self.redelegations.get(delegator, [])
    
    def get_pool(self) -> StakingPool:
        """Get staking pool information"""
        return self.pool
    
    def get_staking_stats(self) -> Dict:
        """Get staking statistics"""
        bonded_ratio = self.pool.bonded_tokens / self.pool.total_supply if self.pool.total_supply > 0 else 0
        total_delegators = len(set(delegator for delegator, _ in self.delegations.keys()))
        total_delegations = len(self.delegations)
        
        return {
            "bonded_tokens": self.pool.bonded_tokens,
            "not_bonded_tokens": self.pool.not_bonded_tokens,
            "total_supply": self.pool.total_supply,
            "bonded_ratio": bonded_ratio,
            "inflation_rate": self.calculate_inflation(),
            "total_delegators": total_delegators,
            "total_delegations": total_delegations,
            "unbonding_time_days": self.unbonding_time / (24 * 3600)
        }

# Global staking module
staking = StakingModule()
