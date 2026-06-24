# Cleaning Log

This log documents every cleaning decision made across all 10 source files.
All cleaning was performed by `analysis/03_clean_data.py`.

---

## 1. master_student.csv

**Rows:** 1,002 | **Columns:** 6

**Issues found:**
- `learner_id` and `school_id` columns were completely empty — these are placeholder columns waiting for generated IDs

**Decisions:**
- Applied generated learner IDs from `learner_id_mapping.csv` by matching on `canonical_name`
- School ID not directly assignable from this file — no school name column present
- All 1,002 rows matched successfully — zero nulls remaining in `learner_id`

---

## 2. master_school.csv

**Rows:** 40 | **Columns:** 3

**Issues found:**
- `school_id` column was completely empty

**Decisions:**
- Applied generated school IDs from `school_id_mapping.csv` by matching on `canonical_name`
- All 40 rows matched successfully — zero nulls remaining in `school_id`

---

## 3. school_name_crosswalk.csv

**Rows:** 180 | **Columns:** 9

**Issues found:**
- `notes` column was 92.2% empty (166 out of 180 rows)
- `updated_at` column was stored as a string date

**Decisions:**
- `notes` nulls filled with `"no_notes"` — column kept for transparency
- `updated_at` parsed to YYYY-MM-DD format

---

## 4. typing_test_attempts.csv

**Rows:** 14,533 | **Columns:** 16

**Issues found:**
- `sso_school_id` and `sso_school_folder` were 91.7% empty (13,327 out of 14,533 rows)
- `school_id` and `school_name` missing in 2,671 rows
- `curriculum` had 24 null values

**Decisions:**
- Dropped `sso_school_id` and `sso_school_folder` — too sparse to be useful
- School names resolved to canonical names via crosswalk file; fuzzy matching applied where exact match failed (threshold: 85)
- Unmatched school records flagged with `school_match_route = unmatched` — 754 rows flagged, none dropped
- `curriculum` nulls filled with `"unknown"`

---

## 5. typing_lesson_activity.csv

**Rows:** 13,306 | **Columns:** 15

**Issues found:**
- `sso_school_id` and `sso_school_folder` were 91.8% empty
- `school_id` and `school_name` missing in 2,707 rows
- `progress_pct` had 187 null values

**Decisions:**
- Dropped `sso_school_id` and `sso_school_folder` — same reason as typing_test_attempts
- School names resolved via crosswalk and fuzzy matching; 247 rows flagged as unmatched
- `progress_pct` nulls filled with `-1` to distinguish from a genuine 0% progress

---

## 6. quill_activity_long.csv

**Rows:** 12,311 | **Columns:** 17

**Issues found:**
- `mismatch_classification` was 99.7% empty (12,274 out of 12,311 rows)
- `standard` had 596 null values
- `score_pct` had 596 null values
- `time_spent_min` had 53 null values

**Decisions:**
- Dropped `mismatch_classification` — 99.7% empty, no analytical value
- `standard` nulls filled with `"no_standard"`
- `score_pct` nulls filled with `-1` to flag missing scores
- `time_spent_min` nulls filled with `-1` to flag missing time

---

## 7. quill_connect_sessions.csv

**Rows:** 11,715 | **Columns:** 13

**Issues found:**
- `mismatch_classification` was 99.7% empty (11,679 out of 11,715 rows)

**Decisions:**
- Dropped `mismatch_classification` — same reason as quill_activity_long
- No other nulls requiring action

---

## 8. efset_results_long.csv

**Rows:** 957 | **Columns:** 30

**Issues found:**
- `speaking_score` and `speaking_cefr` had 39 null values — speaking component not taken by all learners

**Decisions:**
- `speaking_score` nulls filled with `-1` to distinguish from a genuine zero score
- `speaking_cefr` nulls filled with `"not_taken"` to make the reason explicit

---

## 9. det_scores_long.csv

**Rows:** 891 | **Columns:** 46

**Issues found:**
- `Certificate`, `Note`, `certificate_link`, `note` columns were 100% empty
- `Surname(s)` had 21 null values
- File had duplicate column names after standardisation (raw and cleaned versions of same fields)

**Decisions:**
- Dropped all 100% empty columns — they carry no information
- Used the cleaned/processed columns (lowercase) over raw columns where duplicates existed
- `surname_s` nulls filled with `"unknown"`

---

## 10. northstar_results_long.csv

**Rows:** 2,131 | **Columns:** 11

**Issues found:**
- `school_id` and `school_name` were 100% empty across all 2,131 rows
- `assessment_date` was 60.8% empty (1,296 out of 2,131 rows)
- `score_pct` and `passed` had 228 null values each

**Decisions:**
- Dropped `school_id` and `school_name` — 100% empty, unusable
- Used `school_folder` column instead to resolve school identity via crosswalk; 69 rows flagged as unmatched
- `assessment_date` nulls left as null — no reliable way to impute a date; flagged in analysis
- `score_pct` nulls filled with `-1` to flag missing scores
- `passed` nulls filled with `"unknown"`
