# TC-140: csv-data-summarizer-claude-skill - Skill Evaluation Case

## Metadata
- **Source Project**: coffeefuelbump/csv-data-summarizer-claude-skill
- **License**: MIT (see `LICENSE`; README states "MIT License - feel free to use this skill for personal or commercial projects")
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/coffeefuelbump/csv-data-summarizer-claude-skill/main/SKILL.md (branch: `main`). Repository README: https://raw.githubusercontent.com/coffeefuelbump/csv-data-summarizer-claude-skill/main/README.md

## Original Artifact Content

````markdown
---
name: csv-data-summarizer
description: Analyzes CSV files, generates summary stats, and plots quick visualizations using Python and pandas.
metadata:
  version: 2.1.0
  dependencies: python>=3.8, pandas>=2.0.0, matplotlib>=3.7.0, seaborn>=0.12.0
---

# CSV Data Summarizer

This Skill analyzes CSV files and provides comprehensive summaries with statistical insights and visualizations.

## When to Use This Skill

Claude should use this Skill whenever the user:
- Uploads or references a CSV file
- Asks to summarize, analyze, or visualize tabular data
- Requests insights from CSV data
- Wants to understand data structure and quality

## How It Works

## ⚠️ CRITICAL BEHAVIOR REQUIREMENT ⚠️

**DO NOT ASK THE USER WHAT THEY WANT TO DO WITH THE DATA.**
**DO NOT OFFER OPTIONS OR CHOICES.**
**DO NOT SAY "What would you like me to help you with?"**
**DO NOT LIST POSSIBLE ANALYSES.**

**IMMEDIATELY AND AUTOMATICALLY:**
1. Run the comprehensive analysis
2. Generate ALL relevant visualizations
3. Present complete results
4. NO questions, NO options, NO waiting for user input

**THE USER WANTS A FULL ANALYSIS RIGHT AWAY - JUST DO IT.**

### Automatic Analysis Steps:

**The skill intelligently adapts to different data types and industries by inspecting the data first, then determining what analyses are most relevant.**

1. **Load and inspect** the CSV file into pandas DataFrame
2. **Identify data structure** - column types, date columns, numeric columns, categories
3. **Determine relevant analyses** based on what's actually in the data:
 - **Sales/E-commerce data** (order dates, revenue, products): Time-series trends, revenue analysis, product performance
 - **Customer data** (demographics, segments, regions): Distribution analysis, segmentation, geographic patterns
 - **Financial data** (transactions, amounts, dates): Trend analysis, statistical summaries, correlations
 - **Operational data** (timestamps, metrics, status): Time-series, performance metrics, distributions
 - **Survey data** (categorical responses, ratings): Frequency analysis, cross-tabulations, distributions
 - **Generic tabular data**: Adapts based on column types found

4. **Only create visualizations that make sense** for the specific dataset:
 - Time-series plots ONLY if date/timestamp columns exist
 - Correlation heatmaps ONLY if multiple numeric columns exist
 - Category distributions ONLY if categorical columns exist
 - Histograms for numeric distributions when relevant

5. **Generate comprehensive output** automatically including:
 - Data overview (rows, columns, types)
 - Key statistics and metrics relevant to the data type
 - Missing data analysis
 - Multiple relevant visualizations (only those that apply)
 - Actionable insights based on patterns found in THIS specific dataset

6. **Present everything** in one complete analysis - no follow-up questions

**Example adaptations:**
- Healthcare data with patient IDs → Focus on demographics, treatment patterns, temporal trends
- Inventory data with stock levels → Focus on quantity distributions, reorder patterns, SKU analysis 
- Web analytics with timestamps → Focus on traffic patterns, conversion metrics, time-of-day analysis
- Survey responses → Focus on response distributions, demographic breakdowns, sentiment patterns

### Behavior Guidelines

✅ **CORRECT APPROACH - SAY THIS:**
- "I'll analyze this data comprehensively right now."
- "Here's the complete analysis with visualizations:"
- "I've identified this as [type] data and generated relevant insights:"
- Then IMMEDIATELY show the full analysis

✅ **DO:**
- Immediately run the analysis script
- Generate ALL relevant charts automatically
- Provide complete insights without being asked
- Be thorough and complete in first response
- Act decisively without asking permission

❌ **NEVER SAY THESE PHRASES:**
- "What would you like to do with this data?"
- "What would you like me to help you with?"
- "Here are some common options:"
- "Let me know what you'd like help with"
- "I can create a comprehensive analysis if you'd like!"
- Any sentence ending with "?" asking for user direction
- Any list of options or choices
- Any conditional "I can do X if you want"

❌ **FORBIDDEN BEHAVIORS:**
- Asking what the user wants
- Listing options for the user to choose from
- Waiting for user direction before analyzing
- Providing partial analysis that requires follow-up
- Describing what you COULD do instead of DOING it

### Usage

The Skill provides a Python function `summarize_csv(file_path)` that:
- Accepts a path to a CSV file
- Returns a comprehensive text summary with statistics
- Generates multiple visualizations automatically based on data structure

### Example Prompts

> "Here's `sales_data.csv`. Can you summarize this file?"

> "Analyze this customer data CSV and show me trends."

> "What insights can you find in `orders.csv`?"

### Example Output

**Dataset Overview**
- 5,000 rows × 8 columns 
- 3 numeric columns, 1 date column 

**Summary Statistics**
- Average order value: $58.2 
- Standard deviation: $12.4
- Missing values: 2% (100 cells)

**Insights**
- Sales show upward trend over time
- Peak activity in Q4
*(Attached: trend plot)*

## Files

- `analyze.py` - Core analysis logic
- `requirements.txt` - Python dependencies
- `resources/sample.csv` - Example dataset for testing
- `resources/README.md` - Additional documentation

## Notes

- Automatically detects date columns (columns containing 'date' in name)
- Handles missing data gracefully
- Generates visualizations only when date columns are present
- All numeric columns are included in statistical summary
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] `name` and `description` present and accurate
- [ ] `metadata.version` tracked; `metadata.dependencies` declares the Python stack
- [ ] No `license` field in frontmatter (license only in repo `LICENSE`)

### 2. Trigger Condition Clarity
- [ ] "When to Use This Skill" enumerates triggers (uploads a CSV, asks to summarize/analyze/visualize)
- [ ] Trigger is broad ("Uploads or references a CSV file") — potentially over-triggers on any CSV mention
- [ ] No negative routing to non-CSV tabular formats

### 3. Instruction Structure
- [ ] Hierarchy: Purpose → When to Use → How It Works → Behavior Guidelines → Usage → Example Prompts → Example Output → Files → Notes
- [ ] Heavy use of emphatic ALL-CAPS behavioral constraints
- [ ] Clear separation of ✅ correct vs ❌ forbidden behavior

### 4. Example / Output Quality
- [ ] Two example-output sketches (dataset overview, statistics, insights)
- [ ] Multiple worked adaptation examples (healthcare, inventory, web analytics, survey)
- [ ] Names the entry-point function `summarize_csv(file_path)`

### 5. Maintainability
- [ ] Declares files/dependencies (`analyze.py`, `requirements.txt`, sample data)
- [ ] Version-pinned dependency ranges
- [ ] Single self-contained skill; no external references split

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 20% | | |
| Instruction Structure | 25% | | |
| Example / Output Quality | 25% | | |
| Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. Upload a sales CSV and ask "summarize this"; verify the skill analyzes immediately without asking for options
2. Upload a customer dataset; verify it adapts analysis to the detected data type (segmentation, geographic patterns)
3. Upload a CSV with no date column; verify no time-series plot is attempted

### Boundary Test Cases
1. A CSV with only categorical columns — verify it degrades gracefully (frequency analysis, no numeric stats)
2. A very large CSV — verify behavior/prompt does not promise unbounded processing
3. A non-CSV file (e.g., `.xlsx`) — verify the trigger (CSV-specific) does not silently misfire

### Negative Test Cases
1. **Over-triggering**: any request that merely mentions "CSV" fires the full auto-analysis path — verify this does not hijack unrelated tasks
2. Whether the "NEVER ask the user" rule conflicts with cases needing clarification (e.g., password-protected or ambiguous files)
3. Whether missing `pandas`/`matplotlib` fail gracefully (dependency error handling is only implied)

## Notes
- End-user data-analysis artifact; the body is behavioral specification plus a Python entry-point reference.
- MIT license permits verbatim reproduction.
- The defining design trait is a strong "no questions, act immediately" behavioral contract — a useful stress case for trigger over-firing and instruction-conflict inspection.
- `resources/README.md` is referenced but not part of the single-artifact unit captured here.
