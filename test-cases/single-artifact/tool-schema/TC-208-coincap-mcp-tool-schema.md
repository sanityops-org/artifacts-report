# TC-208: CoinCap MCP Server - Tool Schema Evaluation Case

## Metadata
- **Source Project**: QuantGeekDev/coincap-mcp (MCP server for the CoinCap cryptocurrency price API)
- **License**: MIT (Copyright (c) 2024 Alex Andrushevich)
- **Artifact Type**: Tool Schema (MCP tool definitions for `get_crypto_price` and `list_assets`)
- **Collection Date**: 2026-10-14
- **Collection Method**: Fetched verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/GetCryptoPrice.ts` — the `get_crypto_price` tool definition and handler
  - `src/tools/ListAssets.ts` — the `list_assets` tool definition and handler
  - `src/tools/BaseTool.ts` — the shared `BaseTool` interface / abstract base
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Tool definition and handler (`src/tools/GetCryptoPrice.ts`, fetched verbatim)

```typescript
import { Tool } from "@modelcontextprotocol/sdk/types.js";
import { CONSTANTS } from "../constants.js";
import { z } from "zod";
import { CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { BaseToolImplementation } from "./BaseTool.js";

class GetCryptoPrice extends BaseToolImplementation {
  name = "get_crypto_price";
  toolDefinition: Tool = {
    name: this.name,
    description: "Get realtime crypto price on crypto",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: "Name of the crypto coin",
        },
      },
    },
  };

  async toolCall(request: z.infer<typeof CallToolRequestSchema>) {
    try {
      const cryptoName = request.params.arguments?.name;
      if (!cryptoName) {
        throw new Error("Missing crypto name");
      }
      const url = CONSTANTS.CRYPTO_PRICE_URL + cryptoName;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Error fetching coincap data");
      }
      const body = await response.json();
      return {
        content: [{ type: "text", text: JSON.stringify(body.data) }],
      };
    } catch (error) {
      return {
        content: [
          { type: "error", text: JSON.stringify((error as any).message) },
        ],
      };
    }
  }
}

export default GetCryptoPrice;
```

### Companion tool (`src/tools/ListAssets.ts`, fetched verbatim)

```typescript
import { Tool } from "@modelcontextprotocol/sdk/types.js";
import { CONSTANTS } from "../constants.js";
import { BaseToolImplementation } from "./BaseTool.js";

class ListAssetsTool extends BaseToolImplementation {
  name = "list_assets";
  toolDefinition: Tool = {
    name: this.name,
    description: "Get all available crypto assets",
    inputSchema: {
      type: "object",
    },
  };

  toolCall = async () => {
    try {
      const url = CONSTANTS.CRYPTO_PRICE_URL;
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error("Error fetching coincap data");
      }
      const body = await response.json();
      return {
        content: [{ type: "text", text: JSON.stringify(body.data) }],
      };
    } catch (error) {
      return {
        content: [
          { type: "error", text: JSON.stringify((error as any).message) },
        ],
      };
    }
  };
}

export default ListAssetsTool;
```

### Shared tool base (`src/tools/BaseTool.ts`, fetched verbatim)

```typescript
import {
  CallToolRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

export interface BaseTool {
  name: string;
  toolDefinition: Tool;
  toolCall(request: z.infer<typeof CallToolRequestSchema>): Promise<any>;
}

export abstract class BaseToolImplementation implements BaseTool {
  abstract name: string;
  abstract toolDefinition: Tool;
  abstract toolCall(
    request: z.infer<typeof CallToolRequestSchema>
  ): Promise<any>;
}
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] Each tool exposes a concrete JSON Schema `inputSchema` (`type: "object"` with a `properties` map, or an empty object)
- [ ] Parameter types are declared (`name: string`)
- [ ] Required vs optional is clear (`get_crypto_price` has one property with no `required` array; `list_assets` takes no parameters)
- [ ] Enum/identifier guidance is provided (the handler documents that a CoinCap asset name/identifier is required)

### 2. Description Clarity
- [ ] Each tool states what it does ("Get realtime crypto price on crypto", "Get all available crypto assets")
- [ ] The parameter carries a human-readable `description` ("Name of the crypto coin")
- [ ] The two tools are distinguishable (a single-asset lookup vs a full asset listing)

### 3. Integration Compatibility
- [ ] Conforms to the MCP tool model via `@modelcontextprotocol/sdk` `Tool` types
- [ ] Each tool implements a uniform `BaseTool` interface (`name`, `toolDefinition`, `toolCall`)
- [ ] JSON Schema `inputSchema` is hand-written and directly consumable by MCP clients and function-calling LLMs

### 4. Example Quality
- [ ] The description is terse but functional
- [ ] The handler surfaces a specific error when required input is missing ("Missing crypto name")
- [ ] No input example is embedded (a minor quality gap worth scoring)

### 5. Extensibility
- [ ] `BaseTool` / `BaseToolImplementation` define a single contract that every tool follows
- [ ] Tools are isolated in per-file classes (`GetCryptoPrice.ts`, `ListAssets.ts`, `BitcoinPrice.ts`), loaded by a `utils/toolLoader.ts`
- [ ] Shared constants (`CONSTANTS.CRYPTO_PRICE_URL`) centralize the upstream endpoint

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Schema Completeness | 25% | | |
| Description Clarity | 20% | | |
| Integration Compatibility | 25% | | |
| Example Quality | 20% | | |
| Extensibility | 10% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "what is the current price of Bitcoin?"; verify `get_crypto_price` is called with `name: "bitcoin"`.
2. Issue "list all the cryptocurrencies you support"; verify `list_assets` is selected (no parameters).
3. Issue "how much is Ethereum worth right now?"; verify `get_crypto_price` with `name: "ethereum"`.

### Boundary Test Cases
1. `get_crypto_price` with an asset name in a different case (e.g. `"BITCOIN"`); verify whether the upstream API or handler normalizes it (observe behaviour).
2. `get_crypto_price` with an asset identifier form (e.g. a symbol) versus a full name; observe which form the API accepts.
3. `list_assets` (no parameters); verify an empty `inputSchema` object is accepted without an arguments payload.
4. A multi-asset question ("compare BTC, ETH and SOL"); verify the model issues several `get_crypto_price` calls rather than one unsupported batch call.

### Negative Test Cases
1. `get_crypto_price` with no `name`; verify the handler throws and returns "Missing crypto name".
2. `get_crypto_price` with an unknown coin; verify the upstream error is surfaced rather than a fabricated price.
3. A request to buy/sell a crypto asset; verify no trading capability is exposed (the tools are read-only price queries).
4. `name` passed as a number; verify type validation rejects it.

## Notes
- This case quotes the `get_crypto_price` and `list_assets` tool definitions verbatim from `src/tools/GetCryptoPrice.ts` and `src/tools/ListAssets.ts`, plus the shared `BaseTool` contract from `src/tools/BaseTool.ts`. `get_crypto_price` is the representative focus; `list_assets` is quoted because it demonstrates the no-parameter schema case in the same registry.
- Schemas are hand-written JSON Schema objects returned as `toolDefinition`; there is no Zod-to-JSON-Schema generation for the input schema (Zod is used only for the `CallToolRequestSchema` request type). What is quoted is exactly the surface the LLM receives.
- License is MIT; verbatim quotation is permissible.
