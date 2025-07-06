
#!/usr/bin/env python3
"""
Genesis configuration for HYBRID blockchain
"""
import json
import time
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from blockchain.hybrid_wallet import get_founder_wallet

@dataclass
class GenesisValidator:
    address: str
    pub_key: str
    power: int
    name: str

@dataclass
class GenesisAccount:
    address: str
    balance: int
    sequence: int = 0

@dataclass
class GenesisConfig:
    chain_id: str
    genesis_time: str
    initial_height: int
    validators: List[GenesisValidator]
    accounts: List[GenesisAccount]
    app_state: Dict[str, Any]

class GenesisGenerator:
    """Generate genesis configuration for HYBRID blockchain"""
    
    def __init__(self):
        self.chain_id = "hybrid-1"  # Main chain ID per spec
        self.genesis_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
    def create_genesis(self) -> GenesisConfig:
        """Create genesis configuration"""
        founder_wallet = get_founder_wallet()
        
        # Create founder account with proper allocation from 100B total supply
        founder_initial_allocation = 10_000_000_000 * 1_000_000  # 10B HYBRID (10% of total supply)
        founder_account = GenesisAccount(
            address=founder_wallet.address,
            balance=founder_initial_allocation,
            sequence=0
        )
        
        # Create initial validator (founder)
        founder_validator = GenesisValidator(
            address=founder_wallet.address,
            pub_key=founder_wallet.public_key,
            power=1000000,  # 1M voting power
            name="HYBRID Foundation"
        )
        
        # App state configuration
        app_state = {
            "bank": {
                "params": {
                    "send_enabled": [{"denom": "uhybrid", "enabled": True}],
                    "default_send_enabled": True
                },
                "balances": [
                    {
                        "address": founder_account.address,
                        "coins": [{"denom": "uhybrid", "amount": str(founder_account.balance)}]
                    }
                ],
                "supply": [
                    {"denom": "uhybrid", "amount": str(founder_account.balance)}
                ],
                "denom_metadata": [
                    {
                        "description": "The native token of HYBRID blockchain",
                        "denom_units": [
                            {"denom": "uhybrid", "exponent": 0, "aliases": ["micro-hybrid"]},
                            {"denom": "hybrid", "exponent": 6}
                        ],
                        "base": "uhybrid",
                        "display": "hybrid",
                        "name": "HYBRID",
                        "symbol": "HYBRID"
                    }
                ]
            },
            "staking": {
                "params": {
                    "unbonding_time": "1814400s",  # 21 days
                    "max_validators": 100,
                    "max_entries": 7,
                    "historical_entries": 10000,
                    "bond_denom": "uhybrid",
                    "min_commission_rate": "0.050000000000000000"
                },
                "last_total_power": "0",
                "last_validator_powers": [],
                "validators": [],
                "delegations": [],
                "unbonding_delegations": [],
                "redelegations": [],
                "exported": False
            },
            "gov": {
                "starting_proposal_id": "1",
                "deposits": [],
                "votes": [],
                "proposals": [],
                "deposit_params": {
                    "min_deposit": [{"denom": "uhybrid", "amount": "10000000"}],  # 10 HYBRID
                    "max_deposit_period": "172800s"  # 2 days
                },
                "voting_params": {
                    "voting_period": "172800s"  # 2 days
                },
                "tally_params": {
                    "quorum": "0.334000000000000000",
                    "threshold": "0.500000000000000000",
                    "veto_threshold": "0.334000000000000000"
                }
            },
            "nft": {
                "classes": [
                    {
                        "id": "hybrid-node-license",
                        "name": "HYBRID Node License",
                        "symbol": "HNL",
                        "description": "NFT licenses for operating HYBRID blockchain nodes",
                        "uri": "https://hybrid.local/nft/metadata",
                        "uri_hash": "",
                        "data": json.dumps({
                            "license_types": ["storage", "validator"],
                            "max_supply": 10000,
                            "creator": founder_wallet.address
                        })
                    }
                ],
                "nfts": []
            },
            "bridge": {
                "params": {
                    "enabled": True,
                    "supported_chains": ["base", "polygon", "solana"],
                    "min_bridge_amount": "1000000",  # 1 HYBRID
                    "bridge_fee": "10000"  # 0.01 HYBRID
                },
                "deposits": [],
                "withdrawals": []
            }
        }
        
        genesis_config = GenesisConfig(
            chain_id=self.chain_id,
            genesis_time=self.genesis_time,
            initial_height=1,
            validators=[founder_validator],
            accounts=[founder_account],
            app_state=app_state
        )
        
        return genesis_config
    
    def export_genesis(self, filename: str = "genesis.json") -> str:
        """Export genesis to JSON file"""
        genesis = self.create_genesis()
        genesis_dict = asdict(genesis)
        
        with open(filename, 'w') as f:
            json.dump(genesis_dict, f, indent=2)
        
        return filename
    
    def validate_genesis(self, genesis_config: GenesisConfig) -> List[str]:
        """Validate genesis configuration"""
        errors = []
        
        # Validate chain ID
        if not genesis_config.chain_id:
            errors.append("Chain ID is required")
        
        # Validate validators
        if not genesis_config.validators:
            errors.append("At least one validator is required")
        
        # Validate accounts
        total_supply = sum(account.balance for account in genesis_config.accounts)
        if total_supply <= 0:
            errors.append("Total supply must be greater than 0")
        
        # Validate voting power
        total_power = sum(validator.power for validator in genesis_config.validators)
        if total_power <= 0:
            errors.append("Total voting power must be greater than 0")
        
        return errors

# CLI tool for genesis generation
if __name__ == "__main__":
    import sys
    
    generator = GenesisGenerator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "generate":
        genesis_file = generator.export_genesis()
        print(f"✅ Genesis file created: {genesis_file}")
        
        # Validate
        genesis = generator.create_genesis()
        errors = generator.validate_genesis(genesis)
        
        if errors:
            print("❌ Genesis validation errors:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("✅ Genesis configuration is valid")
    else:
        print("Usage: python genesis.py generate")
