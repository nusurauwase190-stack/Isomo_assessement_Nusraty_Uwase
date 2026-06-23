# Isomo Data Fellowship — Learner Engagement & Readiness Assessment
**Fellow:** Nusraty Uwase
**Mentor:** Pacifique M.
**Date:** June 25th, 2026
---
# Repository Overview
Learning platforms generate a constant stream of activity data — lessons completed, sessions logged, time spent. Assessments generate a separate, much smaller stream — scores recorded a few times a year. These two streams are rarely looked at together, and rarely linked to the same learner at all.

This repository is part of the **Isomo Data Fellowship 2026** assessment. Isomo works with learners across Rwanda, running them through two learning platforms — Typing and Quill — and tracking their progress through three assessments: EFSet, DET, and Northstar. This project links those two worlds together. Starting from raw, disconnected files with no shared learner or school ID, this repository builds the identity system needed to connect platform activity to assessment results, cleans and loads nine source files into a queryable database, and uses SQL to answer one concrete question:

> **Are the learners who engage the most on Typing and Quill the same learners who appear in EFSet, DET, and Northstar assessment records — or are there learners who are active but never assessed, and assessed learners who barely engage?**

There is no answer key for this question. The value of this repository is not just the final numbers, but the documented trail of decisions — how learner identity was constructed, how ambiguous matches were handled, and how each cleaning choice was made — that makes those numbers trustworthy.

---

## Repository Structure
├── data/                        # Cleaned CSV files — one per source file
├── queries/                     # SQL query files — one per analytical question
├── analysis/                    # Scripts and final program-ready report
├── docs/                        # All documentation
│   ├── learner_id_design.md     # Learner ID format, fields used, matching logic
│   ├── school_id_design.md      # School ID design and crosswalk approach
│   ├── cleaning_log.md          # Every cleaning decision across all nine files
│   └── ai_log.md                # How AI was used, what it got wrong, what I corrected
└── README.md                    # This file — start here
---

## Data Sources

| Category | Files |
|----------|-------|
| **Platform activity** | Typing activity logs, Quill activity logs |
| **Assessment results** | EFSet results, DET results, Northstar results |
| **Reference** | Master student list, master school list, school name crosswalk |

None of these files share a common learner or school identifier. Building that shared identity layer was the foundation everything else depended on.

---

## Approach Summary

### Layer 1 — Git
Repository structured and committed in stages with a clear, descriptive commit message at every milestone. The commit history reflects how the work was actually done.

### Layer 2 — Learner & School IDs
A unique, stable, reproducible ID was generated for every learner starting from the master student list. A matching school ID system was built using the crosswalk file. Where names did not match exactly across sources, fuzzy matching was applied and every decision documented. Unmatched records were flagged — never silently dropped.

### Layer 3 — Data Cleaning & Loading
All nine source files were cleaned — column names standardized, dates parsed, nulls handled, school names unified — then loaded into PostgreSQL. Every decision is recorded in `docs/cleaning_log.md`.

### Layer 4 — SQL Analysis
Seven queries were written across six required questions plus one self-directed question. Each query lives in its own named `.sql` file inside `queries/`. Topics covered: learner counts per source, school-level platform engagement, high-session low-score schools on Quill, assessment coverage gaps, and a full school-level summary table.

### Layer 5 — Final Output
A program-ready report in `analysis/` that answers the original question without requiring anyone to open a database. It identifies which learners are engaging, which are not, and where the gaps between platform activity and assessment records are sharpest.

---

## Key Findings

*This section will be completed once the full analysis is done. It will summarise which learners are most engaged, which schools lead in platform activity, and where the sharpest gaps between engagement and assessment coverage lie.*

---

## How to Reproduce

1. Clone this repository
2. Install dependencies: `pip install pandas psycopg2 fuzzywuzzy python-Levenshtein`
3. Set up a local PostgreSQL database
4. Run `analysis/01_clean_and_load.py` to clean all source files and load them
5. Run `analysis/02_generate_ids.py` to generate learner and school IDs
6. Execute the queries in `queries/` in numbered order
7. Run `analysis/03_final_report.py` to produce the final output

---

## Tools Used

| Tool | Purpose |
|------|---------|
| **Python** (pandas, psycopg2, fuzzywuzzy) | Data cleaning, ID generation, fuzzy name matching |
| **PostgreSQL** | Database for storing and querying all cleaned data |
| **SQL** | All analytical queries |
| **Claude by Anthropic** | AI coding assistant — used for generating code, debugging, and structuring logic |
| **GitHub** | Version control and public submission |
