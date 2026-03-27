---
name: find-targets
description: Discover and rank the most promising therapeutic targets for a given disease. Use when the user wants to find targets, discover targets, or identify drug targets for a disease. Triggers on "find targets", "discover targets", "top targets for", "what targets".
---

# Discover Top Targets for a Disease

Given a disease, find and rank the most promising therapeutic targets.

## Usage
```
/find-targets Alzheimer's disease
/find-targets EFO_0000249 --top 20
```

## Instructions

Given `$ARGUMENTS`:

1. **Parse.** Extract the disease name or EFO ID. Optionally parse `--top N` (default: 10).

2. **Resolve.** Map to EFO ID via Open Targets search.

3. **Fetch top associated targets** from Open Targets:

```graphql
query topTargets($efoId: String!, $size: Int!) {
  disease(efoId: $efoId) {
    name
    associatedTargets(
      page: { size: $size, index: 0 }
      aggregationFilters: []
    ) {
      count
      rows {
        target {
          id
          approvedSymbol
          biotype
        }
        score
        datatypeScores { componentId score }
      }
    }
  }
}
```

4. **For each target,** also fetch tractability to compute a quick Druggability score.

5. **Score and rank** using the standard rubrics, prioritizing targets with:
   - High overall association score
   - High tractability
   - Genetic evidence (not just literature)
   - Existing chemical matter or clinical precedent

6. **Output** a ranked table plus brief rationale for the top targets.

7. **Highlight novel opportunities** — targets ranked in the top 20 by association but with
   NO approved drugs and NO Phase 3 trials. These represent white-space opportunities.

8. **Save** to `results/targets_for_{DISEASE}.md`.
