
#!/usr/bin/env python3
"""
P2P networking implementation for HYBRID blockchain
"""
import asyncio
import json
import websockets
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class Peer:
    node_id: str
    address: str
    port: int
    websocket: Optional[websockets.WebSocketServerProtocol] = None
    
    @property
    def endpoint(self) -> str:
        return f"ws://{self.address}:{self.port}"

@dataclass
class Message:
    msg_type: str
    data: Dict
    sender: str
    timestamp: float

class P2PNetwork:
    """P2P networking for HYBRID blockchain nodes"""
    
    def __init__(self, node_id: str, listen_port: int = 26656):
        self.node_id = node_id
        self.listen_port = listen_port
        self.peers: Dict[str, Peer] = {}
        self.connected_peers: Set[str] = set()
        self.message_handlers: Dict[str, callable] = {}
        self.server = None
        
        # Register default handlers
        self.register_handler("ping", self._handle_ping)
        self.register_handler("pong", self._handle_pong)
        self.register_handler("peer_list", self._handle_peer_list)
    
    def register_handler(self, msg_type: str, handler: callable):
        """Register message handler"""
        self.message_handlers[msg_type] = handler
    
    async def start_server(self):
        """Start P2P server"""
        try:
            self.server = await websockets.serve(
                self._handle_connection,
                "0.0.0.0",
                self.listen_port
            )
            logger.info(f"P2P server started on port {self.listen_port}")
        except Exception as e:
            logger.error(f"Failed to start P2P server: {e}")
    
    async def _handle_connection(self, websocket, path):
        """Handle incoming P2P connection"""
        peer_id = None
        try:
            async for raw_message in websocket:
                try:
                    message_data = json.loads(raw_message)
                    message = Message(**message_data)
                    
                    # First message should be handshake
                    if not peer_id and message.msg_type == "handshake":
                        peer_id = message.sender
                        peer_info = message.data.get("peer_info", {})
                        
                        # Store peer connection
                        if peer_id not in self.peers:
                            self.peers[peer_id] = Peer(
                                node_id=peer_id,
                                address=peer_info.get("address", "unknown"),
                                port=peer_info.get("port", 0)
                            )
                        
                        self.peers[peer_id].websocket = websocket
                        self.connected_peers.add(peer_id)
                        
                        # Send handshake response
                        await self._send_handshake_response(websocket)
                        logger.info(f"Peer {peer_id} connected")
                        
                    elif peer_id:
                        # Handle regular messages
                        await self._handle_message(message)
                        
                except json.JSONDecodeError:
                    logger.warning("Received invalid JSON message")
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            if peer_id:
                logger.info(f"Peer {peer_id} disconnected")
                self.connected_peers.discard(peer_id)
                if peer_id in self.peers:
                    self.peers[peer_id].websocket = None
    
    async def _send_handshake_response(self, websocket):
        """Send handshake response"""
        response = Message(
            msg_type="handshake_response",
            data={
                "peer_info": {
                    "node_id": self.node_id,
                    "address": "0.0.0.0",
                    "port": self.listen_port
                },
                "peer_list": [
                    {"node_id": pid, "address": peer.address, "port": peer.port}
                    for pid, peer in self.peers.items()
                    if pid in self.connected_peers
                ]
            },
            sender=self.node_id,
            timestamp=asyncio.get_event_loop().time()
        )
        
        await websocket.send(json.dumps(asdict(response)))
    
    async def connect_to_peer(self, address: str, port: int) -> bool:
        """Connect to a peer"""
        endpoint = f"ws://{address}:{port}"
        try:
            websocket = await websockets.connect(endpoint)
            
            # Send handshake
            handshake = Message(
                msg_type="handshake",
                data={
                    "peer_info": {
                        "node_id": self.node_id,
                        "address": "0.0.0.0",
                        "port": self.listen_port
                    }
                },
                sender=self.node_id,
                timestamp=asyncio.get_event_loop().time()
            )
            
            await websocket.send(json.dumps(asdict(handshake)))
            
            # Handle responses
            asyncio.create_task(self._handle_outbound_connection(websocket, endpoint))
            
            logger.info(f"Connected to peer at {endpoint}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to {endpoint}: {e}")
            return False
    
    async def _handle_outbound_connection(self, websocket, endpoint):
        """Handle outbound connection messages"""
        try:
            async for raw_message in websocket:
                try:
                    message_data = json.loads(raw_message)
                    message = Message(**message_data)
                    await self._handle_message(message)
                except Exception as e:
                    logger.error(f"Error handling outbound message: {e}")
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection to {endpoint} closed")
    
    async def _handle_message(self, message: Message):
        """Handle received P2P message"""
        handler = self.message_handlers.get(message.msg_type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Error in handler for {message.msg_type}: {e}")
        else:
            logger.warning(f"No handler for message type: {message.msg_type}")
    
    async def _handle_ping(self, message: Message):
        """Handle ping message"""
        pong = Message(
            msg_type="pong",
            data={"timestamp": asyncio.get_event_loop().time()},
            sender=self.node_id,
            timestamp=asyncio.get_event_loop().time()
        )
        await self.send_to_peer(message.sender, pong)
    
    async def _handle_pong(self, message: Message):
        """Handle pong message"""
        logger.debug(f"Received pong from {message.sender}")
    
    async def _handle_peer_list(self, message: Message):
        """Handle peer list message"""
        peer_list = message.data.get("peers", [])
        for peer_info in peer_list:
            node_id = peer_info.get("node_id")
            if node_id and node_id != self.node_id and node_id not in self.peers:
                # Try to connect to new peer
                address = peer_info.get("address")
                port = peer_info.get("port")
                if address and port:
                    await self.connect_to_peer(address, port)
    
    async def send_to_peer(self, peer_id: str, message: Message):
        """Send message to specific peer"""
        peer = self.peers.get(peer_id)
        if peer and peer.websocket:
            try:
                await peer.websocket.send(json.dumps(asdict(message)))
            except Exception as e:
                logger.error(f"Failed to send to {peer_id}: {e}")
                # Remove disconnected peer
                self.connected_peers.discard(peer_id)
                peer.websocket = None
    
    async def broadcast(self, message: Message):
        """Broadcast message to all connected peers"""
        for peer_id in list(self.connected_peers):
            await self.send_to_peer(peer_id, message)
    
    async def ping_peers(self):
        """Ping all connected peers"""
        ping = Message(
            msg_type="ping",
            data={"timestamp": asyncio.get_event_loop().time()},
            sender=self.node_id,
            timestamp=asyncio.get_event_loop().time()
        )
        await self.broadcast(ping)
    
    def get_connected_peers(self) -> List[str]:
        """Get list of connected peer IDs"""
        return list(self.connected_peers)
    
    async def stop(self):
        """Stop P2P networking"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        # Close peer connections
        for peer in self.peers.values():
            if peer.websocket:
                await peer.websocket.close()

# Example usage
if __name__ == "__main__":
    async def run_p2p_demo():
        # Create P2P network
        network = P2PNetwork("demo_node", 26656)
        
        # Start server
        await network.start_server()
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(10)
                await network.ping_peers()
        except KeyboardInterrupt:
            await network.stop()
    
    asyncio.run(run_p2p_demo())
