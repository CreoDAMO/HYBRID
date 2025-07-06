
#!/usr/bin/env python3
"""
x/naas module - Node-as-a-Service delegation and reward splitting
Implements the NaaS provider system per technical specification
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import time

class NaaSStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    TERMINATED = "terminated"

@dataclass
class NaaSProvider:
    """Node-as-a-Service provider"""
    provider_id: str
    name: str
    address: str
    commission_rate: float  # 0.30 = 30%
    max_delegations: int
    uptime_guarantee: float  # 0.99 = 99%
    managed_nodes: List[str]
    total_delegated_power: int
    status: NaaSStatus = NaaSStatus.ACTIVE

@dataclass
class NaaSDelegation:
    """Delegation to NaaS provider"""
    delegation_id: str
    delegator: str  # License owner
    provider: str   # NaaS provider address
    license_id: str
    node_type: str  # "validator" or "storage"
    commission_rate: float
    delegated_at: str
    status: NaaSStatus = NaaSStatus.ACTIVE

@dataclass
class RewardSplit:
    """Reward distribution for NaaS delegation"""
    delegation_id: str
    total_rewards: int
    owner_share: int    # 70% default
    operator_share: int # 30% default
    timestamp: str

class NaaSModule:
    """
    x/naas module implementation
    Manages Node-as-a-Service providers and delegations
    """
    
    def __init__(self):
        self.providers: Dict[str, NaaSProvider] = {}
        self.delegations: Dict[str, NaaSDelegation] = {}
        self.reward_history: List[RewardSplit] = []
        self.default_commission = 0.30  # 30% to operator, 70% to owner
    
    def register_naas_provider(self, provider: NaaSProvider) -> bool:
        """Register a new NaaS provider"""
        if provider.provider_id in self.providers:
            return False
        
        # Validate commission rate (max 50% per spec)
        if provider.commission_rate > 0.50:
            return False
        
        self.providers[provider.provider_id] = provider
        return True
    
    def delegate_to_naas(self, delegator: str, provider_id: str, 
                        license_id: str, node_type: str) -> Optional[str]:
        """Delegate license to NaaS provider"""
        provider = self.providers.get(provider_id)
        if not provider or provider.status != NaaSStatus.ACTIVE:
            return None
        
        # Check if provider can accept more delegations
        if len(provider.managed_nodes) >= provider.max_delegations:
            return None
        
        delegation_id = f"naas_{delegator}_{provider_id}_{int(time.time())}"
        
        delegation = NaaSDelegation(
            delegation_id=delegation_id,
            delegator=delegator,
            provider=provider_id,
            license_id=license_id,
            node_type=node_type,
            commission_rate=provider.commission_rate,
            delegated_at=str(time.time())
        )
        
        self.delegations[delegation_id] = delegation
        provider.managed_nodes.append(delegation_id)
        
        return delegation_id
    
    def undelegate_from_naas(self, delegation_id: str, delegator: str) -> bool:
        """Remove delegation from NaaS provider"""
        delegation = self.delegations.get(delegation_id)
        if not delegation or delegation.delegator != delegator:
            return False
        
        # Mark as terminated
        delegation.status = NaaSStatus.TERMINATED
        
        # Remove from provider's managed nodes
        provider = self.providers.get(delegation.provider)
        if provider and delegation_id in provider.managed_nodes:
            provider.managed_nodes.remove(delegation_id)
        
        return True
    
    def distribute_rewards(self, delegation_id: str, total_rewards: int) -> RewardSplit:
        """Distribute rewards according to NaaS agreement"""
        delegation = self.delegations.get(delegation_id)
        if not delegation or delegation.status != NaaSStatus.ACTIVE:
            return None
        
        # Calculate split
        operator_share = int(total_rewards * delegation.commission_rate)
        owner_share = total_rewards - operator_share
        
        reward_split = RewardSplit(
            delegation_id=delegation_id,
            total_rewards=total_rewards,
            owner_share=owner_share,
            operator_share=operator_share,
            timestamp=str(time.time())
        )
        
        self.reward_history.append(reward_split)
        return reward_split
    
    def get_provider_stats(self, provider_id: str) -> Optional[Dict]:
        """Get NaaS provider statistics"""
        provider = self.providers.get(provider_id)
        if not provider:
            return None
        
        active_delegations = [
            d for d in self.delegations.values() 
            if d.provider == provider_id and d.status == NaaSStatus.ACTIVE
        ]
        
        total_rewards = sum(
            r.total_rewards for r in self.reward_history
            if any(d.delegation_id == r.delegation_id for d in active_delegations)
        )
        
        return {
            "provider": provider,
            "active_delegations": len(active_delegations),
            "total_rewards_processed": total_rewards,
            "avg_commission": provider.commission_rate,
            "uptime": provider.uptime_guarantee
        }
    
    def get_delegator_rewards(self, delegator: str) -> List[RewardSplit]:
        """Get reward history for delegator"""
        delegator_delegations = [
            d.delegation_id for d in self.delegations.values()
            if d.delegator == delegator
        ]
        
        return [
            r for r in self.reward_history
            if r.delegation_id in delegator_delegations
        ]
    
    def list_providers(self) -> List[NaaSProvider]:
        """List all active NaaS providers"""
        return [p for p in self.providers.values() if p.status == NaaSStatus.ACTIVE]

# Global NaaS module instance
naas_module = NaaSModule()

# Initialize some demo NaaS providers
demo_providers = [
    NaaSProvider(
        provider_id="naas_provider_1",
        name="HYBRID Pro Services",
        address="hybrid1naas1...",
        commission_rate=0.25,  # 25%
        max_delegations=100,
        uptime_guarantee=0.999,
        managed_nodes=[]
    ),
    NaaSProvider(
        provider_id="naas_provider_2", 
        name="Cosmos Node Services",
        address="hybrid1naas2...",
        commission_rate=0.30,  # 30%
        max_delegations=50,
        uptime_guarantee=0.995,
        managed_nodes=[]
    )
]

for provider in demo_providers:
    naas_module.register_naas_provider(provider)

if __name__ == "__main__":
    # Demo usage
    print("🔧 NaaS Module Demo")
    
    # List providers
    providers = naas_module.list_providers()
    print(f"Available providers: {len(providers)}")
    
    # Create delegation
    delegation_id = naas_module.delegate_to_naas(
        delegator="hybrid1user123...",
        provider_id="naas_provider_1",
        license_id="HNL-VAL-001",
        node_type="validator"
    )
    
    if delegation_id:
        print(f"✅ Delegation created: {delegation_id}")
        
        # Simulate reward distribution
        reward_split = naas_module.distribute_rewards(delegation_id, 1000000)  # 1 HYBRID
        print(f"💰 Rewards split - Owner: {reward_split.owner_share}, Operator: {reward_split.operator_share}")
