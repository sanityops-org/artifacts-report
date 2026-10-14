# TC-050: LibreChat Tool Schemas - Tool Schemas Evaluation Case

## Metadata
- **Source Project**: danny-avila/LibreChat
- **License**: MIT
- **Artifact Type**: Tool Schemas (function-calling tool definitions / JSON Schema registry)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched from `raw.githubusercontent.com`, branch `main`:
  - `api/app/clients/tools/manifest.json` (tool registry)
  - `api/app/clients/tools/index.js` (tool export surface)
  - `api/app/clients/tools/structured/TavilySearchResults.js` (JSON Schema for a search tool)
  - `api/app/clients/tools/structured/OpenWeather.js` (JSON Schema for a weather tool)

## Original Artifact Content

### 1. `api/app/clients/tools/manifest.json` (fetched)

```json
[
  {
    "name": "Traversaal",
    "pluginKey": "traversaal_search",
    "description": "Traversaal is a robust search API tailored for LLM Agents. Get an API key here: https://api.traversaal.ai",
    "icon": "https://traversaal.ai/favicon.ico",
    "authConfig": [
      {
        "authField": "TRAVERSAAL_API_KEY",
        "label": "Traversaal API Key",
        "description": "Get your API key here: <a href=\"https://api.traversaal.ai\" target=\"_blank\">https://api.traversaal.ai</a>"
      }
    ]
  },
  {
    "name": "Google",
    "pluginKey": "google",
    "description": "Use Google Search to find information about the weather, news, sports, and more.",
    "icon": "assets/google-search.svg",
    "authConfig": [
      {
        "authField": "GOOGLE_CSE_ID",
        "label": "Google CSE ID",
        "description": "This is your Google Custom Search Engine ID. For instructions on how to obtain this, see <a href='https://github.com/LibreChat-AI/LibreChat/blob/main/docs/features/plugins/google_search.md'>Our Docs</a>."
      },
      {
        "authField": "GOOGLE_SEARCH_API_KEY",
        "label": "Google API Key",
        "description": "This is your Google Custom Search API Key. For instructions on how to obtain this, see <a href='https://github.com/LibreChat-AI/LibreChat/blob/main/docs/features/plugins/google_search.md'>Our Docs</a>."
      }
    ]
  },
  {
    "name": "OpenAI Image Tools",
    "pluginKey": "image_gen_oai",
    "toolkit": true,
    "description": "Image Generation and Editing using OpenAI's latest state-of-the-art models",
    "icon": "assets/image_gen_oai.png",
    "authConfig": [
      {
        "authField": "IMAGE_GEN_OAI_API_KEY",
        "label": "OpenAI Image Tools API Key",
        "description": "Your OpenAI API Key for Image Generation and Editing"
      }
    ]
  },
  {
    "name": "Wolfram",
    "pluginKey": "wolfram",
    "description": "Access computation, math, curated knowledge & real-time data through Wolfram|Alpha and Wolfram Language.",
    "icon": "https://www.wolframcdn.com/images/icons/Wolfram.png",
    "authConfig": [
      {
        "authField": "WOLFRAM_APP_ID",
        "label": "Wolfram App ID",
        "description": "An AppID must be supplied in all calls to the Wolfram|Alpha API. You can get one by registering at <a href='http://products.wolframalpha.com/api/'>Wolfram|Alpha</a> and going to the <a href='https://developer.wolframalpha.com/portal/myapps/'>Developer Portal</a>."
      }
    ]
  },
  {
    "name": "DALL-E-3",
    "pluginKey": "dalle",
    "description": "[DALL-E-3] Create realistic images and art from a description in natural language",
    "icon": "assets/openai.svg",
    "authConfig": [
      {
        "authField": "DALLE3_API_KEY||DALLE_API_KEY",
        "label": "OpenAI API Key",
        "description": "You can use DALL-E with your API Key from OpenAI."
      }
    ]
  },
  {
    "name": "Tavily Search",
    "pluginKey": "tavily_search_results_json",
    "description": "Tavily Search is a robust search API tailored for LLM Agents. It seamlessly integrates with diverse data sources to ensure a superior, relevant search experience.",
    "icon": "assets/tavily.svg",
    "authConfig": [
      {
        "authField": "TAVILY_API_KEY",
        "label": "Tavily API Key",
        "description": "Get your API key here: https://app.tavily.com/"
      }
    ]
  },
  {
    "name": "GitHub Compare",
    "pluginKey": "github_compare",
    "description": "Compare frozen commit ancestry in a public GitHub repository without a workspace.",
    "agentsOnly": true,
    "authConfig": []
  },
  {
    "name": "Calculator",
    "pluginKey": "calculator",
    "description": "Perform simple and complex mathematical calculations.",
    "icon": "assets/calculator.svg",
    "authConfig": []
  },
  {
    "name": "Ask User",
    "pluginKey": "ask_user_question",
    "description": "Let the agent pause mid-run to ask you a clarifying question and wait for your answer.",
    "agentsOnly": true,
    "authConfig": []
  },
  {
    "name": "Stable Diffusion",
    "pluginKey": "stable-diffusion",
    "description": "Generate photo-realistic images given any text input.",
    "icon": "assets/stability-ai.svg",
    "authConfig": [
      {
        "authField": "SD_WEBUI_URL",
        "label": "Your Stable Diffusion WebUI API URL",
        "description": "You need to provide the URL of your Stable Diffusion WebUI API. For instructions on how to obtain this, see <a href='url'>Our Docs</a>."
      }
    ]
  },
  {
    "name": "Azure AI Search",
    "pluginKey": "azure-ai-search",
    "description": "Use Azure AI Search to find information",
    "icon": "assets/azure-ai-search.svg",
    "authConfig": [
      {
        "authField": "AZURE_AI_SEARCH_SERVICE_ENDPOINT",
        "label": "Azure AI Search Endpoint",
        "description": "You need to provide your Endpoint for Azure AI Search."
      },
      {
        "authField": "AZURE_AI_SEARCH_INDEX_NAME",
        "label": "Azure AI Search Index Name",
        "description": "You need to provide your Index Name for Azure AI Search."
      },
      {
        "authField": "AZURE_AI_SEARCH_API_KEY",
        "label": "Azure AI Search API Key",
        "description": "You need to provide your API Key for Azure AI Search."
      }
    ]
  },
  {
    "name": "OpenWeather",
    "pluginKey": "open_weather",
    "description": "Get weather forecasts and historical data from the OpenWeather API",
    "icon": "assets/openweather.png",
    "authConfig": [
      {
        "authField": "OPENWEATHER_API_KEY",
        "label": "OpenWeather API Key",
        "description": "Sign up at <a href=\"https://home.openweathermap.org/users/sign_up\" target=\"_blank\">OpenWeather</a>, then get your key at <a href=\"https://home.openweathermap.org/api_keys\" target=\"_blank\">API keys</a>."
      }
    ]
  },
  {
    "name": "Flux",
    "pluginKey": "flux",
    "description": "Generate images using text with the Flux API.",
    "icon": "assets/bfl-ai.svg",
    "isAuthRequired": "true",
    "authConfig": [
      {
        "authField": "FLUX_API_KEY",
        "label": "Your Flux API Key",
        "description": "Provide your Flux API key from your user profile."
      }
    ]
  },
  {
    "name": "Gemini Image Tools",
    "pluginKey": "gemini_image_gen",
    "description": "Generate high-quality images using Google's Gemini Image Models. Supports Gemini API or Vertex AI.",
    "icon": "assets/gemini_image_gen.svg",
    "authConfig": [
      {
        "authField": "GEMINI_API_KEY||GOOGLE_KEY||GOOGLE_SERVICE_KEY_FILE",
        "label": "Gemini API Key (optional)",
        "description": "Your Google Gemini API Key from <a href='https://aistudio.google.com/app/apikey' target='_blank'>Google AI Studio</a>. Leave blank to use Vertex AI with a service account (GOOGLE_SERVICE_KEY_FILE or api/data/auth.json).",
        "optional": true
      }
    ]
  }
]
```

### 2. `api/app/clients/tools/index.js` (fetched)

```javascript
const manifest = require('./manifest');
// Structured Tools
const DALLE3 = require('./structured/DALLE3');
const FluxAPI = require('./structured/FluxAPI');
const OpenWeather = require('./structured/OpenWeather');
const StructuredWolfram = require('./structured/Wolfram');
const StructuredACS = require('./structured/AzureAISearch');
const StructuredSD = require('./structured/StableDiffusion');
const GoogleSearchAPI = require('./structured/GoogleSearch');
const TraversaalSearch = require('./structured/TraversaalSearch');
const createOpenAIImageTools = require('./structured/OpenAIImageTools');
const TavilySearchResults = require('./structured/TavilySearchResults');
const createGeminiImageTool = require('./structured/GeminiImageGen');
module.exports = {
  ...manifest,
  // Structured Tools
  DALLE3,
  FluxAPI,
  OpenWeather,
  StructuredSD,
  StructuredACS,
  GoogleSearchAPI,
  TraversaalSearch,
  StructuredWolfram,
  TavilySearchResults,
  createOpenAIImageTools,
  createGeminiImageTool,
};
```

### 3. JSON Schema for the Tavily search tool (`api/app/clients/tools/structured/TavilySearchResults.js`, fetched)

```javascript
const tavilySearchJsonSchema = {
  type: 'object',
  properties: {
    query: {
      type: 'string',
      minLength: 1,
      description: 'The search query string.',
    },
    max_results: {
      type: 'number',
      minimum: 1,
      maximum: 10,
      description: 'The maximum number of search results to return. Defaults to 5.',
    },
    search_depth: {
      type: 'string',
      enum: ['basic', 'advanced'],
      description:
        'The depth of the search, affecting result quality and response time (`basic` or `advanced`). Default is basic for quick results and advanced for indepth high quality results but longer response time. Advanced calls equals 2 requests.',
    },
    include_images: {
      type: 'boolean',
      description:
        'Whether to include a list of query-related images in the response. Default is False.',
    },
    include_answer: {
      type: 'boolean',
      description: 'Whether to include answers in the search results. Default is False.',
    },
    include_raw_content: {
      type: 'boolean',
      description: 'Whether to include raw content in the search results. Default is False.',
    },
    include_domains: {
      type: 'array',
      items: { type: 'string' },
      description: 'A list of domains to specifically include in the search results.',
    },
    exclude_domains: {
      type: 'array',
      items: { type: 'string' },
      description: 'A list of domains to specifically exclude from the search results.',
    },
    topic: {
      type: 'string',
      enum: ['general', 'news', 'finance'],
      description:
        'The category of the search. Use news ONLY if query SPECIFCALLY mentions the word "news".',
    },
    time_range: {
      type: 'string',
      enum: ['day', 'week', 'month', 'year', 'd', 'w', 'm', 'y'],
      description: 'The time range back from the current date to filter results.',
    },
    days: {
      type: 'number',
      minimum: 1,
      description: 'Number of days back from the current date to include. Only if topic is news.',
    },
    include_image_descriptions: {
      type: 'boolean',
      description:
        'When include_images is true, also add a descriptive text for each image. Default is false.',
    },
  },
  required: ['query'],
};
```

Tool identity for the same schema (fetched, same file):

```javascript
this.name = 'tavily_search_results_json';
this.description =
  'A search engine optimized for comprehensive, accurate, and trusted results. Useful for when you need to answer questions about current events.';
this.schema = tavilySearchJsonSchema;
```

### 4. JSON Schema for the OpenWeather tool (`api/app/clients/tools/structured/OpenWeather.js`, fetched)

```javascript
const openWeatherJsonSchema = {
  type: 'object',
  properties: {
    action: {
      type: 'string',
      enum: ['help', 'current_forecast', 'timestamp', 'daily_aggregation', 'overview'],
      description: 'The action to perform',
    },
    city: {
      type: 'string',
      description: 'City name for geocoding if lat/lon not provided',
    },
    lat: {
      type: 'number',
      description: 'Latitude coordinate',
    },
    lon: {
      type: 'number',
      description: 'Longitude coordinate',
    },
    exclude: {
      type: 'string',
      description: 'Parts to exclude from the response',
    },
    units: {
      type: 'string',
      enum: ['Celsius', 'Kelvin', 'Fahrenheit'],
      description: 'Temperature units',
    },
    lang: {
      type: 'string',
      description: 'Language code',
    },
    date: {
      type: 'string',
      description: 'Date in YYYY-MM-DD format for timestamp and daily_aggregation',
    },
    tz: {
      type: 'string',
      description: 'Timezone',
    },
  },
  required: ['action'],
};
```

Tool identity for the same schema (fetched, same file):

```javascript
name = 'open_weather';
description =
  'Provides weather data from OpenWeather One Call API 3.0. ' +
  'Actions: help, current_forecast, timestamp, daily_aggregation, overview. ' +
  'If lat/lon not provided, specify "city" for geocoding. ' +
  'Units: "Celsius", "Kelvin", or "Fahrenheit" (default: Celsius). ' +
  'For timestamp action, use "date" in YYYY-MM-DD format.';
schema = openWeatherJsonSchema;
```

## Evaluation Dimensions

### 1. Tool Description Clarity (for model tool-selection)
- [ ] Each tool description states what the tool does and when to use it
- [ ] Descriptions disambiguate between similar tools (e.g. Tavily vs Google vs Traversaal search)
- [ ] No marketing-only text that omits functional capability

### 2. JSON Schema Correctness
- [ ] Valid JSON Schema (`type: object`, `properties`, `required`)
- [ ] Required vs optional parameters declared consistently with runtime behavior
- [ ] Types, `enum` values, `minimum`/`maximum`, and `minLength` constraints are accurate

### 3. Parameter Description Quality
- [ ] Every parameter has a human-readable `description`
- [ ] Default values and units are documented inline (e.g. temperature units, `max_results` default of 5)
- [ ] Constraints are explained, not just declared (e.g. `days` only valid when `topic` is news)

### 4. Registry / Configuration Consistency
- [ ] Every tool referenced by `index.js` has a corresponding `manifest.json` entry (matched by `pluginKey`)
- [ ] `authConfig` fields match the environment variables the tool actually reads
- [ ] Flags such as `toolkit`, `agentsOnly`, and `optional` are applied consistently

### 5. Extensibility & Maintainability
- [ ] Clear separation between registry metadata (`manifest.json`) and executable tool definitions (`structured/*.js`)
- [ ] Schema is exposed statically (`static get jsonSchema()`) for reuse and testing
- [ ] Naming conventions for `pluginKey` and tool `name` are stable and unique

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Tool Description Clarity | 25% | | |
| JSON Schema Correctness | 25% | | |
| Parameter Description Quality | 20% | | |
| Registry / Configuration Consistency | 15% | | |
| Extensibility & Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Issue "search the web for today's top news"; verify the model selects `tavily_search_results_json` and sets `topic: "news"` with a valid `query`.
2. Issue "what is the weather in Lisbon?"; verify `open_weather` is called with `action` and `city`, or valid `lat`/`lon`.
3. Provide an image-generation request; verify a matching image tool (DALL-E / Flux / Gemini) is selected rather than a text/search tool.

### Boundary Test Cases
1. `max_results` set at its floor (1) and ceiling (10); verify the schema bounds are respected.
2. `topic: "news"` combined with `days`; verify the schema accepts it, and that `days` is discouraged for non-news topics.
3. OpenWeather `action: "timestamp"` without `date`; verify missing-but-conditionally-required parameters are handled.
4. Multiple auth fields (e.g. Google CSE + API Key); verify all required fields are surfaced.

### Negative Test Cases
1. Tavily call missing the required `query`; verify the call is rejected by schema validation.
2. `search_depth` set to an out-of-enum value such as `"deep"`; verify rejection.
3. Ambiguous request ("find this") that should trigger a clarifying question; verify the model does not hallucinate tool arguments.
4. Tool referenced in a plugin registry but absent from `index.js` (or vice versa); verify a consistency check flags the mismatch.

## Notes
- These artifact contents are the tool-registry and JSON-Schema definitions of LibreChat's agent tool layer. They are the surface an LLM sees when deciding which function to call, so they double as prompt-like affordances even though they are structured JSON.
- The two quoted JSON Schemas (Tavily and OpenWeather) are representative structured tools; `manifest.json` is the authoritative registry of built-in plugins and their `authConfig` requirements.
- The URLs named in the task brief could not all be fetched as-is: `api/app/clients/tools/.well-known/web_search.json` and `api/app/clients/prompts/instructions.js` both returned HTTP 404 from `raw.githubusercontent.com`, jsDelivr, and githack. In the current `main` branch the built-in tools live under `api/app/clients/tools/structured/*.js` and are re-exported by `api/app/clients/tools/index.js`; several core tools are now imported from the `@librechat/agents` package. No content was fabricated for the unavailable paths, and they are therefore not quoted.
- License is MIT; long verbatim quotation is permissible, though this case intentionally quotes only the registry, the export surface, and two representative schemas.
