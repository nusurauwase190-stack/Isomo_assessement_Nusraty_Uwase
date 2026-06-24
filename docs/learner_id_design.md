# Learner ID Design

## Format

`LRN00001` to `LRN01002`

- Prefix: `LRN` — identifies this as a learner ID
- Number: 5 zero-padded digits — supports up to 99,999 learners

## Source File

`data/reference/master_student.csv` — this is the source of truth for who a learner is.

## Fields Used

`canonical_name` — the only reliable identifier available across all source files.
No email, student number, or shared ID existed across the platform and assessment files.

## Generation Method

1. Load `master_student.csv`
2. Sort all learners alphabetically by `canonical_name`
3. Assign `LRN00001` to the first learner, `LRN00002` to the second, and so on
4. Save the mapping table to `data/reference/learner_id_mapping.csv`

## Why Alphabetical Sorting?

Sorting ensures stability — the same learner always gets the same ID every time
the script is run, regardless of when or on which machine. There is no randomness
in the assignment.

## Why Zero-Padding?

Without padding, text sorting would order `LRN10` before `LRN9`. Zero-padding
ensures correct ordering and future-proofs the system for larger cohorts.

## Handling Near-Matches Across Sources

Names do not always match exactly across platform and assessment files.
The strategy used:

- **Exact match first** — if a name in a source file matches `canonical_name` exactly, assign the ID directly
- **Fuzzy match second** — if no exact match, use fuzzy string matching (fuzzywuzzy, threshold 85) to find the closest canonical name
- **Flag unmatched** — if no match meets the threshold, the record is flagged with `match_status = unmatched` and kept in the data, never silently dropped

All fuzzy matches are logged in `docs/cleaning_log.md`.

## Extending the System for a New Cohort

1. Add new learners to `master_student.csv`
2. Re-run `analysis/02_generate_ids.py`
3. Existing learners retain their IDs because alphabetical sorting is stable
4. New learners receive the next available numbers in the sequence
