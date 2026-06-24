# School ID Design

## Format

`SCH001` to `SCH040`

- Prefix: `SCH` — identifies this as a school ID
- Number: 3 zero-padded digits — supports up to 999 schools

## Source File

`data/reference/master_school.csv` — this is the source of truth for all schools.

## Fields Used

`canonical_name` — the standardised school name used as the basis for ID generation.

## Generation Method

1. Load `master_school.csv`
2. Sort all schools alphabetically by `canonical_name`
3. Assign `SCH001` to the first school, `SCH002` to the second, and so on
4. Save the mapping table to `data/reference/school_id_mapping.csv`

## Why Alphabetical Sorting?

Same reason as learner IDs — alphabetical sorting ensures that the same school
always gets the same ID every time the script is run. It is stable and reproducible.

## The School Name Problem

Schools appear under many different names across source files. The same school
can appear as an abbreviation, a full name, a spelling variant, or a
completely different name entirely. Real examples from this dataset:

- `ASYV` also appears as "Agahozo Shalom Youth Village - Liquidnet High School"
  and "LIQUIDNET FAMILY HIGH SCHOOL"
- `ES Sancta Maria Karambo` also appears as "ES Santa Maria Karambo"
- `Cornerstone Leadership Academy` also appears as "CLA" and "Cornerstone LA"
- `ENDP Karubanda` also appears as "ECOLE NOTRE DAME DE LA PROVIDENCE KARUBANDA"

The `school_name_crosswalk.csv` file maps every raw name variant back to the
correct `canonical_name`. This crosswalk is applied during data cleaning so
that every record ends up linked to the correct school ID.

## Extending the System for a New Cohort

1. Add new schools to `master_school.csv`
2. Add any new name variants to `school_name_crosswalk.csv`
3. Re-run `analysis/02_generate_ids.py`
4. Existing schools retain their IDs because alphabetical sorting is stable
5. New schools receive the next available numbers in the sequence
