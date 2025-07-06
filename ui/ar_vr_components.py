
"""
AR/VR UI Components for HYBRID Virtual Worlds
Advanced 3D visualization and immersive experiences
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import json
from typing import Dict, List, Any

def create_ar_camera_interface():
    """Create AR camera interface"""
    st.markdown("""
    <div style="border: 2px solid #4CAF50; border-radius: 15px; padding: 20px; background: linear-gradient(135deg, #E8F5E8 0%, #F0FFF0 100%);">
        <h3>📱 AR Camera View</h3>
        <div style="text-align: center; padding: 40px; background: #000; border-radius: 10px; color: white;">
            <h4>🎥 Camera Feed Active</h4>
            <p>Point your device at a surface to place blockchain visualizations</p>
            <div style="display: inline-block; width: 60px; height: 60px; border: 3px solid #4CAF50; border-radius: 50%; border-top: 3px solid transparent; animation: spin 1s linear infinite;"></div>
        </div>
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    </div>
    """, unsafe_allow_html=True)

def create_vr_world_preview(world_data: Dict[str, Any]):
    """Create VR world preview"""
    
    # 3D scene preview
    fig = go.Figure()
    
    # Add terrain/ground
    x_terrain = np.linspace(-100, 100, 20)
    y_terrain = np.linspace(-100, 100, 20)
    X, Y = np.meshgrid(x_terrain, y_terrain)
    Z = np.sin(X/10) * np.cos(Y/10) * 2  # Wavy terrain
    
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Earth',
        showscale=False,
        opacity=0.7,
        name="Terrain"
    ))
    
    # Add buildings/structures
    if '3d_assets' in world_data:
        for asset in world_data['3d_assets'][:10]:  # Limit to 10 for performance
            pos = asset['position']
            fig.add_trace(go.Scatter3d(
                x=[pos['x']],
                y=[pos['z']],
                z=[pos['y'] + 5],  # Elevated
                mode='markers',
                marker=dict(
                    size=10,
                    color='red' if asset['type'] == 'building' else 'blue',
                    symbol='diamond' if asset['type'] == 'building' else 'circle'
                ),
                name=asset['type'].title(),
                text=f"{asset['type']}<br>Interactive: {asset.get('interactive', False)}"
            ))
    
    # Add blockchain data towers
    if 'blockchain_data_points' in world_data:
        for data_point in world_data['blockchain_data_points'][:5]:
            pos = data_point['position']
            height = data_point['height']
            
            # Create tower as a line
            fig.add_trace(go.Scatter3d(
                x=[pos['x'], pos['x']],
                y=[pos['z'], pos['z']],
                z=[0, height],
                mode='lines+markers',
                line=dict(color='cyan', width=5),
                marker=dict(size=[3, 8], color=['cyan', 'yellow']),
                name="Data Tower",
                text=f"Transactions: {data_point['data']['tx_count']}"
            ))
    
    # Add user avatars
    if 'user_avatars' in world_data:
        avatar_positions = world_data['user_avatars'][:20]  # Limit avatars
        fig.add_trace(go.Scatter3d(
            x=[av['position']['x'] for av in avatar_positions],
            y=[av['position']['z'] for av in avatar_positions],
            z=[av['position']['y'] + 1.8 for av in avatar_positions],  # Human height
            mode='markers',
            marker=dict(
                size=6,
                color='green',
                symbol='circle'
            ),
            name="Users",
            text=[f"User: {av['user_id']}" for av in avatar_positions]
        ))
    
    fig.update_layout(
        title=f"🌍 VR World Preview: {world_data.get('world_info', {}).get('name', 'Unknown')}",
        scene=dict(
            xaxis_title="X Coordinate",
            yaxis_title="Z Coordinate", 
            zaxis_title="Y Coordinate (Height)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            ),
            aspectmode='cube'
        ),
        height=600,
        showlegend=True
    )
    
    return fig

def create_webxr_interface():
    """Create WebXR interface"""
    st.markdown("""
    <div style="border: 2px solid #FF6B6B; border-radius: 15px; padding: 20px; background: linear-gradient(135deg, #FFE8E8 0%, #FFF0F0 100%);">
        <h3>🥽 WebXR Virtual Reality</h3>
        <div style="text-align: center;">
            <div style="display: inline-block; padding: 30px; background: #1a1a1a; border-radius: 15px; color: white; margin: 10px;">
                <h4>🎮 VR Session</h4>
                <p>Compatible browsers: Chrome, Firefox, Edge</p>
                <p>Supported devices: Oculus, HTC Vive, Windows Mixed Reality</p>
                <button onclick="enterVR()" style="background: #FF6B6B; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 16px; cursor: pointer;">
                    🚀 Enter VR
                </button>
            </div>
        </div>
    </div>
    
    <script>
    async function enterVR() {
        if (navigator.xr) {
            try {
                const session = await navigator.xr.requestSession('immersive-vr');
                console.log('VR session started');
                // Initialize VR scene here
            } catch (error) {
                console.error('VR not supported or permission denied');
                alert('VR not available. Please use a compatible browser and device.');
            }
        } else {
            alert('WebXR not supported in this browser');
        }
    }
    </script>
    """, unsafe_allow_html=True)

def create_blockchain_3d_visualization(block_data: List[Dict], tx_data: List[Dict]):
    """Create 3D blockchain visualization"""
    
    fig = go.Figure()
    
    # Create blockchain as connected blocks
    block_positions = []
    for i, block in enumerate(block_data[:20]):  # Last 20 blocks
        x = i * 5  # Spread blocks along X axis
        y = 0
        z = len(block.get('transactions', [])) / 10  # Height based on tx count
        
        block_positions.append({'x': x, 'y': y, 'z': z, 'block': block})
        
        # Add block as a cube (simplified as sphere)
        fig.add_trace(go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode='markers',
            marker=dict(
                size=max(5, len(block.get('transactions', []))),
                color=i,  # Color by age
                colorscale='Viridis',
                opacity=0.8
            ),
            name=f"Block {block.get('height', i)}",
            text=f"Block {block.get('height', i)}<br>Transactions: {len(block.get('transactions', []))}<br>Hash: {block.get('hash', 'unknown')[:16]}..."
        ))
    
    # Connect blocks with lines
    if len(block_positions) > 1:
        fig.add_trace(go.Scatter3d(
            x=[pos['x'] for pos in block_positions],
            y=[pos['y'] for pos in block_positions],
            z=[pos['z'] for pos in block_positions],
            mode='lines',
            line=dict(color='cyan', width=3),
            name="Blockchain",
            showlegend=False
        ))
    
    # Add transaction flows
    for i, tx in enumerate(tx_data[:50]):  # Limit transactions
        # Random positions for transaction visualization
        start_x = np.random.uniform(0, len(block_positions) * 5)
        end_x = np.random.uniform(0, len(block_positions) * 5)
        
        fig.add_trace(go.Scatter3d(
            x=[start_x, end_x],
            y=[np.random.uniform(-10, 10), np.random.uniform(-10, 10)],
            z=[np.random.uniform(0, 5), np.random.uniform(0, 5)],
            mode='lines',
            line=dict(
                color='orange',
                width=max(1, tx.get('amount', 0) / 1000000),  # Width based on amount
                dash='dot'
            ),
            opacity=0.6,
            showlegend=False,
            text=f"TX: {tx.get('amount', 0) / 1000000:.2f} HYBRID"
        ))
    
    fig.update_layout(
        title="🔗 3D Blockchain Visualization",
        scene=dict(
            xaxis_title="Block Sequence",
            yaxis_title="Network Spread",
            zaxis_title="Transaction Volume",
            camera=dict(
                eye=dict(x=1.2, y=1.2, z=1.2)
            )
        ),
        height=600
    )
    
    return fig

def create_nft_gallery_3d(nft_data: List[Dict]):
    """Create 3D NFT gallery"""
    
    fig = go.Figure()
    
    # Gallery layout - circular arrangement
    n_nfts = len(nft_data)
    radius = 10
    
    for i, nft in enumerate(nft_data):
        angle = (i / n_nfts) * 2 * np.pi
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = np.random.uniform(0, 3)  # Random height for variety
        
        # NFT as a marker
        fig.add_trace(go.Scatter3d(
            x=[x],
            y=[y],
            z=[z],
            mode='markers',
            marker=dict(
                size=15,
                color=nft.get('rarity_color', 'blue'),
                symbol='square',
                opacity=0.8
            ),
            name=nft.get('name', f'NFT {i}'),
            text=f"{nft.get('name', f'NFT {i}')}<br>Type: {nft.get('type', 'Unknown')}<br>Price: {nft.get('price', 0)} HYBRID"
        ))
        
        # Add a frame around each NFT
        frame_size = 1
        fig.add_trace(go.Mesh3d(
            x=[x-frame_size, x+frame_size, x+frame_size, x-frame_size],
            y=[y-frame_size, y-frame_size, y+frame_size, y+frame_size],
            z=[z, z, z, z],
            i=[0, 0],
            j=[1, 2],
            k=[2, 3],
            opacity=0.3,
            color='gold',
            showlegend=False
        ))
    
    # Add gallery floor
    floor_x = np.linspace(-15, 15, 10)
    floor_y = np.linspace(-15, 15, 10)
    X_floor, Y_floor = np.meshgrid(floor_x, floor_y)
    Z_floor = np.zeros_like(X_floor) - 1
    
    fig.add_trace(go.Surface(
        x=X_floor, y=Y_floor, z=Z_floor,
        colorscale=[[0, 'lightgray'], [1, 'darkgray']],
        showscale=False,
        opacity=0.5,
        name="Gallery Floor"
    ))
    
    fig.update_layout(
        title="🎨 3D NFT Gallery",
        scene=dict(
            xaxis_title="Gallery X",
            yaxis_title="Gallery Y",
            zaxis_title="Display Height",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=0.5)
            ),
            aspectmode='cube'
        ),
        height=600
    )
    
    return fig

def create_trading_floor_vr(trading_data: Dict):
    """Create VR trading floor visualization"""
    
    fig = go.Figure()
    
    # Trading desks in a grid
    desk_positions = []
    for i in range(5):  # 5 rows
        for j in range(10):  # 10 columns
            x = j * 3
            y = i * 4
            z = 0
            
            desk_positions.append({'x': x, 'y': y, 'z': z})
            
            # Trading desk
            fig.add_trace(go.Scatter3d(
                x=[x],
                y=[y], 
                z=[z + 1],  # Desk height
                mode='markers',
                marker=dict(
                    size=8,
                    color='brown',
                    symbol='square'
                ),
                name=f"Desk {i}-{j}",
                showlegend=False,
                text=f"Trading Desk {i*10 + j}<br>Active Trades: {np.random.randint(1, 20)}"
            ))
            
            # Trading screens above desks
            fig.add_trace(go.Scatter3d(
                x=[x],
                y=[y],
                z=[z + 2.5],  # Screen height
                mode='markers',
                marker=dict(
                    size=12,
                    color='lime' if np.random.random() > 0.5 else 'red',  # Green/red for profit/loss
                    symbol='square',
                    opacity=0.8
                ),
                name=f"Screen {i}-{j}",
                showlegend=False,
                text=f"Price: ${np.random.uniform(8, 12):.2f}<br>Change: {np.random.uniform(-5, 5):.1f}%"
            ))
    
    # Central trading board
    fig.add_trace(go.Scatter3d(
        x=[15],  # Center
        y=[10],
        z=[5],   # Elevated
        mode='markers',
        marker=dict(
            size=30,
            color='gold',
            symbol='diamond'
        ),
        name="Central Board",
        text="HYBRID Trading Floor<br>Volume: $2.3M<br>Active Traders: 145"
    ))
    
    # Price movement visualization
    price_history = np.random.cumsum(np.random.randn(50)) + 10
    time_points = np.linspace(0, 30, 50)
    
    fig.add_trace(go.Scatter3d(
        x=time_points,
        y=[20] * 50,  # Fixed Y position
        z=price_history,
        mode='lines+markers',
        line=dict(color='cyan', width=5),
        marker=dict(size=3, color='cyan'),
        name="HYBRID Price",
        text=[f"Price: ${price:.2f}" for price in price_history]
    ))
    
    fig.update_layout(
        title="💹 VR Trading Floor",
        scene=dict(
            xaxis_title="Trading Floor X",
            yaxis_title="Trading Floor Y",
            zaxis_title="Height / Price",
            camera=dict(
                eye=dict(x=1, y=1, z=0.8)
            ),
            aspectmode='manual',
            aspectratio=dict(x=2, y=1, z=0.5)
        ),
        height=600
    )
    
    return fig

# Export components
__all__ = [
    'create_ar_camera_interface',
    'create_vr_world_preview', 
    'create_webxr_interface',
    'create_blockchain_3d_visualization',
    'create_nft_gallery_3d',
    'create_trading_floor_vr'
]
