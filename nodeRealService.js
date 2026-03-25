/**
 * Minimal JSON-RPC helper for BNB Smart Chain block tracking.
 *
 * NodeReal RPC URL can be provided directly via env var:
 * - NODE_REAL_BSC_RPC_URL
 *
 * Or, provide a NodeReal API key and let this module build the default RPC URL:
 * - NODE_REAL_BSC_API_KEY (preferred)
 * - NODE_REAL_API_KEY (fallback)
 *
 * NodeReal default mainnet format:
 * https://bsc-mainnet.nodereal.io/v1/{apiKey}
 */

async function fetchJsonRpc(rpcUrl, payload) {
  if (!rpcUrl) {
    throw new Error(
      "Missing RPC URL/API key. Set NODE_REAL_BSC_RPC_URL (or BSC_NODE_REAL_RPC_URL) OR set NODE_REAL_BSC_API_KEY (or NODE_REAL_API_KEY)."
    );
  }

  // Node 18+ should have global fetch; if not, user must polyfill.
  if (typeof fetch !== "function") {
    throw new Error(
      "Global fetch is not available. Use Node 18+ or add a fetch polyfill."
    );
  }

  const res = await fetch(rpcUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`RPC request failed: ${res.status} ${res.statusText} ${text}`.trim());
  }

  return res.json();
}

/**
 * Fetch latest BNB Smart Chain block number via JSON-RPC.
 * @param {string} [rpcUrl] Optional RPC URL override.
 * @returns {Promise<{ blockNumber: number, blockHex: string }>}
 */
async function getLatestBnbSmartChainBlockNumber(rpcUrl) {
  const apiKey =
    process.env.NODE_REAL_BSC_API_KEY || process.env.NODE_REAL_API_KEY;

  const url =
    rpcUrl ||
    process.env.NODE_REAL_BSC_RPC_URL ||
    process.env.BSC_NODE_REAL_RPC_URL ||
    (apiKey
      ? `https://bsc-mainnet.nodereal.io/v1/${encodeURIComponent(apiKey)}`
      : undefined);

  const payload = {
    jsonrpc: "2.0",
    id: 1,
    method: "eth_blockNumber",
    params: [],
  };

  const data = await fetchJsonRpc(url, payload);

  if (data?.error) {
    throw new Error(
      `RPC error: ${data.error.message || JSON.stringify(data.error)}`
    );
  }

  const blockHex = data?.result;
  if (typeof blockHex !== "string") {
    throw new Error(`Unexpected RPC response: ${JSON.stringify(data)}`);
  }

  return {
    blockNumber: (() => {
      const n = parseInt(blockHex, 16);
      if (!Number.isFinite(n)) {
        throw new Error(`Unexpected blockHex value: ${blockHex}`);
      }
      return n;
    })(),
    blockHex,
  };
}

module.exports = {
  getLatestBnbSmartChainBlockNumber,
};

