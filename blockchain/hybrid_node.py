"""
HYBRID Blockchain Node Implementation
Core node functionality for the HYBRID network
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

class NodeType(Enum):
    STORAGE = "storage"
    VALIDATOR = "validator"

@dataclass
class NFTLicense:
    """NFT License for node operation"""
    token_id: str
    owner_address: str
    node_type: NodeType
    start_date: str
    end_date: Optional[str]

@dataclass
class Block:
    """HYBRID blockchain block"""
    height: int
    hash: str
    prev_hash: str
    timestamp: float
    transactions: List[Dict]
    validator: str

class HybridBlockchainNode:
    """HYBRID blockchain node implementation"""

    def __init__(self, node_type: NodeType, license: Optional[NFTLicense] = None):
        self.node_type = node_type
        self.license = license
        self.is_running = False
        self.block_height = 1234567
        self.peers: List[str] = []
        self.blockchain: List[Block] = []
        self.validator_set: List[str] = []

    async def start(self):
        """Start the blockchain node"""
        if self.node_type == NodeType.VALIDATOR and not self.license:
            raise Exception("Validator nodes require an NFT license")

        self.is_running = True
        print(f"🚀 HYBRID {self.node_type.value} node started")

        # Start background tasks
        asyncio.create_task(self._block_production_loop())
        asyncio.create_task(self._peer_discovery_loop())

    async def stop(self):
        """Stop the blockchain node"""
        self.is_running = False
        print(f"⏹️ HYBRID {self.node_type.value} node stopped")

    async def _block_production_loop(self):
        """Block production loop for validators"""
        while self.is_running:
            if self.node_type == NodeType.VALIDATOR:
                await self._produce_block()
            await asyncio.sleep(6)  # 6 second block time

    async def _peer_discovery_loop(self):
        """Peer discovery and networking"""
        while self.is_running:
            # Simulate peer discovery
            await asyncio.sleep(30)

    async def _produce_block(self):
        """Produce a new block"""
        if not self.is_running:
            return

        new_block = Block(
            height=self.block_height + 1,
            hash=f"0x{abs(hash(f'block_{self.block_height + 1}_{time.time()}'))%10**16:016x}",
            prev_hash=f"0x{self.block_height:016x}" if self.blockchain else "0x0",
            timestamp=time.time(),
            transactions=[],
            validator=self.license.owner_address if self.license else "hybrid1genesis"
        )

        self.blockchain.append(new_block)
        self.block_height += 1
        print(f"📦 Block {new_block.height} produced by {new_block.validator}")

    def get_status(self) -> Dict[str, Any]:
        """Get node status"""
        return {
            "node_type": self.node_type.value,
            "is_running": self.is_running,
            "block_height": self.block_height,
            "peer_count": len(self.peers),
            "validator_count": len(self.validator_set),
            "has_license": self.license is not None
        }

def create_hybrid_node(node_type: str, license: Optional[NFTLicense] = None) -> HybridBlockchainNode:
    """Create a HYBRID blockchain node"""
    node_type_enum = NodeType.STORAGE if node_type.lower() == "storage" else NodeType.VALIDATOR

    # Create default license for demo
    if not license:
        license = NFTLicense(
            token_id="DEMO-001",
            owner_address="hybrid1demo",
            node_type=node_type_enum,
            start_date="2024-01-01",
            end_date=None
        )

    return HybridBlockchainNode(node_type_enum, license)
```

```python
if __name__ == "__main__":
    async def main():
        # Create and start a storage node
        node = create_hybrid_node("storage")
        await node.start()

    asyncio.run(main())
```