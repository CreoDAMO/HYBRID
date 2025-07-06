# HYBRID Blockchain — Technical Implementation v0.1.0

[![MIT License with NFT Clause](https://img.shields.io/badge/license-MIT%20%2B%20NFT-blue.svg)](LICENSE)
[![Cosmos SDK](https://img.shields.io/badge/cosmos--sdk-v0.47-green.svg)](https://cosmos.network)
[![Ethermint](https://img.shields.io/badge/ethermint-EVM%20compatible-orange.svg)](https://ethermint.dev)

---

## Overview of HYBRID Blockchain
The HYBRID Blockchain is a Layer 1 blockchain built with the Cosmos SDK v0.47, featuring:

### 🏗️ Core Architecture
- **Chain ID**: `hybrid-1` (mainnet) / `hybrid-test-1` (testnet)
- **Consensus**: Tendermint BFT (5s block time, 2/3+1 voting power)
- **Address Prefix**: `hybrid` (Bech32 format)
- **Token**: `uhybrid` (1 HYBRID = 1,000,000 uhybrid)

### 💰 Token Economics
- **Total Supply**: 100,000,000,000 HYBRID (100 Billion)
- **Genesis Allocation**: 10B HYBRID to founder wallet (10% of total supply)
- **Inflation**: 7% → 2% taper over 8 years
- **Block Rewards**: 50% validators, 20% storage, 20% community, 10% dev fund

### 🔗 Multi-Chain Integration
- **Base/Polygon**: `0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79`
- **Solana**: `3E8keZHkH1AHvRfbmq44tEmBgJYz1NjkhBE41C4gJHUn`
- **HYBRID Native**: Auto-generated founder wallet pre-funded with 10B HYBRID tokens

## 👑 HYBRID Native Wallet System

### Founder Wallet (Genesis)
The HYBRID blockchain includes a native wallet system with the founder wallet automatically generated and pre-funded:

- **Purpose**: Founder, Lead Engineer & Developer genesis wallet
- **Initial Supply**: 100,000,000 HYBRID tokens
- **Address Format**: Bech32 with `hybrid` prefix (e.g., `hybrid1abc123...`)
- **Features**: 
  - Ed25519 cryptographic keys
  - 24-word mnemonic phrase
  - Native $HYBRID balance tracking
  - Wallet creation and funding capabilities

## 🧩 Core Modules

### x/licence Module
NFT-gated node participation system:
- **Validator License (HNL-VAL)**: 1,000 HYBRID mint price
- **Storage License (HNL-STR)**: 250 HYBRID mint price
- Cross-chain license verification via relayer
- Delegation support for license owners
- Slashing protection with blacklisting

### x/naas Module  
Node-as-a-Service delegation:
- **Revenue Split**: 70% owner, 30% operator (default)
- Provider registration with uptime guarantees
- Automated reward distribution
- Delegation management

### x/moe Module
AI Mixture-of-Experts integration:
- On-chain model registry (IPFS-backed)
- Inference call coordination
- **Fee Structure**: 90% to experts, 10% burned
- Expert reputation system
- gRPC inference gateway

### Ethermint EVM Subsystem
- **EVM Compatibility**: Dual-state (SDK + EVM) from block 1
- **Gas Token**: uhybrid (1 gwei ≈ 0.001 uhybrid)
- **Precompiles**: NFT license verification at 0x000...HNL
- Solidity contract verification via Sourcify

### Native Wallet System
- **Secure Key Management**: Ed25519 cryptographic keys
- **Bech32 Addresses**: Standard Cosmos ecosystem format (`hybrid1...`)
- **Multi-Wallet Support**: Create unlimited wallets with founder funding
- **24-Word Recovery**: BIP-39 mnemonic phrases
- **Cross-Chain Bridge**: Integrated Axelar/Wormhole support

The blockchain uses $HYBRID tokens for all operations, with NFT licenses required for node participation.

---

## Licensing the HYBRID Blockchain

### Recommended License: MIT License with NFT Clause
The **MIT License with NFT Clause** is ideal for the HYBRID Blockchain, balancing open-source principles with controlled node operation.

#### Why MIT with NFT Clause?
1. **Open-Source and Permissive**:
   - Allows developers to use, modify, and distribute the codebase, fostering community contributions and aligning with Web3’s ethos.
   - Familiar to blockchain developers (e.g., used by OpenZeppelin, Cosmos SDK).

2. **NFT-Based Node Licensing**:
   - The NFT clause ensures that operating Storage or Validator Nodes requires a valid HYBRID Node License NFT, aligning with the economic model (transaction fee rewards in $HYBRID) ().
   - Balances open-source access with controlled network participation.

3. **Decentralization and Governance**:
   - Supports community-driven development and potential MultiChainDAO governance without restrictive copyleft requirements.

4. **Commercial Flexibility**:
   - Enables monetization through NFT sales and $HYBRID rewards while allowing others to build on the platform.

5. **Blockchain Compatibility**:
   - Suitable for immutable components (smart contracts, consensus logic) without impractical obligations like source code disclosure for derivatives.

#### License Text
```text
MIT License with NFT Clause

Copyright (c) 2025 HYBRID Blockchain

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

2. Operation of HYBRID Blockchain Storage or Validator Nodes requires ownership
   of a valid HYBRID Node License NFT, issued by the HYBRID Blockchain team.
   Node operation without a valid NFT is prohibited, and the Software will not
   permit network participation without NFT verification.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

#### Implementation Steps
1. **Add to Repository**:
   ```bash
   echo "[MIT License with NFT Clause Above]" > LICENSE
   git add LICENSE
   git commit -m "Add MIT License with NFT Clause for HYBRID Blockchain"
   git push
   ```

2. **Add SPDX Identifiers**:
   - **Solidity**:
     ```solidity
     // SPDX-License-Identifier: MIT
     pragma solidity ^0.8.20;
     ```
   - **Rust (Solana)**:
     ```rust
     // SPDX-License-Identifier: MIT
     use anchor_lang::prelude::*;
     ```
   - **Go (Cosmos SDK)**:
     ```go
     // SPDX-License-Identifier: MIT
     package main
     ```

3. **Update README**:
   ```markdown
   ## License
   The HYBRID Blockchain is licensed under the MIT License with an NFT Clause. See the [LICENSE](LICENSE) file for details. Operating Storage or Validator Nodes requires a valid HYBRID Node License NFT.
   ```

4. **NFT Verification**:
   - Integrate NFT checks in node software:
     ```go
     package main
     import (
         "github.com/hybridchain/x/nft"
         "github.com/cosmos/cosmos-sdk/server"
     )
     func VerifyNodeLicense(nftID string, address types.AccAddress) bool {
         return nft.IsOwner(address, nftID)
     }
     ```

5. **NFT Contract**:
   ```solidity
   // SPDX-License-Identifier: MIT
   pragma solidity ^0.8.20;
   import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

   contract HybridNodeLicense is ERC721 {
       constructor() ERC721("HybridNodeLicense", "HNL") {}
       function mint(address to, uint256 tokenId) external {
           _mint(to, tokenId);
       }
   }
   ```

---

## Addressing the Five Tasks for HYBRID Blockchain

### 1. Detailed Test Script for Wallet Interactions
This script tests wallet interactions for HYBRID Blockchain node operations, including NFT verification, balance checks, and $HYBRID transactions.

**`test/hybridWalletInteractions.test.js`**:
```javascript
const { ethers } = require("hardhat");
const { Connection, PublicKey } = require("@solana/web3.js");
const { expect } = require("chai");
const { execSync } = require("child_process");

describe("HYBRID Blockchain Wallet Interactions", function () {
  const evmWalletAddress = "0xCc380FD8bfbdF0c020de64075b86C84c2BB0AE79";
  const solanaWalletAddress = new PublicKey("3E8keZHkH1AHvRfbmq44tEmBgJYz1NjkhBE41C4gJHUn");
  const hybridWalletAddress = "hybrid1q2w3e4r5t6y7u8i9o0p";
  const networkConfig = {
    base: { rpc: "https://mainnet.base.org", chainId: 8453 },
    polygon: { rpc: "https://polygon-rpc.com", chainId: 137 },
    solana: { rpc: "https://api.mainnet-beta.solana.com" },
    hybrid: { rpc: "http://localhost:26657" },
  };

  let hybridClient, solanaConn, provider, nftContract;

  before(async function () {
    provider = new ethers.providers.JsonRpcProvider(networkConfig.base.rpc);
    solanaConn = new Connection(networkConfig.solana.rpc, "confirmed");
    hybridClient = {
      queryBalance: (address) => execSync(`hybridchaind query bank balances ${address} --node ${networkConfig.hybrid.rpc} --output json`),
      queryNFT: (address, nftId) => execSync(`hybridchaind query nft owner ${nftId} --node ${networkConfig.hybrid.rpc} --output json`),
      sendTx: (from, to, amount) => execSync(`hybridchaind tx bank send ${from} ${to} ${amount}uhybrid --node ${networkConfig.hybrid.rpc} --chain-id hybrid-mainnet --yes`),
    };
    const HybridNodeLicense = await ethers.getContractFactory("HybridNodeLicense");
    nftContract = await HybridNodeLicense.deploy();
  });

  it("should verify EVM wallet balance (Base)", async function () {
    const balance = await provider.getBalance(evmWalletAddress);
    expect(balance).to.be.gt(0, "Base wallet balance should be greater than 0");
    console.log(`Base Wallet Balance: ${ethers.utils.formatEther(balance)} ETH`);
  });

  it("should verify EVM wallet balance (Polygon)", async function () {
    const polygonProvider = new ethers.providers.JsonRpcProvider(networkConfig.polygon.rpc);
    const balance = await polygonProvider.getBalance(evmWalletAddress);
    expect(balance).to.be.gt(0, "Polygon wallet balance should be greater than 0");
    console.log(`Polygon Wallet Balance: ${ethers.utils.formatEther(balance)} MATIC`);
  });

  it("should verify Solana wallet balance", async function () {
    const balance = await solanaConn.getBalance(solanaWalletAddress);
    expect(balance).to.be.gt(0, "Solana wallet balance should be greater than 0");
    console.log(`Solana Wallet Balance: ${balance / 1_000_000_000} SOL`);
  });

  it("should verify HybridChain wallet balance", async function () {
    const balanceOutput = hybridClient.queryBalance(hybridWalletAddress);
    const balance = JSON.parse(balanceOutput).balances.find((b) => b.denom === "uhybrid").amount;
    expect(balance).to.be.gt(0, "Hybrid wallet balance should be greater than 0");
    console.log(`Hybrid Wallet Balance: ${balance / 1_000_000} HYBRID`);
  });

  it("should verify HYBRID Node License NFT ownership", async function () {
    await nftContract.mint(evmWalletAddress, 1);
    const owner = await nftContract.ownerOf(1);
    expect(owner).to.equal(evmWalletAddress, "Wallet should own the NFT");
  });

  it("should submit a $HYBRID transaction", async function () {
    const txOutput = hybridClient.sendTx(hybridWalletAddress, "hybrid1anotheraddress", "1000000");
    const tx = JSON.parse(txOutput);
    expect(tx.code).to.equal(0, "Transaction should succeed");
  });
});
```

**Running**:
```bash
npm install --save-dev hardhat @solana/web3.js chai jest
npx hardhat test test/hybridWalletInteractions.test.js
```
**Prerequisites**:
- Fund wallets: ETH (Base), MATIC (Polygon), SOL (Solana), $HYBRID (HybridChain).
- Deploy `HybridNodeLicense` contract on Base.
- Run a local HybridChain node.

---

### 2. Canvas Panel for Wallet Connections
This Mermaid diagram visualizes wallet connections for the HYBRID Blockchain across Base, Polygon, Solana, and HybridChain, emphasizing node operations and NFT licensing.

```mermaid
graph TD
    A[HYBRID Blockchain <br> Node Software] -->|Connects| B[Wallet Connector]
    B -->|EVM (MetaMask)| C[Base/Polygon Wallet <br> 0xCc380FD8...]
    B -->|Solana (Phantom)| D[Solana Wallet <br> 3E8keZHk...]
    B -->|Cosmos SDK| E[HybridChain Wallet <br> hybrid1q2w3e4...]
    C -->|RPC: https://mainnet.base.org| F[Base Chain]
    C -->|RPC: https://polygon-rpc.com| G[Polygon Chain]
    D -->|RPC: https://api.mainnet-beta.solana.com| H[Solana Chain]
    E -->|RPC: http://localhost:26657| I[HybridChain]
    F -->|Axelar/Wormhole| I
    G -->|Axelar/Wormhole| I
    H -->|Wormhole| I
    I -->|NFT License Verification| J[Node License NFT Contract]
    I -->|Transaction Fees| K[$HYBRID Rewards]
    classDef blockchain fill:#3498db,stroke:#fff,color:#fff
    classDef connector fill:#f1c40f,stroke:#fff,color:#000
    classDef wallet fill:#2ecc71,stroke:#fff,color:#000
    classDef chain fill:#6f42c1,stroke:#fff,color:#fff
    classDef external fill:#ff6b6b,stroke:#fff,color:#000
    class A blockchain
    class B connector
    class C,D,E wallet
    class F,G,H,I chain
    class J,K external
```

**Usage**:
- Paste into `mermaid.live` to visualize.
- **Interpretation**: The node software connects wallets via MetaMask, Phantom, or Cosmos SDK. HybridChain verifies NFT licenses before allowing node operation, with cross-chain interactions via Axelar/Wormhole.

---

### 3. Solana Program for HYBRID Blockchain Payments
This program handles $HYBRID token payments (bridged as SPL tokens) for node license purchases.

**`programs/hybrid/src/lib.rs`**:
```rust
// SPDX-License-Identifier: MIT
use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};

declare_id!("HybridPay1111111111111111111111111111111111");

#[program]
pub mod hybrid {
    use super::*;

    pub fn initialize_payment(ctx: Context<InitializePayment>, payment_id: u64, amount: u64) -> Result<()> {
        let payment = &mut ctx.accounts.payment;
        payment.payment_id = payment_id;
        payment.buyer = ctx.accounts.buyer.key();
        payment.recipient = ctx.accounts.recipient.key();
        payment.amount = amount;
        payment.status = PaymentStatus::Pending;
        Ok(())
    }

    pub fn pay_with_spl(ctx: Context<PayWithSpl>, payment_id: u64, amount: u64) -> Result<()> {
        let payment = &mut ctx.accounts.payment;
        require!(payment.payment_id == payment_id, ErrorCode::InvalidPayment);
        require!(payment.status == PaymentStatus::Pending, ErrorCode::InvalidStatus);

        let transfer = Transfer {
            from: ctx.accounts.buyer_token_account.to_account_info(),
            to: ctx.accounts.recipient_token_account.to_account_info(),
            authority: ctx.accounts.buyer.to_account_info(),
        };
        token::transfer(CpiContext::new(ctx.accounts.token_program.to_account_info(), transfer), amount)?;

        payment.status = PaymentStatus::Completed;
        emit!(PaymentProcessed {
            payment_id,
            buyer: ctx.accounts.buyer.key(),
            amount,
            currency: "HYBRID".to_string(),
        });
        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(payment_id: u64)]
pub struct InitializePayment<'info> {
    #[account(init, payer = buyer, space = 8 + 8 + 32 + 32 + 8 + 1, seeds = [b"payment", payment_id.to_le_bytes().as_ref()], bump)]
    pub payment: Account<'info, Payment>,
    #[account(mut)]
    pub buyer: Signer<'info>,
    /// CHECK: Recipient is verified
    pub recipient: AccountInfo<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct PayWithSpl<'info> {
    #[account(mut, has_one = buyer, has_one = recipient)]
    pub payment: Account<'info, Payment>,
    #[account(mut)]
    pub buyer: Signer<'info>,
    #[account(mut)]
    pub buyer_token_account: Account<'info, TokenAccount>,
    #[account(mut)]
    /// CHECK: Recipient token account is verified
    pub recipient_token_account: AccountInfo<'info>,
    pub token_program: Program<'info, Token>,
}

#[account]
pub struct Payment {
    pub payment_id: u64,
    pub buyer: Pubkey,
    pub recipient: Pubkey,
    pub amount: u64,
    pub status: PaymentStatus,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, PartialEq)]
pub enum PaymentStatus {
    Pending,
    Completed,
}

#[event]
pub struct PaymentProcessed {
    pub payment_id: u64,
    pub buyer: Pubkey,
    pub amount: u64,
    pub currency: String,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Invalid payment ID")]
    InvalidPayment,
    #[msg("Invalid payment status")]
    InvalidStatus,
}
```

**Anchor.toml**:
```toml
[programs.mainnet]
hybrid = "HybridPay1111111111111111111111111111111111"
license = "MIT"

[registry]
url = "https://api.apr.dev"

[provider]
cluster = "mainnet-beta"
wallet = "/path/to/solana-wallet-keypair.json"

[scripts]
test = "yarn run ts-mocha -p ./tsconfig.json -t 1000000 tests/**/*.ts"
```

**Deployment**:
```bash
anchor build
anchor deploy --provider.cluster mainnet
```

**Frontend**:
```typescript
import { Connection, PublicKey } from "@solana/web3.js";
import { Program, AnchorProvider } from "@project-serum/anchor";

const processHybridPayment = async (paymentId: number, amount: number, recipient: string) => {
  const connection = new Connection("https://api.mainnet-beta.solana.com", "confirmed");
  const provider = new AnchorProvider(connection, window.solana, {});
  const program = new Program(idl, new PublicKey("HybridPay1111111111111111111111111111111111"), provider);
  await program.rpc.payWithSpl(new anchor.BN(paymentId), new anchor.BN(amount), {
    accounts: {
      payment: /* derive PDA */,
      buyer: provider.wallet.publicKey,
      buyerTokenAccount: /* buyer's SPL token account */,
      recipientTokenAccount: /* recipient's SPL token account */,
      tokenProgram: new PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
      systemProgram: anchor.web3.SystemProgram.programId,
    },
  });
};
```

---

### 4. Deep-Dive into HybridChain Node Setup
This details setting up Storage and Validator Nodes for the HYBRID Blockchain.

**Prerequisites**:
- **Hardware**: Validator: 8-core CPU, 16GB RAM, 500GB SSD; Storage: 4-core CPU, 8GB RAM, 200GB SSD.
- **OS**: Ubuntu 20.04.
- **Dependencies**:
  ```bash
  sudo apt update && sudo apt install -y git curl build-essential
  curl -sSL https://go.dev/dl/go1.20.5.linux-amd64.tar.gz | sudo tar -C /usr/local -xz
  export PATH=$PATH:/usr/local/go/bin
  ```

**Setup**:
1. **Install Ignite CLI**:
   ```bash
   curl https://get.ignite.com/cli | bash
   ```

2. **Clone Repository**:
   ```bash
   git clone https://github.com/hybridchain/hybridchain.git
   cd hybridchain
   ```

3. **Initialize Node**:
   - Validator:
     ```bash
     hybridchaind init validator-node --chain-id hybrid-mainnet
     ```
   - Storage:
     ```bash
     hybridchaind init storage-node --chain-id hybrid-mainnet
     ```

4. **Genesis File**:
   ```bash
   curl https://mainnet-files.hybridchain.local/genesis.json > ~/.hybridchaind/config/genesis.json
   ```

5. **Peers**:
   Update `~/.hybridchaind/config/config.toml`:
   ```toml
   [p2p]
   persistent_peers = "node1@peer1.hybridchain.local:26656,node2@peer2.hybridchain.local:26656"
   ```

6. **NFT Verification**:
   ```go
   // SPDX-License-Identifier: MIT
   package main
   import (
       "github.com/hybridchain/x/nft"
       "github.com/cosmos/cosmos-sdk/server"
   )
   func main() {
       if !nft.IsOwner(server.Context().FromAddress, "node_license_1") {
           panic("Invalid Node License NFT")
       }
       // Start node
   }
   ```

7. **Start Node**:
   - Validator:
     ```bash
     hybridchaind start --rpc.laddr tcp://0.0.0.0:26657 --mode validator
     ```
   - Storage:
     ```bash
     hybridchaind start --rpc.laddr tcp://0.0.0.0:26657
     ```

8. **Expose RPC**:
   ```bash
   sudo ufw allow 26657
   ```

9. **Fund Wallet**:
   ```bash
   hybridchaind tx bank send [your-address] hybrid1q2w3e4r5t6y7u8i9o0p 1000000uhybrid --node http://localhost:26657
   ```

**VPS**:
- Use DigitalOcean/AWS (4 vCPUs, 8GB RAM for Storage Nodes).
- Configure as above.

**Node-as-a-Service (NaaS)**:
- Delegate NFT to a NaaS provider ().

---

### 5. Simulated Cross-Chain Payment Workflow
This simulates purchasing a Storage Node License NFT using $HYBRID tokens bridged to Base.

**Workflow**:
1. **Deploy NFT Contract**:
   ```javascript
   const HybridNodeLicense = await ethers.getContractFactory("HybridNodeLicense");
   const nftContract = await HybridNodeLicense.deploy();
   ```

2. **Pay $HYBRID**:
   ```bash
   hybridchaind tx bank send hybrid1q2w3e4r5t6y7u8i9o0p hybrid1nftissuer 100000000uhybrid --node http://localhost:26657
   ```

3. **Bridge to Base (Axelar)**:
   ```javascript
   const Axelar = new ethers.Contract(axelarGateway, AxelarABI, provider.getSigner());
   await Axelar.sendToken("hybridchain", "base", "HYBRID", 100000000);
   ```

4. **Mint NFT**:
   ```javascript
   await nftContract.mint(evmWalletAddress, 1);
   ```

5. **Verify NFT**:
   ```bash
   hybridchaind query nft owner node_license_1 --node http://localhost:26657
   ```

**Output**:
```
Deploying NFT contract...
Contract Deployed: 0xNFTContractAddress
Initiating $HYBRID payment...
Tx Hash: hybrid_tx_123
Bridging to Base...
Bridge Tx: 0xbridge_tx_456
Minting NFT...
NFT Minted: Token ID 1, Owner 0xCc380FD8...
Verification: hybrid1q2w3e4r5t6y7u8i9o0p owns node_license_1
```

---

## Putting Everything Together
- **License**: The MIT License with NFT Clause ensures open-source access while requiring NFT ownership for node operation, embedded in all code (Solidity, Rust, Go) and documentation.
- **Test Script**: Verifies wallet interactions across Base, Polygon, Solana, and HybridChain, including NFT checks.
- **Canvas Panel**: Visualizes wallet connections, emphasizing node operations and cross-chain bridging.
- **Solana Program**: Handles $HYBRID payments for node licenses, integrated with the frontend.
- **Node Setup**: Provides detailed steps for Storage and Validator Nodes, with NFT verification.
- **Cross-Chain Workflow**: Simulates NFT license purchase, demonstrating interoperability.

**Directory Structure**:
```
hybridchain/
├── contracts/
│   ├── HybridNodeLicense.sol  # SPDX-License-Identifier: MIT
├── programs/
│   ├── hybrid/src/lib.rs      # SPDX-License-Identifier: MIT
├── test/
│   ├── hybridWalletInteractions.test.js  # SPDX-License-Identifier: MIT
├── cmd/hybridchaind/
│   ├── main.go                # SPDX-License-Identifier: MIT
├── LICENSE                    # MIT with NFT Clause
├── README.md                  # License details
```

---
## 1. Draft a NOTICE File for Dependencies

The `NOTICE` file credits third-party dependencies used in the HYBRID Blockchain, ensuring compliance with their licenses and providing transparency. Below is a `NOTICE` file based on the dependencies likely used in the HYBRID Blockchain codebase, including those referenced in the test script, Solana program, and node setup (e.g., Cosmos SDK, OpenZeppelin, Anchor).

### NOTICE File
```text
HYBRID Blockchain - NOTICE

The HYBRID Blockchain project incorporates the following third-party open-source software dependencies. Each component is subject to its respective license terms, as noted below. This NOTICE file ensures compliance with the licensing requirements of these dependencies.

1. Cosmos SDK
   - Description: Framework for building the HYBRID Blockchain node software.
   - Version: 0.47.0
   - License: Apache License 2.0
   - Source: https://github.com/cosmos/cosmos-sdk
   - Copyright: Copyright (c) 2018-2025 The Cosmos Authors
   - License Terms: See https://github.com/cosmos/cosmos-sdk/blob/main/LICENSE

2. OpenZeppelin Contracts
   - Description: Library for secure smart contract development (e.g., ERC721 for node license NFTs).
   - Version: 5.0.0
   - License: MIT License
   - Source: https://github.com/OpenZeppelin/openzeppelin-contracts
   - Copyright: Copyright (c) 2016-2025 OpenZeppelin
   - License Terms: See https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/LICENSE

3. Anchor Framework
   - Description: Framework for Solana program development (e.g., $HYBRID payment program).
   - Version: 0.30.0
   - License: Apache License 2.0
   - Source: https://github.com/coral-xyz/anchor
   - Copyright: Copyright (c) 2021-2025 Coral-XYZ
   - License Terms: See https://github.com/coral-xyz/anchor/blob/master/LICENSE

4. Hardhat
   - Description: Development environment for EVM-based testing (e.g., wallet interaction tests).
   - Version: 2.22.0
   - License: MIT License
   - Source: https://github.com/nomiclabs/hardhat
   - Copyright: Copyright (c) 2020-2025 Nomic Labs
   - License Terms: See https://github.com/nomiclabs/hardhat/blob/main/LICENSE

5. Solana Web3.js
   - Description: Library for interacting with Solana blockchain.
   - Version: 1.95.0
   - License: MIT License
   - Source: https://github.com/solana-labs/solana-web3.js
   - Copyright: Copyright (c) 2020-2025 Solana Labs
   - License Terms: See https://github.com/solana-labs/solana-web3.js/blob/master/LICENSE

6. Axelar SDK
   - Description: Library for cross-chain bridging (e.g., $HYBRID to Base).
   - Version: 0.13.0
   - License: MIT License
   - Source: https://github.com/axelarnetwork/axelarjs-sdk
   - Copyright: Copyright (c) 2021-2025 Axelar Network
   - License Terms: See https://github.com/axelarnetwork/axelarjs-sdk/blob/main/LICENSE

The HYBRID Blockchain itself is licensed under the MIT License with NFT Clause. See the LICENSE file for details.

For any questions or to report issues regarding these dependencies, please contact the HYBRID Blockchain team at [contact@hybridchain.local].
```

### Implementation
1. **Create NOTICE File**:
   ```bash
   echo "[NOTICE File Content Above]" > NOTICE
   git add NOTICE
   git commit -m "Add NOTICE file for third-party dependencies"
   git push
   ```

2. **Update README**:
   Add to `README.md`:
   ```markdown
   ## Notices
   The HYBRID Blockchain uses third-party dependencies. See the [NOTICE](NOTICE) file for details and license terms.
   ```

3. **Notes**:
   - Verify the exact versions of dependencies in your `go.mod`, `package.json`, or `Cargo.toml` files and update the `NOTICE` file accordingly.
   - If additional dependencies (e.g., LangChain, Coinbase OnchainKit) are used, include them with their respective licenses (often MIT or Apache 2.0).

---

## 2. Script to Automate SPDX Identifier Addition

This script automatically adds the `SPDX-License-Identifier: MIT` tag to source files (Solidity, Rust, Go, JavaScript/TypeScript) in the HYBRID Blockchain repository, ensuring compliance with the MIT License with NFT Clause.

### Script: `add-spdx.sh`
```bash
#!/bin/bash

# Script to add SPDX-License-Identifier: MIT to source files
LICENSE_HEADER="// SPDX-License-Identifier: MIT"

# Directories to scan
DIRECTORIES=("contracts" "programs" "test" "cmd/hybridchaind")

# File extensions to process
EXTENSIONS=("*.sol" "*.rs" "*.go" "*.js" "*.ts")

# Function to add SPDX header if missing
add_spdx() {
  local file=$1
  local ext=$2

  # Check if file already has SPDX header
  if ! grep -q "SPDX-License-Identifier" "$file"; then
    case $ext in
      *.sol|*.rs|*.go|*.js|*.ts)
        echo "Adding SPDX header to $file"
        echo -e "$LICENSE_HEADER\n$(cat "$file")" > "$file.tmp" && mv "$file.tmp" "$file"
        ;;
    esac
  else
    echo "SPDX header already present in $file"
  fi
}

# Iterate through directories and extensions
for dir in "${DIRECTORIES[@]}"; do
  if [ -d "$dir" ]; then
    for ext in "${EXTENSIONS[@]}"; do
      find "$dir" -type f -name "$ext" | while read -r file; do
        add_spdx "$file" "$ext"
      done
    done
  else
    echo "Directory $dir does not exist, skipping..."
  fi
done

echo "SPDX identifier addition complete."
```

### Usage
1. **Save Script**:
   ```bash
   echo "[Script Content Above]" > add-spdx.sh
   chmod +x add-spdx.sh
   ```

2. **Run Script**:
   ```bash
   ./add-spdx.sh
   ```

3. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Add SPDX-License-Identifier: MIT to source files"
   git push
   ```

4. **Notes**:
   - Ensure the script runs in the root of the HYBRID Blockchain repository.
   - Adjust `DIRECTORIES` to match your repository structure (e.g., add `frontend` if applicable).
   - The script checks for existing SPDX headers to avoid duplicates.
   - Verify changes manually to ensure no unintended modifications.

---

## 3. MultiChainDAO Proposal for the License

This proposal submits the MIT License with NFT Clause to the HYBRID Blockchain’s MultiChainDAO for community approval, assuming a Cosmos SDK-based governance module (e.g., `gov`) and cross-chain voting capabilities.

### Proposal: `proposal.json`
```json
{
  "title": "Adopt MIT License with NFT Clause for HYBRID Blockchain",
  "description": "This proposal adopts the MIT License with NFT Clause for the HYBRID Blockchain codebase, ensuring open-source access while requiring NFT ownership for node operation (Storage and Validator Nodes). The license balances Web3’s open-source ethos with the economic model of NFT-based node licensing, fostering community contributions and network participation.",
  "changes": [
    {
      "subspace": "licensing",
      "key": "software_license",
      "value": "MIT License with NFT Clause"
    }
  ],
  "deposit": "1000000uhybrid"
}
```

### Submission Steps
1. **Create Proposal**:
   ```bash
   echo '[Proposal JSON Above]' > proposal.json
   ```

2. **Submit to MultiChainDAO**:
   ```bash
   hybridchaind tx gov submit-proposal param-change proposal.json \
     --from hybrid1q2w3e4r5t6y7u8i9o0p \
     --node http://localhost:26657 \
     --chain-id hybrid-mainnet \
     --yes
   ```

3. **Vote on Proposal**:
   - Community members vote:
     ```bash
     hybridchaind tx gov vote <proposal-id> yes \
       --from hybrid1q2w3e4r5t6y7u8i9o0p \
       --node http://localhost:26657 \
       --chain-id hybrid-mainnet \
       --yes
     ```

4. **Cross-Chain Voting**:
   - Assuming MultiChainDAO supports cross-chain governance (e.g., via Axelar), integrate EVM/Solana voting:
     ```javascript
     const Governance = new ethers.Contract(governanceAddress, GovernanceABI, provider.getSigner());
     await Governance.vote("hybrid_proposal_<id>", true); // Vote yes on Base
     ```

5. **Documentation**:
   - Announce on X:
     ```text
     The HYBRID Blockchain proposes adopting the MIT License with NFT Clause! Vote on MultiChainDAO to shape our open-source future. Details: [link to proposal] #HYBRID #Web3
     ```
   - Update `README.md` post-approval:
     ```markdown
     ## Governance
     The MIT License with NFT Clause was approved via MultiChainDAO proposal #<id> on [date].
     ```

6. **Notes**:
   - Replace `<proposal-id>` with the actual ID after submission.
   - Ensure sufficient $HYBRID for the deposit (1,000,000 uhybrid).
   - If MultiChainDAO isn’t implemented, use an off-chain governance platform (e.g., Snapshot) with a similar proposal structure.

---

## 4. Expand on Node-as-a-Service (NaaS) Integration

NaaS allows users to delegate their HYBRID Node License NFTs to third-party providers who run Storage or Validator Nodes on their behalf, earning passive $HYBRID rewards. This section expands on NaaS integration, building on the HYBRID Blockchain’s NFT-based node model ().

### NaaS Architecture
- **NFT Delegation**:
  - Users delegate their Node License NFTs to a NaaS provider via a smart contract or Cosmos SDK module, retaining ownership but granting operational rights.
  - Example: A user with a Storage Node NFT delegates to a provider running a high-availability node.
- **Reward Distribution**:
  - NaaS providers earn $HYBRID transaction fees and distribute a portion (e.g., 70%) to NFT owners, keeping a fee (e.g., 30%).
- **Cross-Chain Support**:
  - NFTs may be deployed on Base or HybridChain, with Axelar/Wormhole enabling cross-chain delegation.
- **Security**:
  - NFT contracts use OpenZeppelin’s `ERC721` with access control (e.g., `Ownable`) to ensure secure delegation.
  - Node software verifies delegated NFTs before operation.

### Implementation
1. **NFT Delegation Contract (Base)**:
   ```solidity
   // SPDX-License-Identifier: MIT
   pragma solidity ^0.8.20;
   import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
   import "@openzeppelin/contracts/access/Ownable.sol";

   contract HybridNodeLicense is ERC721, Ownable {
       mapping(uint256 => address) public delegatedOperators;

       constructor() ERC721("HybridNodeLicense", "HNL") Ownable() {}

       function mint(address to, uint256 tokenId) external onlyOwner {
           _mint(to, tokenId);
       }

       function delegate(uint256 tokenId, address operator) external {
           require(ownerOf(tokenId) == msg.sender, "Not NFT owner");
           delegatedOperators[tokenId] = operator;
           emit Delegated(tokenId, operator);
       }

       function verifyDelegation(uint256 tokenId, address operator) external view returns (bool) {
           return delegatedOperators[tokenId] == operator;
       }

       event Delegated(uint256 tokenId, address operator);
   }
   ```

2. **Cosmos SDK Module for NaaS**:
   - Create a `naas` module to handle delegation and rewards:
     ```go
     // SPDX-License-Identifier: MIT
     package naas

     import (
         "github.com/cosmos/cosmos-sdk/types"
         "github.com/hybridchain/x/nft"
     )

     type Keeper struct {
         nftKeeper nft.Keeper
     }

     func (k Keeper) DelegateNFT(ctx types.Context, nftID string, owner, operator types.AccAddress) error {
         if !k.nftKeeper.IsOwner(ctx, owner, nftID) {
             return errors.New("not NFT owner")
         }
         k.nftKeeper.SetOperator(ctx, nftID, operator)
         return nil
     }

     func (k Keeper) DistributeRewards(ctx types.Context, nftID string, amount types.Int) error {
         owner := k.nftKeeper.GetOwner(ctx, nftID)
         operator := k.nftKeeper.GetOperator(ctx, nftID)
         ownerShare := amount.MulInt64(70).QuoInt64(100) // 70% to owner
         operatorShare := amount.Sub(ownerShare)         // 30% to operator
         // Send $HYBRID to owner and operator
         return nil
     }
     ```

3. **Node Software Integration**:
   - Update `hybridchaind` to check delegated NFTs:
     ```go
     // SPDX-License-Identifier: MIT
     package main
     import (
         "github.com/hybridchain/x/nft"
         "github.com/hybridchain/x/naas"
         "github.com/cosmos/cosmos-sdk/server"
     )
     func main() {
         ctx := server.Context()
         if !nft.IsOwner(ctx.FromAddress, "node_license_1") && !naas.IsOperator(ctx.FromAddress, "node_license_1") {
             panic("Invalid Node License NFT or delegation")
         }
         // Start node
     }
     ```

4. **NaaS Provider Setup**:
   - **Hardware**: High-availability servers (16-core CPU, 32GB RAM, 1TB SSD).
   - **Software**: Run multiple `hybridchaind` instances, each tied to a delegated NFT.
   - **API**: Expose a REST API for users to delegate NFTs and monitor rewards:
     ```bash
     curl -X POST https://naas.hybridchain.local/delegate \
       -d '{"nft_id":"node_license_1","operator":"hybrid1naasprovider"}'
     ```

5. **Cross-Chain NaaS**:
   - Use Axelar to bridge NFTs or $HYBRID rewards between HybridChain and Base:
     ```javascript
     const Axelar = new ethers.Contract(axelarGateway, AxelarABI, provider.getSigner());
     await Axelar.sendNFT("hybridchain", "base", nftContract.address, 1);
     ```

6. **User Flow**:
   - User purchases NFT (e.g., via cross-chain payment workflow).
   - User delegates NFT to NaaS provider via frontend:
     ```typescript
     const delegateNFT = async (tokenId: number, operator: string) => {
       const contract = new ethers.Contract(nftContractAddress, HybridNodeLicenseABI, signer);
       await contract.delegate(tokenId, operator);
     };
     ```
   - Provider runs node, distributes 70% of $HYBRID rewards to user monthly.

7. **Economic Model**:
   - **Cost**: Assume NFT costs 100 $HYBRID (~$1000 at $10/token).
   - **Rewards**: Storage Nodes earn ~0.5 $HYBRID/day; user gets 70% (~$1050/year at $10/token), yielding ~5% ROI.
   - **Provider Fee**: 30% of rewards covers infrastructure costs.

8. **Security**:
   - Use multisig wallets for NaaS provider operations.
   - Audit NFT and NaaS contracts with Mythril/Slither.
   - Implement slashing for malicious operators (e.g., via Cosmos SDK governance).

### Benefits
- **Accessibility**: Users without technical expertise can participate in node operations.
- **Scalability**: Providers run multiple nodes, increasing network decentralization.
- **Passive Income**: NFT owners earn $HYBRID without managing infrastructure.

---

## Consolidated Next Steps
1. **License**:
   - Add `LICENSE` and `NOTICE` files to the repository.
   - Run `add-spdx.sh` to add SPDX identifiers.
   - Submit MultiChainDAO proposal and announce on X.
2. **NaaS**:
   - Deploy `HybridNodeLicense` contract and `naas` module.
   - Partner with cloud providers (e.g., DigitalOcean) for NaaS infrastructure.
   - Develop a frontend for NFT delegation and reward tracking.
3. **Testing and Deployment**:
   - Test wallet interactions on testnets (Base Sepolia, Polygon Amoy, Solana Devnet, Hybrid Testnet).
   - Deploy Solana program and NFT contract.
   - Validate node setup with NFT verification.
4. **Community**:
   - Engage node operators via X and Discord.
   - Document NaaS setup in `README.md`.

---

## Directory Structure
```
hybridchain/
├── contracts/
│   ├── HybridNodeLicense.sol  # SPDX-License-Identifier: MIT
├── programs/
│   ├── hybrid/src/lib.rs      # SPDX-License-Identifier: MIT
├── test/
│   ├── hybridWalletInteractions.test.js  # SPDX-License-Identifier: MIT
├── cmd/hybridchaind/
│   ├── main.go                # SPDX-License-Identifier: MIT
├── x/naas/
│   ├── keeper.go              # SPDX-License-Identifier: MIT
├── LICENSE                    # MIT with NFT Clause
├── NOTICE                     # Dependency credits
├── README.md                  # License and NOTICE details
├── add-spdx.sh                # SPDX automation script
├── proposal.json              # MultiChainDAO proposal
```

---
