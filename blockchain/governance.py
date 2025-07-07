
"""
HYBRID Blockchain Governance System
On-chain governance for protocol upgrades and parameter changes
"""

import time
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class ProposalType(Enum):
    TEXT = "text"
    PARAMETER_CHANGE = "parameter_change"
    SOFTWARE_UPGRADE = "software_upgrade"
    COMMUNITY_POOL_SPEND = "community_pool_spend"

class ProposalStatus(Enum):
    DEPOSIT_PERIOD = "deposit_period"
    VOTING_PERIOD = "voting_period"
    PASSED = "passed"
    REJECTED = "rejected"
    FAILED = "failed"

class VoteOption(Enum):
    YES = "yes"
    NO = "no"
    NO_WITH_VETO = "no_with_veto"
    ABSTAIN = "abstain"

@dataclass
class Proposal:
    """Governance proposal"""
    id: int
    title: str
    description: str
    proposer: str
    proposal_type: ProposalType
    status: ProposalStatus
    submit_time: float
    deposit_end_time: float
    voting_start_time: float
    voting_end_time: float
    total_deposit: int
    final_tally: Dict[str, int]
    content: Dict
    
@dataclass
class Vote:
    """Vote on a proposal"""
    proposal_id: int
    voter: str
    option: VoteOption
    weight: int
    timestamp: float

@dataclass
class Deposit:
    """Deposit on a proposal"""
    proposal_id: int
    depositor: str
    amount: int
    timestamp: float

class GovernanceModule:
    """HYBRID blockchain governance system"""
    
    def __init__(self):
        self.proposals: Dict[int, Proposal] = {}
        self.votes: Dict[int, List[Vote]] = {}
        self.deposits: Dict[int, List[Deposit]] = {}
        self.next_proposal_id = 1
        
        # Governance parameters
        self.min_deposit = 1000 * 1_000_000  # 1000 HYBRID
        self.max_deposit_period = 7 * 24 * 3600  # 7 days
        self.voting_period = 7 * 24 * 3600  # 7 days
        self.quorum = 0.33  # 33%
        self.threshold = 0.50  # 50%
        self.veto_threshold = 0.33  # 33%
        
    def submit_proposal(
        self,
        title: str,
        description: str,
        proposer: str,
        proposal_type: ProposalType,
        content: Dict,
        initial_deposit: int = 0
    ) -> int:
        """Submit a new governance proposal"""
        
        proposal_id = self.next_proposal_id
        self.next_proposal_id += 1
        
        current_time = time.time()
        
        proposal = Proposal(
            id=proposal_id,
            title=title,
            description=description,
            proposer=proposer,
            proposal_type=proposal_type,
            status=ProposalStatus.DEPOSIT_PERIOD,
            submit_time=current_time,
            deposit_end_time=current_time + self.max_deposit_period,
            voting_start_time=0,
            voting_end_time=0,
            total_deposit=initial_deposit,
            final_tally={},
            content=content
        )
        
        self.proposals[proposal_id] = proposal
        self.votes[proposal_id] = []
        self.deposits[proposal_id] = []
        
        # Add initial deposit if provided
        if initial_deposit > 0:
            self.add_deposit(proposal_id, proposer, initial_deposit)
        
        return proposal_id
    
    def add_deposit(self, proposal_id: int, depositor: str, amount: int) -> bool:
        """Add deposit to a proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal or proposal.status != ProposalStatus.DEPOSIT_PERIOD:
            return False
        
        # Check if deposit period has ended
        if time.time() > proposal.deposit_end_time:
            self._end_deposit_period(proposal_id)
            return False
        
        deposit = Deposit(
            proposal_id=proposal_id,
            depositor=depositor,
            amount=amount,
            timestamp=time.time()
        )
        
        self.deposits[proposal_id].append(deposit)
        proposal.total_deposit += amount
        
        # Check if minimum deposit reached
        if proposal.total_deposit >= self.min_deposit:
            self._start_voting_period(proposal_id)
        
        return True
    
    def _start_voting_period(self, proposal_id: int):
        """Start voting period for a proposal"""
        proposal = self.proposals[proposal_id]
        current_time = time.time()
        
        proposal.status = ProposalStatus.VOTING_PERIOD
        proposal.voting_start_time = current_time
        proposal.voting_end_time = current_time + self.voting_period
    
    def _end_deposit_period(self, proposal_id: int):
        """End deposit period for a proposal"""
        proposal = self.proposals[proposal_id]
        
        if proposal.total_deposit < self.min_deposit:
            proposal.status = ProposalStatus.FAILED
        else:
            self._start_voting_period(proposal_id)
    
    def vote(self, proposal_id: int, voter: str, option: VoteOption, weight: int) -> bool:
        """Vote on a proposal"""
        proposal = self.proposals.get(proposal_id)
        if not proposal or proposal.status != ProposalStatus.VOTING_PERIOD:
            return False
        
        # Check if voting period has ended
        if time.time() > proposal.voting_end_time:
            self._tally_votes(proposal_id)
            return False
        
        # Check if voter has already voted
        existing_votes = [v for v in self.votes[proposal_id] if v.voter == voter]
        if existing_votes:
            # Update existing vote
            existing_votes[0].option = option
            existing_votes[0].weight = weight
            existing_votes[0].timestamp = time.time()
        else:
            # Add new vote
            vote = Vote(
                proposal_id=proposal_id,
                voter=voter,
                option=option,
                weight=weight,
                timestamp=time.time()
            )
            self.votes[proposal_id].append(vote)
        
        return True
    
    def _tally_votes(self, proposal_id: int):
        """Tally votes and determine proposal outcome"""
        proposal = self.proposals[proposal_id]
        votes = self.votes[proposal_id]
        
        # Calculate vote totals
        tally = {
            VoteOption.YES.value: 0,
            VoteOption.NO.value: 0,
            VoteOption.NO_WITH_VETO.value: 0,
            VoteOption.ABSTAIN.value: 0
        }
        
        total_voting_power = sum(vote.weight for vote in votes)
        
        for vote in votes:
            tally[vote.option.value] += vote.weight
        
        proposal.final_tally = tally
        
        # Determine outcome
        if total_voting_power == 0:
            proposal.status = ProposalStatus.FAILED
            return
        
        # Check quorum
        total_non_abstain = total_voting_power - tally[VoteOption.ABSTAIN.value]
        if total_non_abstain < self.quorum * total_voting_power:
            proposal.status = ProposalStatus.FAILED
            return
        
        # Check veto
        veto_ratio = tally[VoteOption.NO_WITH_VETO.value] / total_non_abstain
        if veto_ratio > self.veto_threshold:
            proposal.status = ProposalStatus.REJECTED
            return
        
        # Check threshold
        yes_ratio = tally[VoteOption.YES.value] / total_non_abstain
        if yes_ratio > self.threshold:
            proposal.status = ProposalStatus.PASSED
        else:
            proposal.status = ProposalStatus.REJECTED
    
    def get_proposal(self, proposal_id: int) -> Optional[Proposal]:
        """Get proposal by ID"""
        return self.proposals.get(proposal_id)
    
    def get_proposals(self, status: Optional[ProposalStatus] = None) -> List[Proposal]:
        """Get all proposals, optionally filtered by status"""
        proposals = list(self.proposals.values())
        
        if status:
            proposals = [p for p in proposals if p.status == status]
        
        return sorted(proposals, key=lambda x: x.submit_time, reverse=True)
    
    def get_votes(self, proposal_id: int) -> List[Vote]:
        """Get votes for a proposal"""
        return self.votes.get(proposal_id, [])
    
    def get_deposits(self, proposal_id: int) -> List[Deposit]:
        """Get deposits for a proposal"""
        return self.deposits.get(proposal_id, [])
    
    def update_proposals(self):
        """Update proposal statuses based on time"""
        current_time = time.time()
        
        for proposal in self.proposals.values():
            if proposal.status == ProposalStatus.DEPOSIT_PERIOD:
                if current_time > proposal.deposit_end_time:
                    self._end_deposit_period(proposal.id)
            elif proposal.status == ProposalStatus.VOTING_PERIOD:
                if current_time > proposal.voting_end_time:
                    self._tally_votes(proposal.id)
    
    def get_governance_stats(self) -> Dict:
        """Get governance statistics"""
        total_proposals = len(self.proposals)
        active_proposals = len([p for p in self.proposals.values() 
                              if p.status in [ProposalStatus.DEPOSIT_PERIOD, ProposalStatus.VOTING_PERIOD]])
        passed_proposals = len([p for p in self.proposals.values() if p.status == ProposalStatus.PASSED])
        
        return {
            "total_proposals": total_proposals,
            "active_proposals": active_proposals,
            "passed_proposals": passed_proposals,
            "min_deposit": self.min_deposit,
            "voting_period_days": self.voting_period / (24 * 3600),
            "quorum": self.quorum,
            "threshold": self.threshold
        }

# Global governance module
governance = GovernanceModule()
