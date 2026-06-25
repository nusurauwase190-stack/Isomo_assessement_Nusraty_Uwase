# AI Log

This log documents how an AI coding agent (Claude) was used throughout this
project, what it got wrong on the first attempt, what had to be corrected,
and what I would do differently next time.

---

## What I asked the agent to do

- Scaffold the repository structure (Layer 1) and write a starter README.
- Help design a learner ID and school ID system from `master_student.csv`
  and `master_school.csv`, including a reproducible ID format and a fuzzy
  name-matching approach for the crosswalk file (Layer 2).
- Write the data cleaning scripts (`02_generate_ids.py`, `03_clean_data.py`)
  and the PostgreSQL loading script (`04_load_to_postgres.py`), and help me
  log every cleaning decision in `docs/cleaning_log.md` (Layer 3).
- Write the six required SQL queries plus my own self-directed query
  (Layer 4).
- Help me turn the SQL results into a final, program-lead-readable report,
  and write the script that produces that report (Layer 5).

## What it got wrong or left incomplete on the first attempt

- **README drifted from the actual file names.** The "How to Reproduce"
  section referenced `01_clean_and_load.py` and `03_final_report.py`,
  neither of which existed — the agent had renamed/restructured scripts
  partway through (`02_generate_ids.py`, `03_clean_data.py`,
  `04_load_to_postgres.py`) but never went back to update the README to
  match.
- **One query file was saved with a typo'd extension** —
  `05_assessment_coverage.sq` instead of `.sql` — which would have silently
  broken anyone trying to run the queries in numbered order.
- **The final report existed before the script that should have produced
  it.** The agent wrote `analysis/final_report.md` by hand from query
  output rather than writing a script that runs the queries and generates
  the report directly — meaning the report wasn't actually reproducible
  the way the assignment asked for.
- **The cleaned CSVs were never committed to `data/`.** They were written
  to a local `data/cleaned/` folder during testing but the commit step was
  skipped, even though the cleaning log (which was committed) implies they
  exist.

## What I had to correct or redirect

- Renamed the stray `.sq` file to `.sql`.
- Rewrote the README's reproduction steps to match the scripts that
  actually exist in the repo.
- Asked the agent to write `analysis/05_generate_final_report.py` so the
  report is generated programmatically from the live queries rather than
  hand-written, which is what Layer 5 actually asks for.
- Flagged that the 9 cleaned CSVs are missing from `data/` and need to be
  committed before submission.

## One thing I would do differently next time

I would ask the agent to do a final "repo consistency check" — cross
referencing every filename mentioned in the README and cleaning log
against what's actually committed — *before* declaring a layer done, not
after. Most of the issues above weren't wrong code, they were drift
between what got built and what got documented, and that's exactly the
kind of thing that's cheap to check early and annoying to find late.
