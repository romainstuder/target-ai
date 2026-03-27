---
name: compare-targets
description: Compare multiple gene targets head-to-head for the same disease to help prioritize a drug development pipeline. Use when the user wants to compare, rank, or prioritize targets against each other. Triggers on "compare targets", "head to head", "which target", "prioritize targets".
---

# Compare Targets Head-to-Head

Compare multiple targets for the same disease to help prioritize a pipeline.

## Usage
```
/compare-targets EGFR,HER2,HER3,MET — non-small cell lung cancer
```

## Instructions

Given `$ARGUMENTS`:

1. **Parse.** Extract the list of targets (2–10) and exactly one disease.

2. **Resolve.** Map all identifiers via Open Targets search.

3. **Batch fetch.** For each target, collect:
   - Association score with the disease
   - Tractability assessment
   - Known drugs and clinical trial phase
   - Safety liabilities
   - Genetic constraint scores

4. **Score all targets** using the standard 0–5 rubrics.

5. **Produce a comparison table** sorted by Composite score:

   | Rank | Target | Clinical | Druggability | Pathway | Composite | Existing Drugs | Max Trial Phase | Key Differentiator |
   |---|---|---|---|---|---|---|---|---|

6. **Narrative comparison.** Write a brief (3–5 sentences per target) comparison highlighting:
   - Why the top-ranked target leads
   - Which target is the most novel/underexplored opportunity
   - Which target has the best safety profile
   - Any targets that should be deprioritized and why

7. **Save** to `results/comparison_{DISEASE}.md`.
