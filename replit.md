
# HYBRID Blockchain + HTSX Integration

This is a revolutionary blockchain project that combines the HYBRID Blockchain (built on Cosmos SDK) with HTSX runtime - a declarative component system for Web3 development.

## Project Overview

The HYBRID Blockchain is a Layer 1 blockchain featuring:
- **Native Coin**: HYBRID (not a token) - 100 billion total supply
- **Consensus**: Tendermint BFT with 5-second block times
- **Multi-chain**: Integrated with Base, Polygon, and Solana
- **NFT Licensing**: Node operators require NFT licenses to participate
- **HTSX Runtime**: Declarative blockchain components for dApp development

## Key Components

### Blockchain Core (`/blockchain/`)
- `hybrid_node.py` - Core blockchain node implementation
- `wallet_manager.py` - Multi-chain wallet system with founder wallet
- `spiral_trust_engine.py` - SpiralScript trust computation engine
- `multi_ai_orchestrator.py` - AI-powered blockchain optimization
- `holographic_blockchain_engine.py` - 3D visualization and holographic rendering

### HTSX System (`/components/`)
- `hybrid_htsx.py` - Declarative blockchain component system
- Components include wallet connectors, NFT licenses, cross-chain bridges, node operators

### User Interface (`/ui/`)
- `streamlit_ui.py` - Main Web UI built with Streamlit
- `admin_dashboard.py` - Admin interface for blockchain management
- `holographic_interface.py` - 3D/AR/VR blockchain visualization

### Examples (`/examples/`)
- `defi_protocol.htsx` - Example DeFi protocol in HTSX
- `node_operator.htsx` - Example node operator dashboard

## HTSX Syntax

HTSX files combine HTML, TypeScript, and blockchain components:

```htsx
<htsx>
  <html>
    <head><title>My HYBRID dApp</title></head>
    <body>
      <wallet-connector chains="hybrid,base,polygon" required="true" />
      <hybrid-coin balance="display" utilities="all" />
      <nft-license type="storage" price="100" currency="HYBRID" />
      
      <script lang="hybrid">
        class MyDApp {
          async initialize() {
            const balance = await hybridChain.getBalance();
            console.log(`Balance: ${balance} HYBRID`);
          }
        }
      </script>
    </body>
  </html>
</htsx>
```

## Available Components

- `<wallet-connector>` - Multi-chain wallet connection
- `<nft-license>` - Node license management
- `<cross-chain-bridge>` - Token bridging between chains
- `<node-operator>` - Node operation dashboard
- `<hybrid-coin>` - HYBRID token utilities
- `<liquidity-pool>` - DeFi liquidity pools
- `<staking-vault>` - Token staking interface
- `<governance-dao>` - DAO governance tools

## Development Commands

- `python start_hybrid.py` - Start the full HYBRID blockchain node + UI
- `python main.py` - Run Streamlit UI only
- `python health_check.py` - Check system health
- `python test_stress.py` - Run stress tests

## API Endpoints

When running, the system exposes:
- **UI**: http://0.0.0.0:8501 (Streamlit interface)
- **RPC**: http://0.0.0.0:26657 (Blockchain RPC)
- **Admin**: http://0.0.0.0:8501?admin=true (Admin dashboard)

## Key Features

1. **Multi-chain Integration**: Native support for Ethereum, Polygon, Solana, and Base
2. **NFT-Gated Nodes**: Requires NFT ownership to operate blockchain nodes
3. **SpiralScript Engine**: Advanced trust computation and currency minting
4. **Holographic UI**: 3D blockchain visualization and AR/VR interfaces
5. **AI Integration**: Multi-AI orchestration for optimization and security
6. **HTSX Runtime**: Declarative Web3 component system

## Architecture

The system uses a hybrid architecture:
- **Cosmos SDK** for the blockchain layer
- **Streamlit** for the web interface
- **Python** for backend logic
- **HTSX** for declarative blockchain components
- **WebAssembly** for high-performance computations

## Configuration

Key configuration files:
- `.streamlit/config.toml` - Streamlit configuration
- `requirements.txt` - Python dependencies
- `start_hybrid.py` - Main startup script

## Development Tips

1. Use `python start_hybrid.py` to run the full system
2. The founder wallet is automatically created with 10B HYBRID tokens
3. HTSX files can be edited in real-time and hot-reloaded
4. The admin dashboard provides deep blockchain insights
5. All components are designed to work offline and online

## License

MIT License with NFT Clause - Open source with node operation requiring NFT ownership.

## Support

For questions about HTSX syntax, blockchain integration, or component development, refer to the extensive documentation in `/docs/` and example files in `/examples/`.
