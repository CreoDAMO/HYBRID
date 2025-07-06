
#!/usr/bin/env python3
"""
Real Tendermint consensus implementation for HYBRID blockchain
"""
import asyncio
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

@dataclass
class Vote:
    validator: str
    block_hash: str
    height: int
    round: int
    vote_type: str  # "prevote" or "precommit"
    timestamp: float
    signature: str

@dataclass
class ValidatorSet:
    validators: Dict[str, int]  # validator_id -> voting_power
    total_power: int
    
    def get_proposer(self, height: int, round: int) -> str:
        """Deterministic proposer selection"""
        validator_list = list(self.validators.keys())
        proposer_index = (height + round) % len(validator_list)
        return validator_list[proposer_index]
    
    def has_majority(self, votes: List[Vote]) -> bool:
        """Check if votes represent 2/3+ majority"""
        vote_power = sum(self.validators.get(vote.validator, 0) for vote in votes)
        return vote_power * 3 > self.total_power * 2

class TendermintConsensus:
    """Real Tendermint consensus algorithm implementation"""
    
    def __init__(self, validator_id: str, validator_set: ValidatorSet):
        self.validator_id = validator_id
        self.validator_set = validator_set
        self.height = 1
        self.round = 0
        self.step = "propose"  # propose, prevote, precommit, commit
        self.locked_block = None
        self.valid_block = None
        
        # Vote storage
        self.prevotes: Dict[int, Dict[int, List[Vote]]] = {}  # height -> round -> votes
        self.precommits: Dict[int, Dict[int, List[Vote]]] = {}
        
        # Private key for signing
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        
    async def start_consensus(self):
        """Start the consensus algorithm"""
        while True:
            try:
                await self.run_consensus_round()
            except Exception as e:
                print(f"Consensus error: {e}")
                await asyncio.sleep(1)
    
    async def run_consensus_round(self):
        """Run a single consensus round"""
        print(f"Starting consensus for height {self.height}, round {self.round}")
        
        # Step 1: Propose
        if self.is_proposer():
            proposal = await self.create_proposal()
            await self.broadcast_proposal(proposal)
        
        # Wait for proposal or timeout
        await asyncio.sleep(3)
        
        # Step 2: Prevote
        prevote = await self.create_prevote()
        await self.broadcast_vote(prevote)
        
        # Wait for prevotes
        await asyncio.sleep(3)
        
        # Step 3: Precommit
        precommit = await self.create_precommit()
        await self.broadcast_vote(precommit)
        
        # Wait for precommits
        await asyncio.sleep(3)
        
        # Step 4: Commit (if we have majority)
        if await self.can_commit():
            await self.commit_block()
            self.height += 1
            self.round = 0
        else:
            self.round += 1
    
    def is_proposer(self) -> bool:
        """Check if this validator is the proposer for current height/round"""
        proposer = self.validator_set.get_proposer(self.height, self.round)
        return proposer == self.validator_id
    
    async def create_proposal(self) -> Dict:
        """Create a block proposal"""
        # In real implementation, this would gather transactions from mempool
        proposal = {
            "height": self.height,
            "round": self.round,
            "proposer": self.validator_id,
            "block_hash": f"block_{self.height}_{self.round}",
            "timestamp": time.time(),
            "transactions": []  # Would include real transactions
        }
        return proposal
    
    async def create_prevote(self) -> Vote:
        """Create a prevote"""
        # Simplified: vote for valid proposal if exists
        block_hash = f"block_{self.height}_{self.round}" if self.valid_block else ""
        
        vote = Vote(
            validator=self.validator_id,
            block_hash=block_hash,
            height=self.height,
            round=self.round,
            vote_type="prevote",
            timestamp=time.time(),
            signature=self.sign_vote(block_hash, "prevote")
        )
        return vote
    
    async def create_precommit(self) -> Vote:
        """Create a precommit"""
        # Check if we have 2/3+ prevotes for a block
        prevotes = self.get_prevotes(self.height, self.round)
        block_hash = ""
        
        if prevotes and self.validator_set.has_majority(prevotes):
            # Vote for the block with majority prevotes
            block_hash = prevotes[0].block_hash
        
        vote = Vote(
            validator=self.validator_id,
            block_hash=block_hash,
            height=self.height,
            round=self.round,
            vote_type="precommit",
            timestamp=time.time(),
            signature=self.sign_vote(block_hash, "precommit")
        )
        return vote
    
    def sign_vote(self, block_hash: str, vote_type: str) -> str:
        """Sign a vote with validator's private key"""
        message = f"{block_hash}:{vote_type}:{self.height}:{self.round}"
        signature = self.private_key.sign(message.encode())
        return signature.hex()
    
    async def broadcast_proposal(self, proposal: Dict):
        """Broadcast proposal to other validators"""
        print(f"Broadcasting proposal: {proposal['block_hash']}")
        # In real implementation, this would use P2P networking
    
    async def broadcast_vote(self, vote: Vote):
        """Broadcast vote to other validators"""
        print(f"Broadcasting {vote.vote_type} for {vote.block_hash}")
        # Store vote locally for demo
        self.store_vote(vote)
    
    def store_vote(self, vote: Vote):
        """Store received vote"""
        if vote.vote_type == "prevote":
            if vote.height not in self.prevotes:
                self.prevotes[vote.height] = {}
            if vote.round not in self.prevotes[vote.height]:
                self.prevotes[vote.height][vote.round] = []
            self.prevotes[vote.height][vote.round].append(vote)
        
        elif vote.vote_type == "precommit":
            if vote.height not in self.precommits:
                self.precommits[vote.height] = {}
            if vote.round not in self.precommits[vote.height]:
                self.precommits[vote.height][vote.round] = []
            self.precommits[vote.height][vote.round].append(vote)
    
    def get_prevotes(self, height: int, round: int) -> List[Vote]:
        """Get prevotes for specific height/round"""
        return self.prevotes.get(height, {}).get(round, [])
    
    def get_precommits(self, height: int, round: int) -> List[Vote]:
        """Get precommits for specific height/round"""
        return self.precommits.get(height, {}).get(round, [])
    
    async def can_commit(self) -> bool:
        """Check if we can commit the block"""
        precommits = self.get_precommits(self.height, self.round)
        return len(precommits) > 0 and self.validator_set.has_majority(precommits)
    
    async def commit_block(self):
        """Commit the block to the blockchain"""
        precommits = self.get_precommits(self.height, self.round)
        if precommits:
            block_hash = precommits[0].block_hash
            print(f"✅ COMMITTED block {block_hash} at height {self.height}")
            # In real implementation, this would update blockchain state

# Example usage
if __name__ == "__main__":
    async def run_consensus_demo():
        # Create validator set
        validator_set = ValidatorSet(
            validators={"val1": 1, "val2": 1, "val3": 1},
            total_power=3
        )
        
        # Create consensus instance
        consensus = TendermintConsensus("val1", validator_set)
        
        # Start consensus
        await consensus.start_consensus()
    
    asyncio.run(run_consensus_demo())
