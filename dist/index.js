// server/index.ts
import express2 from "express";

// server/routes.ts
import { createServer } from "http";
import { WebSocketServer as WebSocketServer2 } from "ws";

// server/services/blockchainService.ts
var BlockchainService = class {
  networkStatus = {
    blockHeight: 2847693,
    tps: 1247,
    validators: 125,
    peers: 847,
    chainId: "hybridchain-1",
    version: "v1.0.0",
    gasPrice: "0.025 HYBRID",
    memory: "68%",
    blockTime: "6.2s"
  };
  auditEvents = [
    {
      id: "1",
      type: "INCOMING",
      sourceChain: "Polygon",
      targetChain: "HybridChain",
      txHash: "0x7a3f...d8b2",
      amount: "150.5 MATIC",
      sender: "0x1234...5678",
      recipient: "0x8765...4321",
      timestamp: "2m ago",
      status: "CONFIRMED"
    },
    {
      id: "2",
      type: "OUTGOING",
      sourceChain: "HybridChain",
      targetChain: "Solana",
      txHash: "5GjR...nK8M",
      amount: "89.2 SOL",
      sender: "0x8765...4321",
      recipient: "DsVm...Qx3k",
      timestamp: "15s ago",
      status: "PENDING"
    }
  ];
  bridgeStatus = {
    ibc: {
      active: 24,
      pending: 3,
      volume: "$2.4M"
    },
    wormhole: {
      vaas: 1847,
      guardians: "19/19",
      volume: "$847K"
    },
    axelar: {
      chains: 47,
      validators: 75,
      volume: "$12.7M"
    }
  };
  evmStatus = {
    contracts: 1847,
    gasPrice: "2.5 Gwei",
    callsPerSec: 342
  };
  shopStats = {
    products: 12847,
    merchants: 3421,
    volume: "$847K"
  };
  recentOrders = [
    {
      id: "#7849",
      amount: "$127.50",
      status: "CONFIRMED",
      timestamp: "5m ago"
    },
    {
      id: "#7848",
      amount: "$89.99",
      status: "PENDING",
      timestamp: "12m ago"
    }
  ];
  async getNetworkStatus() {
    this.networkStatus.blockHeight += Math.floor(Math.random() * 3) + 1;
    this.networkStatus.tps = 1247 + Math.floor(Math.random() * 200) - 100;
    return this.networkStatus;
  }
  async getAuditEvents() {
    return this.auditEvents;
  }
  async getAuditMetrics() {
    return {
      totalTransactions: 2847693,
      successfulTx: 2846446,
      failedTx: 1247,
      successRate: 99.96,
      chainBreakdown: {
        "POL": 1423847,
        "BASE": 894231,
        "SOL": 529615
      }
    };
  }
  async getBridgeStatus() {
    return this.bridgeStatus;
  }
  async getEVMStatus() {
    return this.evmStatus;
  }
  async getShopStats() {
    return this.shopStats;
  }
  async getRecentOrders() {
    return this.recentOrders;
  }
  async sendGreeting(name, targetChain) {
    const txHash = `0x${Math.random().toString(16).substring(2, 10)}...${Math.random().toString(16).substring(2, 6)}`;
    return {
      success: true,
      message: `Hello, ${name}! Welcome to HybridChain!`,
      txHash: targetChain ? txHash : void 0
    };
  }
  async deployContract(contractType) {
    const contractAddress = `0x${Math.random().toString(16).substring(2, 10)}...${Math.random().toString(16).substring(2, 6)}`;
    const txHash = `0x${Math.random().toString(16).substring(2, 10)}...${Math.random().toString(16).substring(2, 6)}`;
    return {
      success: true,
      contractAddress,
      txHash
    };
  }
  // Method to update data (called by WebSocket service)
  updateNetworkStatus(updates) {
    this.networkStatus = { ...this.networkStatus, ...updates };
  }
  addAuditEvent(event) {
    this.auditEvents.unshift(event);
    if (this.auditEvents.length > 10) {
      this.auditEvents.pop();
    }
  }
};
var blockchainService = new BlockchainService();

// server/services/websocketService.ts
import { WebSocket } from "ws";
function setupWebSocketService(wss) {
  const clients = /* @__PURE__ */ new Set();
  wss.on("connection", (ws) => {
    clients.add(ws);
    console.log("WebSocket client connected");
    ws.on("close", () => {
      clients.delete(ws);
      console.log("WebSocket client disconnected");
    });
    ws.on("error", (error) => {
      console.error("WebSocket error:", error);
      clients.delete(ws);
    });
    sendToClient(ws, {
      type: "NETWORK_UPDATE",
      data: blockchainService.getNetworkStatus()
    });
  });
  function broadcast(message) {
    const messageStr = JSON.stringify(message);
    clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(messageStr);
      }
    });
  }
  function sendToClient(client, message) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(message));
    }
  }
  setInterval(async () => {
    const networkStatus = await blockchainService.getNetworkStatus();
    broadcast({
      type: "NETWORK_UPDATE",
      data: networkStatus
    });
  }, 5e3);
  setInterval(() => {
    if (Math.random() > 0.7) {
      const mockEvent = {
        id: Date.now().toString(),
        type: Math.random() > 0.5 ? "INCOMING" : "OUTGOING",
        sourceChain: ["Polygon", "Base", "Solana"][Math.floor(Math.random() * 3)],
        targetChain: "HybridChain",
        txHash: `0x${Math.random().toString(16).substring(2, 10)}...${Math.random().toString(16).substring(2, 6)}`,
        amount: `${(Math.random() * 1e3).toFixed(2)} ETH`,
        sender: `0x${Math.random().toString(16).substring(2, 10)}...${Math.random().toString(16).substring(2, 6)}`,
        recipient: `0x${Math.random().toString(16).substring(2, 10)}...${Math.random().toString(16).substring(2, 6)}`,
        timestamp: "just now",
        status: Math.random() > 0.8 ? "PENDING" : "CONFIRMED"
      };
      blockchainService.addAuditEvent(mockEvent);
      broadcast({
        type: "AUDIT_EVENT",
        data: mockEvent
      });
    }
  }, 1e4);
}

// server/routes.ts
async function registerRoutes(app2) {
  const httpServer = createServer(app2);
  const wss = new WebSocketServer2({
    server: httpServer,
    path: "/ws"
  });
  setupWebSocketService(wss);
  app2.get("/api/blockchain/status", async (req, res) => {
    try {
      const status = await blockchainService.getNetworkStatus();
      res.json(status);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch blockchain status" });
    }
  });
  app2.get("/api/audit/events", async (req, res) => {
    try {
      const events = await blockchainService.getAuditEvents();
      res.json(events);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch audit events" });
    }
  });
  app2.get("/api/audit/metrics", async (req, res) => {
    try {
      const metrics = await blockchainService.getAuditMetrics();
      res.json(metrics);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch audit metrics" });
    }
  });
  app2.get("/api/bridge/status", async (req, res) => {
    try {
      const status = await blockchainService.getBridgeStatus();
      res.json(status);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch bridge status" });
    }
  });
  app2.get("/api/evm/status", async (req, res) => {
    try {
      const status = await blockchainService.getEVMStatus();
      res.json(status);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch EVM status" });
    }
  });
  app2.get("/api/shop/stats", async (req, res) => {
    try {
      const stats = await blockchainService.getShopStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch shop stats" });
    }
  });
  app2.get("/api/shop/orders", async (req, res) => {
    try {
      const orders = await blockchainService.getRecentOrders();
      res.json(orders);
    } catch (error) {
      res.status(500).json({ error: "Failed to fetch orders" });
    }
  });
  app2.post("/api/hello/greeting", async (req, res) => {
    try {
      const { name, targetChain } = req.body;
      const result = await blockchainService.sendGreeting(name, targetChain);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: "Failed to send greeting" });
    }
  });
  app2.post("/api/evm/deploy", async (req, res) => {
    try {
      const { contractType } = req.body;
      const result = await blockchainService.deployContract(contractType);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: "Failed to deploy contract" });
    }
  });
  return httpServer;
}

// server/vite.ts
import express from "express";
import fs from "fs";
import path2 from "path";
import { createServer as createViteServer, createLogger } from "vite";

// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import runtimeErrorOverlay from "@replit/vite-plugin-runtime-error-modal";
var vite_config_default = defineConfig({
  plugins: [
    react(),
    runtimeErrorOverlay(),
    ...process.env.NODE_ENV !== "production" && process.env.REPL_ID !== void 0 ? [
      await import("@replit/vite-plugin-cartographer").then(
        (m) => m.cartographer()
      )
    ] : []
  ],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
      "@shared": path.resolve(import.meta.dirname, "shared"),
      "@assets": path.resolve(import.meta.dirname, "attached_assets")
    }
  },
  root: path.resolve(import.meta.dirname, "client"),
  build: {
    outDir: path.resolve(import.meta.dirname, "dist/public"),
    emptyOutDir: true
  },
  server: {
    fs: {
      strict: true,
      deny: ["**/.*"]
    }
  }
});

// server/vite.ts
import { nanoid } from "nanoid";
var viteLogger = createLogger();
function log(message, source = "express") {
  const formattedTime = (/* @__PURE__ */ new Date()).toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
    hour12: true
  });
  console.log(`${formattedTime} [${source}] ${message}`);
}
async function setupVite(app2, server) {
  const serverOptions = {
    middlewareMode: true,
    hmr: { server },
    allowedHosts: true
  };
  const vite = await createViteServer({
    ...vite_config_default,
    configFile: false,
    customLogger: {
      ...viteLogger,
      error: (msg, options) => {
        viteLogger.error(msg, options);
        process.exit(1);
      }
    },
    server: serverOptions,
    appType: "custom"
  });
  app2.use(vite.middlewares);
  app2.use("*", async (req, res, next) => {
    const url = req.originalUrl;
    try {
      const clientTemplate = path2.resolve(
        import.meta.dirname,
        "..",
        "client",
        "index.html"
      );
      let template = await fs.promises.readFile(clientTemplate, "utf-8");
      template = template.replace(
        `src="/src/main.tsx"`,
        `src="/src/main.tsx?v=${nanoid()}"`
      );
      const page = await vite.transformIndexHtml(url, template);
      res.status(200).set({ "Content-Type": "text/html" }).end(page);
    } catch (e) {
      vite.ssrFixStacktrace(e);
      next(e);
    }
  });
}
function serveStatic(app2) {
  const distPath = path2.resolve(import.meta.dirname, "public");
  if (!fs.existsSync(distPath)) {
    throw new Error(
      `Could not find the build directory: ${distPath}, make sure to build the client first`
    );
  }
  app2.use(express.static(distPath));
  app2.use("*", (_req, res) => {
    res.sendFile(path2.resolve(distPath, "index.html"));
  });
}

// server/index.ts
var app = express2();
app.use(express2.json());
app.use(express2.urlencoded({ extended: false }));
app.use((req, res, next) => {
  const start = Date.now();
  const path3 = req.path;
  let capturedJsonResponse = void 0;
  const originalResJson = res.json;
  res.json = function(bodyJson, ...args) {
    capturedJsonResponse = bodyJson;
    return originalResJson.apply(res, [bodyJson, ...args]);
  };
  res.on("finish", () => {
    const duration = Date.now() - start;
    if (path3.startsWith("/api")) {
      let logLine = `${req.method} ${path3} ${res.statusCode} in ${duration}ms`;
      if (capturedJsonResponse) {
        logLine += ` :: ${JSON.stringify(capturedJsonResponse)}`;
      }
      if (logLine.length > 80) {
        logLine = logLine.slice(0, 79) + "\u2026";
      }
      log(logLine);
    }
  });
  next();
});
(async () => {
  const server = await registerRoutes(app);
  app.use((err, _req, res, _next) => {
    const status = err.status || err.statusCode || 500;
    const message = err.message || "Internal Server Error";
    res.status(status).json({ message });
    throw err;
  });
  if (app.get("env") === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }
  const port = 5e3;
  server.listen({
    port,
    host: "0.0.0.0",
    reusePort: true
  }, () => {
    log(`serving on port ${port}`);
  });
})();
