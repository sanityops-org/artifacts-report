# TC-200: mcp-crypto-price (truss44) - Tool Schema Evaluation Case

## Metadata
- **Source Project**: truss44/mcp-crypto-price (MCP server for cryptocurrency price/market data via CoinCap)
- **License**: MIT (Copyright (c) 2025 Tracey Russell)
- **Artifact Type**: Tool Schema (MCP tool definition for the `price-get` / "Get Crypto Price" tool)
- **Collection Date**: 2026-10-13
- **Collection Method**: Downloaded verbatim from `raw.githubusercontent.com`, branch `main`:
  - `src/tools/price.ts` — the Zod `GetPriceArgumentsSchema` (input) and `PriceOutputSchema` (output) and the `handleGetPrice` implementation
  - `src/index.ts` — the `server.registerTool('price-get', {...})` registration (tool name, title, description, annotations)
  - `LICENSE` — confirmed MIT

## Original Artifact Content

### Input and output schemas (`src/tools/price.ts`, fetched verbatim)

```typescript
import { z } from 'zod';

export const GetPriceArgumentsSchema = z.object({
  symbol: z
    .string()
    .min(1)
    .describe('Cryptocurrency symbol or name (e.g. BTC or Bitcoin)'),
});

export const PriceOutputSchema = z.object({
  name: z.string(),
  symbol: z.string(),
  priceUsd: z.string(),
  changePercent24Hr: z.string().nullable(),
  volumeUsd24Hr: z.string().nullable(),
  marketCapUsd: z.string().nullable(),
  rank: z.string().nullable(),
});
```

### Tool registration (`src/index.ts`, fetched verbatim)

```typescript
  server.registerTool(
    'price-get',
    {
      title: 'Get Crypto Price',
      description:
        'Get real-time price, 24-hour change percentage, trading volume, and market cap for any cryptocurrency by symbol or name.',
      inputSchema: GetPriceArgumentsSchema.shape,
      outputSchema: PriceOutputSchema.shape,
      annotations: {
        title: 'Get Crypto Price',
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true,
      },
    },
    async (args, _extra) => {
      const result = await handleGetPrice(args);
      return result as unknown as CallToolResult;
    }
  );
```

## Evaluation Dimensions

### 1. Schema Completeness
- [ ] The tool exposes a concrete Zod `inputSchema` (`GetPriceArgumentsSchema`)
- [ ] The single parameter is typed and constrained (`z.string().min(1)`)
- [ ] Required vs optional is explicit (`symbol` is required — no `.optional()`)
- [ ] An `outputSchema` is declared, documenting the structured response

### 2. Description Clarity
- [ ] The tool description states the capability and the returned fields ("real-time price, 24-hour change percentage, trading volume, and market cap")
- [ ] The parameter has a `.describe(...)` string with examples (`BTC or Bitcoin`)
- [ ] Scope is bounded ("by symbol or name")

### 3. Integration Compatibility
- [ ] Registered via `McpServer.registerTool(...)` with `inputSchema`/`outputSchema` taken from Zod `.shape`
- [ ] Annotations are standards-compliant (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`)
- [ ] Returns both a text `content` block and `structuredContent` matching the output schema

### 4. Example Quality
- [ ] The `symbol` description embeds concrete examples (`BTC`, `Bitcoin`)
- [ ] The output schema names each returned field explicitly
- [ ] Missing-asset and error cases return an explicit message rather than an empty payload

### 5. Extensibility
- [ ] Tools are one module each under `src/tools/` and re-exported from `src/tools/index.ts`
- [ ] The CoinCap API key is optional and read from the environment (`COINCAP_API_KEY`), keeping the schema credential-free
- [ ] `inputSchema` and `outputSchema` share a single source of truth (the Zod schemas), avoiding drift

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
1. Issue "what's the price of Bitcoin?"; verify `price-get` is called with `symbol: "Bitcoin"` (or `BTC`).
2. Issue "get the current ETH price and market cap"; verify `symbol: "ETH"` and that `priceUsd`/`marketCapUsd` are returned per the output schema.
3. Issue "how much has Solana changed in 24 hours?"; verify `symbol: "SOL"` and the `changePercent24Hr` field is surfaced.

### Boundary Test Cases
1. A lowercase symbol (e.g. `"btc"`); verify the handler uppercases it and still resolves.
2. A symbol with surrounding whitespace; verify resolution behavior.
3. A nullable output field (e.g. `rank` absent); verify `null` is handled rather than crashing.
4. A very new/illiquid asset where `volumeUsd24Hr` may be null; verify the output schema's `.nullable()` is respected.

### Negative Test Cases
1. An empty `symbol` string; verify the `.min(1)` constraint rejects it.
2. `price-get` without `symbol`; verify validation rejects the call.
3. `symbol` provided as a number; verify type validation rejects it.
4. An unknown ticker (e.g. `"NOTACOIN"`); verify the documented "Could not find cryptocurrency with symbol ..." path.

## Notes
- This is one logical artifact: the `price-get` tool (registration title "Get Crypto Price"). The server also exposes market, historical, top-assets, technical-analysis, rates, exchanges, search, global-metrics, compare, candlestick, price-conversion, and asset-info tools.
- The `inputSchema`/`outputSchema` are authored in Zod and passed to the SDK as `.shape`; the verbatim Zod source and registration are quoted and labeled as the schema source, per the rule for generated schemas.
- The tool name (`price-get`) and the human title ("Get Crypto Price") differ; the model sees the registered name, which is a naming-consistency discussion point.
- License is MIT; verbatim quotation is permissible.
