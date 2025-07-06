
#!/usr/bin/env python3
import asyncio
import click
import json
import requests
from typing import Dict, Any
from blockchain.hybrid_node import create_hybrid_node, NodeType
from blockchain.hybrid_wallet import hybrid_wallet_manager, get_founder_wallet, create_hybrid_wallet

@click.group()
def cli():
    """HYBRID Blockchain CLI Tool"""
    pass

@cli.command()
@click.option('--node-type', default='storage', type=click.Choice(['validator', 'storage', 'full']))
@click.option('--rpc-port', default=26657)
@click.option('--p2p-port', default=26656)
def start_node(node_type: str, rpc_port: int, p2p_port: int):
    """Start a HYBRID blockchain node"""
    click.echo(f"Starting HYBRID {node_type} node...")
    
    async def run_node():
        node = create_hybrid_node(node_type)
        node.rpc_port = rpc_port
        node.p2p_port = p2p_port
        
        try:
            await node.start()
        except KeyboardInterrupt:
            await node.stop()
            click.echo("Node stopped.")
    
    asyncio.run(run_node())

@cli.command()
@click.option('--rpc-url', default='http://0.0.0.0:26657')
def node_status(rpc_url: str):
    """Get node status"""
    try:
        response = requests.get(f"{rpc_url}/status")
        if response.status_code == 200:
            status = response.json()
            click.echo(f"Node ID: {status['node_id']}")
            click.echo(f"Node Type: {status['node_type']}")
            click.echo(f"Height: {status['height']}")
            click.echo(f"Running: {status['is_running']}")
        else:
            click.echo("Failed to get node status")
    except Exception as e:
        click.echo(f"Error connecting to node: {e}")

@cli.command()
@click.argument('address')
@click.option('--rpc-url', default='http://0.0.0.0:26657')
def balance(address: str, rpc_url: str):
    """Get account balance"""
    try:
        response = requests.get(f"{rpc_url}/balance/{address}")
        if response.status_code == 200:
            data = response.json()
            balance_hybrid = data['balance'] / 1_000_000  # Convert from micro-HYBRID
            click.echo(f"Address: {data['address']}")
            click.echo(f"Balance: {balance_hybrid:.6f} HYBRID")
        else:
            click.echo("Failed to get balance")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.option('--from-addr', required=True)
@click.option('--to-addr', required=True)
@click.option('--amount', required=True, type=float)
@click.option('--rpc-url', default='http://0.0.0.0:26657')
def send(from_addr: str, to_addr: str, amount: float, rpc_url: str):
    """Send HYBRID tokens"""
    try:
        tx_data = {
            "from": from_addr,
            "to": to_addr,
            "amount": int(amount * 1_000_000),  # Convert to micro-HYBRID
            "fee": 1000
        }
        
        response = requests.post(f"{rpc_url}/tx/send", json=tx_data)
        if response.status_code == 200:
            result = response.json()
            click.echo(f"Transaction sent: {result['tx_hash']}")
        else:
            click.echo("Failed to send transaction")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.argument('htsx_file')
@click.option('--rpc-url', default='http://0.0.0.0:26657')
def execute_htsx(htsx_file: str, rpc_url: str):
    """Execute HTSX file on the blockchain"""
    try:
        with open(htsx_file, 'r') as f:
            htsx_content = f.read()
        
        response = requests.post(f"{rpc_url}/htsx/execute", json={"content": htsx_content})
        if response.status_code == 200:
            result = response.json()
            click.echo("HTSX execution result:")
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo("Failed to execute HTSX")
    except Exception as e:
        click.echo(f"Error: {e}")

@cli.command()
@click.option('--license-type', default='storage', type=click.Choice(['validator', 'storage']))
@click.option('--owner', required=True)
def issue_license(license_type: str, owner: str):
    """Issue a node license NFT"""
    import uuid
    token_id = f"license_{uuid.uuid4().hex[:8]}"
    
    click.echo(f"Issuing {license_type} license NFT:")
    click.echo(f"Token ID: {token_id}")
    click.echo(f"Owner: {owner}")
    click.echo(f"Type: {license_type}")

@cli.group()
def wallet():
    """HYBRID wallet management commands"""
    pass

@wallet.command()
def founder():
    """Show founder wallet information"""
    founder = get_founder_wallet()
    click.echo("👑 HYBRID Founder Wallet")
    click.echo("=" * 40)
    click.echo(f"Address: {founder.address}")
    click.echo(f"Label: {founder.label}")
    click.echo(f"Balance: {founder.balance / 1_000_000:,.2f} HYBRID")
    click.echo(f"USD Value: ${founder.balance / 1_000_000 * 10:,.2f} (at $10/HYBRID)")
    click.echo(f"Created: {founder.created_at}")

@wallet.command()
@click.option('--label', default='', help='Wallet label')
def create(label: str):
    """Create a new HYBRID wallet"""
    new_wallet = create_hybrid_wallet(label)
    click.echo("📱 New HYBRID Wallet Created")
    click.echo("=" * 40)
    click.echo(f"Address: {new_wallet.address}")
    click.echo(f"Label: {new_wallet.label}")
    click.echo(f"Mnemonic: {new_wallet.mnemonic}")
    click.echo(f"Balance: {new_wallet.balance / 1_000_000:,.2f} HYBRID")
    click.echo("\n⚠️ IMPORTANT: Save your mnemonic phrase securely!")

@wallet.command()
def list():
    """List all wallets"""
    wallets = hybrid_wallet_manager.list_wallets()
    click.echo("📋 HYBRID Wallets")
    click.echo("=" * 60)
    
    for wallet in wallets:
        status = "👑 FOUNDER" if wallet.address == hybrid_wallet_manager.founder_address else "📱 USER"
        click.echo(f"{status} {wallet.address[:20]}... | {wallet.balance / 1_000_000:>12,.2f} HYBRID | {wallet.label}")

@wallet.command()
@click.argument('address')
def info(address: str):
    """Get wallet information"""
    wallet = hybrid_wallet_manager.get_wallet(address)
    if wallet:
        click.echo(f"📱 Wallet Information")
        click.echo("=" * 40)
        click.echo(f"Address: {wallet.address}")
        click.echo(f"Label: {wallet.label}")
        click.echo(f"Balance: {wallet.balance / 1_000_000:,.6f} HYBRID")
        click.echo(f"Created: {wallet.created_at}")
        if wallet.address == hybrid_wallet_manager.founder_address:
            click.echo("👑 Status: FOUNDER WALLET")
    else:
        click.echo(f"❌ Wallet not found: {address}")

@wallet.command()
@click.option('--from-addr', required=True, help='Sender address')
@click.option('--to-addr', required=True, help='Recipient address')
@click.option('--amount', required=True, type=float, help='Amount in HYBRID')
def transfer(from_addr: str, to_addr: str, amount: float):
    """Transfer HYBRID tokens between wallets"""
    amount_micro = int(amount * 1_000_000)
    
    success = hybrid_wallet_manager.transfer(from_addr, to_addr, amount_micro)
    
    if success:
        click.echo(f"✅ Successfully transferred {amount} HYBRID")
        click.echo(f"From: {from_addr}")
        click.echo(f"To: {to_addr}")
        
        # Show updated balances
        from_balance = hybrid_wallet_manager.get_balance_hybrid(from_addr)
        to_balance = hybrid_wallet_manager.get_balance_hybrid(to_addr)
        click.echo(f"Sender balance: {from_balance:,.6f} HYBRID")
        click.echo(f"Recipient balance: {to_balance:,.6f} HYBRID")
    else:
        click.echo(f"❌ Transfer failed - insufficient balance or invalid addresses")

if __name__ == '__main__':
    cli()
