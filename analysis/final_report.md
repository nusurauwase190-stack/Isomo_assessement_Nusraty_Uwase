# Isomo Data Fellowship — Final Report
## Learner Engagement & Assessment Gap Analysis

**Fellow:** Nusraty Uwase
**Date:** June 25, 2026

---

## Introduction

This report presents the findings of an end-to-end data analysis conducted 
as part of the Isomo Data Fellowship 2026 assessment. Isomo runs learners 
across Rwanda through two learning platforms — Typing and Quill — and tracks 
their progress through three formal assessments: EFSet, DET, and Northstar.

These two streams — platform activity and assessment records — come from 
different systems, use different naming conventions, and share no common 
learner identifier. This analysis builds the identity layer needed to connect 
them, cleans and loads ten source files into a queryable database, and uses 
SQL to answer one concrete question: are the learners who engage the most on 
the platforms the same ones showing up in assessment records — or is there a 
gap?

---

## Data Overview

| Source | Records |
|--------|---------|
| Typing lesson activity | 13,306 |
| Typing test attempts | 14,533 |
| Quill activity | 12,311 |
| Quill sessions | 11,715 |
| EFSet results | 957 |
| DET results | 891 |
| Northstar results | 2,131 |
| Master students | 1,002 |
| Master schools | 40 |

---

## Key Findings

### 1. Platform engagement is high, assessment coverage is low
The platform files contain tens of thousands of activity records across 
Typing and Quill. The assessment files are significantly smaller — EFSet 
has 957 records, DET has 891, and Northstar has 2,131. This alone suggests 
that not all active learners are being assessed.

### 2. There are learners who are active on platforms but never assessed
Query 4 identified learners who appear in platform data but have no record 
in any of the three assessments. These are learners who are engaging with 
the learning tools but whose progress has never been formally measured.

### 3. Assessment coverage varies across schools
Query 6 shows significant variation at the school level. Some schools have 
strong platform engagement and good assessment coverage. Others have high 
platform activity but very few learners appearing in assessment records.

### 4. The most engaged learners are not always the most assessed
Query 7 — the core analytical question — identified learners in the top 25% 
of platform engagement who have never appeared in any assessment record. 
This is the sharpest gap in the data: learners who are clearly active and 
investing time in the platforms, but who are invisible to the formal 
assessment system.

---

## Recommendations for Programme Leads

1. **Prioritise assessment outreach for high-engagement learners** — 
   learners with the most platform activity who have never been assessed 
   should be the first group targeted for EFSet, DET, or Northstar 
   scheduling.

2. **Investigate school-level gaps** — schools with high Typing or Quill 
   activity but low assessment counts may face logistical barriers to 
   assessment participation.

3. **Use learner IDs consistently** — several records across files could 
   not be matched to a known learner. Consistent use of the learner ID 
   system introduced in this project would eliminate this gap in future 
   cohorts.

---

## How This Report Was Produced

All data was cleaned and loaded into PostgreSQL using Python scripts 
located in `analysis/`. The SQL queries in `queries/` were run against 
the database to produce the findings above. Every cleaning decision is 
documented in `docs/cleaning_log.md`, and the full ID design rationale 
is in `docs/learner_id_design.md` and `docs/school_id_design.md`. 
The repository README provides a complete overview of the project 
structure and step-by-step reproduction instructions.

---

## Conclusion

The data tells a clear story: platform engagement and assessment coverage 
are not the same thing, and they do not always overlap. There are learners 
who are consistently active on Typing and Quill but have never sat an 
EFSet, DET, or Northstar assessment. These learners are not disengaged — 
they are simply unassessed. Closing this gap is not a data problem; it is 
a programme decision. This analysis provides the evidence needed to make 
that decision deliberately.
