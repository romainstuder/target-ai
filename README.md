# 🧬 Target Validation Tool for Claude Code

An AI-powered drug target validation assistant that scores and ranks therapeutic targets against diseases using real-time data from Open Targets Platform and supplementary biomedical databases.

## What It Does

Given one or more **gene targets** and **diseases**, this tool:

1. **Resolves** gene symbols → Ensembl IDs and disease names → EFO IDs
2. **Fetches** evidence from Open Targets Platform (genetic associations, clinical trials, tractability, pathways, safety)
3. **Scores** each target–disease pair on three dimensions (0–5 each):
   - **Clinical Evidence** — GWAS hits, rare variants, clinical trial history
   - **Druggability** — small-molecule/antibody tractability, existing chemical matter
   - **Pathway/Biology** — pathway membership, tissue expression, animal models
4. **Ranks** by weighted composite score and provides a detailed narrative analysis
5. **Saves** results as Markdown report, CSV, and raw JSON

## Quick Start

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) installed (`npm install -g @anthropic-ai/claude-code`)
- An Anthropic API key or Claude Pro/Max subscription
- Python 3.10+ (for the helper script; Claude Code can also query APIs directly)
- No additional API keys needed — Open Targets Platform is free and open

### Setup

```bash
# Clone or download this project
git clone https://github.com/romainstuder/target-ai target-validation-tool
cd target-validation-tool

# Start Claude Code
claude
```

That's it. Claude Code reads the `CLAUDE.md` file on startup and becomes your target validation assistant.

### Usage — Commands

Once inside Claude Code, use these commands:

#### `validate` — Multi-target × multi-disease scoring
```
validate BRAF,KRAS — melanoma,lung cancer
validate PCSK9,HMGCR,ANGPTL3 — cardiovascular disease
validate CDK4,CDK6 — breast cancer, ovarian cancer
```

#### `score-target` — Deep-dive on a single target
```
score-target PCSK9 — cardiovascular disease, familial hypercholesterolemia
score-target EGFR — non-small cell lung cancer
```

#### `compare-targets` — Head-to-head comparison for one disease
```
compare-targets EGFR,HER2,HER3,MET — non-small cell lung cancer
compare-targets JAK1,JAK2,JAK3,TYK2 — rheumatoid arthritis
```

#### `find-targets` — Discover top targets for a disease
```
find-targets Alzheimer's disease
find-targets Crohn's disease --top 20
```

### Usage — Natural Language

You can also just talk to Claude naturally:

```
> What are the best drug targets for type 2 diabetes? Score the top 10.

> Is TREM2 a good target for Alzheimer's? Compare it against BACE1 and BIN1.

> I'm working on a grant proposal for targeting GPR84 in inflammatory bowel disease.
  Can you validate this target and identify the key risks?

> Score these oncology targets for pancreatic cancer: KRAS, TP53, CDKN2A, SMAD4
```

### Usage — Python Script (standalone)

The included Python script can also be run independently:

```bash
# Search for a target
python open_targets_client.py search-target BRAF

# Full validation
python open_targets_client.py validate "BRAF,KRAS" "melanoma,lung cancer"

# Get target tractability info
python open_targets_client.py target-info ENSG00000157764
```

## Scoring Methodology

### Dimensions & Weights

| Dimension | Weight | Data Sources |
|-----------|--------|-------------|
| Clinical Evidence | 40% | GWAS Catalog, ClinVar, ClinGen, UniProt, clinical trials (ChEMBL) |
| Druggability | 35% | Open Targets tractability, ChEMBL drugs, structural data |
| Pathway/Biology | 25% | Reactome, literature mining (EuropePMC), expression (Expression Atlas) |

### Composite Score

```
Composite = (Clinical × 0.40) + (Druggability × 0.35) + (Pathway × 0.25)
```

### Confidence Levels

| Level | Criteria |
|-------|---------|
| **High** | Composite ≥ 3.5 with data from ≥ 3 independent source types |
| **Medium** | Composite 2.0–3.49 or limited independent sources |
| **Low** | Composite < 2.0 or based primarily on literature mining |

## Output Files

After each validation run, results are saved to the `results/` directory:

| File | Contents |
|------|---------|
| `validation_{disease}.html` | **★ Interactive HTML scoring matrix** — open in browser |
| `validation_report.md` | Full Markdown report with tables and narrative |
| `scores.csv` | Machine-readable scores for downstream analysis |
| `raw_data.json` | Raw API responses for reproducibility and auditing |

## Project Structure

```
target-validation-tool/
├── CLAUDE.md                          # Core instructions (read by Claude Code on startup)
├── README.md                          # This file
├── open_targets_client.py             # Python API client + HTML generator
├── report_template.html               # HTML template (data injected by Python)
├── .claude/
│   └── skills/
│       ├── validate/SKILL.md          # validate skill
│       ├── score-target/SKILL.md      # score-target skill
│       ├── compare-targets/SKILL.md   # compare-targets skill
│       └── find-targets/SKILL.md      # find-targets skill
└── results/                           # Generated outputs
    ├── validation_melanoma.html       #   ★ Interactive HTML (primary deliverable)
    ├── validation_report.md
    ├── scores.csv
    └── raw_data.json
```

> **Note:** Commands are defined in both `.claude/skills/` and `.claude/commands/` for
> compatibility across Claude Code versions. You can also just type naturally —
> `CLAUDE.md` is always loaded and Claude will run the right Python command.

## Customization

### Adjusting Weights

Edit the composite formula in `CLAUDE.md` under "Step 4 — Compute Composite Score":

```
# Default: Clinical-heavy (industry standard)
Composite = (Clinical × 0.40) + (Druggability × 0.35) + (Pathway × 0.25)

# Academic / early discovery: Biology-heavy
Composite = (Clinical × 0.25) + (Druggability × 0.25) + (Pathway × 0.50)

# Repurposing focus: Druggability-heavy
Composite = (Clinical × 0.30) + (Druggability × 0.50) + (Pathway × 0.20)
```

### Adding New Scoring Criteria

Add new sub-scores to the rubric tables in `CLAUDE.md`. Claude Code will automatically incorporate them.

### Adding New Data Sources

Describe additional APIs or databases in `CLAUDE.md` under "Data Sources" and Claude Code will query them alongside Open Targets.

## Limitations

- **Scores are heuristic, not predictive.** They summarize available evidence but don't guarantee clinical success.
- **Data freshness.** Open Targets releases quarterly. Very recent trial results may require supplementary web search.
- **Bias toward well-studied targets.** Under-researched targets will score lower due to data scarcity, not necessarily due to poor biology.
- **Not a substitute for expert review.** Use this tool to prioritize and generate hypotheses, not as a final decision-maker.

## License

MIT — use freely for academic and commercial research.

## Acknowledgments

- [Open Targets Platform](https://platform.opentargets.org/) for the comprehensive, open-access target–disease association data
- [Anthropic Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) for the agentic coding framework
