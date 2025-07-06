
#!/usr/bin/env python3
"""
x/moe module - AI Mixture-of-Experts integration
Handles on-chain AI model registry and inference calls
"""
import json
import hashlib
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ModelStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    BLACKLISTED = "blacklisted"

@dataclass
class MoEModel:
    """AI model registration in the MoE system"""
    model_id: str
    name: str
    description: str
    ipfs_cid: str  # Content-addressable model storage
    creator: str
    version: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    inference_fee: int  # Cost per inference in uhybrid
    status: ModelStatus = ModelStatus.ACTIVE
    created_at: str = ""
    total_calls: int = 0
    total_fees_earned: int = 0

@dataclass
class MoEInferenceCall:
    """On-chain inference call record"""
    call_id: str
    model_id: str
    caller: str
    input_hash: str  # SHA256 of input data
    output_hash: str  # SHA256 of output data
    fee_paid: int
    inference_time_ms: int
    timestamp: str
    status: str  # "pending", "completed", "failed"

@dataclass
class MoEExpert:
    """AI expert operator in the MoE network"""
    expert_id: str
    operator_address: str
    supported_models: List[str]
    reputation_score: float
    total_inferences: int
    success_rate: float
    avg_response_time: float
    stake_amount: int  # Staked HYBRID for reputation

class MoEModule:
    """
    x/moe module implementation
    Manages AI model registry and inference coordination
    """
    
    def __init__(self):
        self.models: Dict[str, MoEModel] = {}
        self.inference_calls: Dict[str, MoEInferenceCall] = {}
        self.experts: Dict[str, MoEExpert] = {}
        self.total_fees_collected = 0
        self.burn_rate = 0.10  # 10% of fees burned, 90% to experts
    
    def register_model(self, model: MoEModel) -> bool:
        """Register a new AI model in the MoE system"""
        if model.model_id in self.models:
            return False
        
        # Validate IPFS CID format
        if not self._validate_ipfs_cid(model.ipfs_cid):
            return False
        
        model.created_at = str(time.time())
        self.models[model.model_id] = model
        return True
    
    def _validate_ipfs_cid(self, cid: str) -> bool:
        """Validate IPFS content identifier"""
        # Basic validation - starts with Qm and proper length
        return cid.startswith('Qm') and len(cid) == 46
    
    def call_moe(self, caller: str, model_id: str, input_data: str) -> Optional[str]:
        """Initiate MoE inference call"""
        model = self.models.get(model_id)
        if not model or model.status != ModelStatus.ACTIVE:
            return None
        
        # Generate call ID
        call_id = f"moe_{model_id}_{int(time.time())}_{hash(input_data) % 10000}"
        
        # Hash input for privacy
        input_hash = hashlib.sha256(input_data.encode()).hexdigest()
        
        inference_call = MoEInferenceCall(
            call_id=call_id,
            model_id=model_id,
            caller=caller,
            input_hash=input_hash,
            output_hash="",
            fee_paid=model.inference_fee,
            inference_time_ms=0,
            timestamp=str(time.time()),
            status="pending"
        )
        
        self.inference_calls[call_id] = inference_call
        
        # Update model stats
        model.total_calls += 1
        
        # In production, this would emit an event for off-chain workers
        print(f"🧠 MoE inference call {call_id} created for model {model_id}")
        
        return call_id
    
    def submit_moe_result(self, call_id: str, expert_id: str, 
                         output_data: str, inference_time_ms: int) -> bool:
        """Submit inference result from expert"""
        call = self.inference_calls.get(call_id)
        if not call or call.status != "pending":
            return False
        
        expert = self.experts.get(expert_id)
        if not expert:
            return False
        
        # Hash output
        output_hash = hashlib.sha256(output_data.encode()).hexdigest()
        
        # Update call record
        call.output_hash = output_hash
        call.inference_time_ms = inference_time_ms
        call.status = "completed"
        
        # Distribute fees
        self._distribute_inference_fees(call, expert_id)
        
        # Update expert stats
        expert.total_inferences += 1
        expert.avg_response_time = (
            (expert.avg_response_time * (expert.total_inferences - 1) + inference_time_ms) 
            / expert.total_inferences
        )
        
        return True
    
    def _distribute_inference_fees(self, call: MoEInferenceCall, expert_id: str):
        """Distribute inference fees between expert and burn"""
        total_fee = call.fee_paid
        burn_amount = int(total_fee * self.burn_rate)
        expert_reward = total_fee - burn_amount
        
        # Update totals
        self.total_fees_collected += total_fee
        
        # Update model earnings
        model = self.models[call.model_id]
        model.total_fees_earned += expert_reward
        
        print(f"💰 Fee distribution - Expert: {expert_reward}, Burned: {burn_amount}")
    
    def register_expert(self, expert: MoEExpert) -> bool:
        """Register new MoE expert operator"""
        if expert.expert_id in self.experts:
            return False
        
        # Minimum stake requirement (10,000 HYBRID)
        if expert.stake_amount < 10_000_000_000:  # 10k HYBRID in uhybrid
            return False
        
        self.experts[expert.expert_id] = expert
        return True
    
    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """Get detailed model information"""
        model = self.models.get(model_id)
        if not model:
            return None
        
        # Get recent inference calls
        recent_calls = [
            call for call in self.inference_calls.values()
            if call.model_id == model_id
        ][-10:]  # Last 10 calls
        
        return {
            "model": model,
            "recent_calls": len(recent_calls),
            "avg_inference_time": sum(c.inference_time_ms for c in recent_calls if c.status == "completed") / max(len(recent_calls), 1),
            "success_rate": len([c for c in recent_calls if c.status == "completed"]) / max(len(recent_calls), 1)
        }
    
    def list_active_models(self) -> List[MoEModel]:
        """List all active models"""
        return [m for m in self.models.values() if m.status == ModelStatus.ACTIVE]
    
    def get_expert_stats(self, expert_id: str) -> Optional[Dict]:
        """Get expert performance statistics"""
        expert = self.experts.get(expert_id)
        if not expert:
            return None
        
        expert_calls = [
            call for call in self.inference_calls.values()
            # In production, we'd track which expert handled each call
        ]
        
        return {
            "expert": expert,
            "total_earnings": sum(
                self.models[call.model_id].inference_fee * (1 - self.burn_rate)
                for call in expert_calls
                if call.status == "completed"
            )
        }

# Global MoE module instance
moe_module = MoEModule()

# Register some demo models
demo_models = [
    MoEModel(
        model_id="hybrid_llm_v1",
        name="HYBRID Language Model v1",
        description="Multi-chain aware language model for DeFi queries",
        ipfs_cid="QmYjtig7VJQ6XsnUjqqJvj7QaMcCAwtrgNdahSiFofrE7o",
        creator="hybrid1creator...",
        version="1.0.0",
        input_schema={"type": "string", "max_length": 1000},
        output_schema={"type": "string", "max_length": 2000},
        inference_fee=100_000  # 0.1 HYBRID
    ),
    MoEModel(
        model_id="hybrid_price_predictor",
        name="HYBRID Price Prediction Model",
        description="Predicts HYBRID token price based on on-chain metrics",
        ipfs_cid="QmPricePredict123456789AbCdEfGhIjKlMnOpQrSt",
        creator="hybrid1creator...",
        version="2.1.0",
        input_schema={"type": "object", "properties": {"timeframe": "string", "metrics": "array"}},
        output_schema={"type": "object", "properties": {"price": "number", "confidence": "number"}},
        inference_fee=250_000  # 0.25 HYBRID
    )
]

for model in demo_models:
    moe_module.register_model(model)

if __name__ == "__main__":
    # Demo usage
    print("🧠 MoE Module Demo")
    
    # List models
    models = moe_module.list_active_models()
    print(f"Active models: {len(models)}")
    
    # Make inference call
    call_id = moe_module.call_moe(
        caller="hybrid1user...",
        model_id="hybrid_llm_v1",
        input_data="What is the current HYBRID token price?"
    )
    
    if call_id:
        print(f"🚀 Inference call created: {call_id}")
        
        # Simulate expert response
        success = moe_module.submit_moe_result(
            call_id=call_id,
            expert_id="expert_1",
            output_data="Based on current market data, HYBRID is trading at $10.50",
            inference_time_ms=1500
        )
        
        if success:
            print("✅ Inference completed successfully")
