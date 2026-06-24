"""
03_clean_data.py
----------------
Layer 3 of the Isomo Data Fellowship assessment pipeline.

This script takes all 10 raw source files — two platform activity files,
four Quill files, three assessment files, and three reference files — and
prepares them for loading into PostgreSQL.

Every file goes through the same core treatment:
  - Column names standardized to lowercase with underscores
  - Dates parsed into a consistent YYYY-MM-DD format
  - Null and empty values handled deliberately, not ignored
  - School names resolved to canonical names via the crosswalk file
  - Learner and school IDs applied from the mapping tables

Records that cannot be matched to a known learner or school are flagged
with match_status = 'unmatched' and kept in the data. Nothing is silently
dropped.

Output: 10 cleaned CSV files saved to data/cleaned/
"""

import pandas as pd
import os
from fuzzywuzzy import process, fuzz

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REF_DIR  = os.path.join(DATA_DIR, "reference")
PLAT_DIR = os.path.join(DATA_DIR, "platform")
ASMT_DIR = os.path.join(DATA_DIR, "assessments")
OUT_DIR  = os.path.join(DATA_DIR, "cleaned")

os.makedirs(OUT_DIR, exist_ok=True)

# ── Load mapping tables ───────────────────────────────────────────────────────
learner_map = pd.read_csv(os.path.join(REF_DIR, "learner_id_mapping.csv"))
school_map  = pd.read_csv(os.path.join(REF_DIR, "school_id_mapping.csv"))
crosswalk   = pd.read_csv(os.path.join(REF_DIR, "school_name_crosswalk.csv"))

# Build lookup dictionaries
learner_lookup = dict(zip(learner_map["canonical_name"].str.strip().str.lower(),
                          learner_map["learner_id"]))
school_lookup  = dict(zip(school_map["canonical_name"].str.strip().str.lower(),
                          school_map["school_id"]))

# Build school name crosswalk lookup (raw_name -> canonical_name)
crosswalk_approved = crosswalk[crosswalk["match_status"] == "approved"]
crosswalk_lookup = dict(zip(
    crosswalk_approved["raw_school_name"].str.strip().str.lower(),
    crosswalk_approved["canonical_name"].str.strip()
))

print("✓ Mapping tables loaded")
print(f"  Learners: {len(learner_lookup)} | Schools: {len(school_lookup)} | Crosswalk entries: {len(crosswalk_lookup)}")

# ── Helper functions ──────────────────────────────────────────────────────────

def standardise_columns(df):
    """Lowercase column names and replace spaces with underscores."""
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(" ", "_", regex=False)
                  .str.replace(r"[^\w]", "_", regex=True)
                  .str.replace(r"_+", "_", regex=True)
                  .str.strip("_"))
    return df

def parse_date(series, fmt=None):
    """Parse date column to YYYY-MM-DD string."""
    return pd.to_datetime(series, errors="coerce", format=fmt).dt.strftime("%Y-%m-%d")

def resolve_school_name(raw_name):
    """Resolve raw school name to canonical name via crosswalk, then fuzzy match."""
    if pd.isna(raw_name) or str(raw_name).strip() == "":
        return None, "missing"
    key = str(raw_name).strip().lower()
    if key in crosswalk_lookup:
        return crosswalk_lookup[key], "crosswalk_exact"
    match, score = process.extractOne(key, crosswalk_lookup.keys(), scorer=fuzz.token_sort_ratio)
    if score >= 85:
        return crosswalk_lookup[match], f"crosswalk_fuzzy_{score}"
    return raw_name, "unmatched"

def resolve_learner_name(raw_name):
    """Resolve raw learner name to learner_id via exact then fuzzy match."""
    if pd.isna(raw_name) or str(raw_name).strip() == "":
        return None, "missing"
    key = str(raw_name).strip().lower()
    if key in learner_lookup:
        return learner_lookup[key], "exact"
    match, score = process.extractOne(key, learner_lookup.keys(), scorer=fuzz.token_sort_ratio)
    if score >= 85:
        return learner_lookup[match], f"fuzzy_{score}"
    return None, "unmatched"

# ── 1. master_student ─────────────────────────────────────────────────────────
print("\n── Cleaning master_student ──────────────────────────────────────────")
df = pd.read_csv(os.path.join(REF_DIR, "master_student.csv"))
df = standardise_columns(df)
df["learner_id"] = df["canonical_name"].map(
    lambda x: learner_lookup.get(str(x).strip().lower()))
df["school_id"] = df["canonical_name"].map(
    lambda x: school_lookup.get(str(x).strip().lower()))
df.to_csv(os.path.join(OUT_DIR, "master_student_clean.csv"), index=False)
print(f"  ✓ {len(df)} rows | nulls in learner_id: {df['learner_id'].isna().sum()}")

# ── 2. master_school ──────────────────────────────────────────────────────────
print("\n── Cleaning master_school ───────────────────────────────────────────")
df = pd.read_csv(os.path.join(REF_DIR, "master_school.csv"))
df = standardise_columns(df)
df["school_id"] = df["canonical_name"].map(
    lambda x: school_lookup.get(str(x).strip().lower()))
df.to_csv(os.path.join(OUT_DIR, "master_school_clean.csv"), index=False)
print(f"  ✓ {len(df)} rows | nulls in school_id: {df['school_id'].isna().sum()}")

# ── 3. school_name_crosswalk ──────────────────────────────────────────────────
print("\n── Cleaning school_name_crosswalk ───────────────────────────────────")
df = pd.read_csv(os.path.join(REF_DIR, "school_name_crosswalk.csv"))
df = standardise_columns(df)
df["updated_at"] = parse_date(df["updated_at"])
df["notes"] = df["notes"].fillna("no_notes")
df.to_csv(os.path.join(OUT_DIR, "school_name_crosswalk_clean.csv"), index=False)
print(f"  ✓ {len(df)} rows")

# ── 4. typing_test_attempts ───────────────────────────────────────────────────
print("\n── Cleaning typing_test_attempts ────────────────────────────────────")
df = pd.read_csv(os.path.join(PLAT_DIR, "typing_test_attempts.csv"))
df = standardise_columns(df)
df["date"] = parse_date(df["date"])
df = df.drop(columns=["sso_school_id", "sso_school_folder"])
resolved = df["school_name"].apply(resolve_school_name)
df["canonical_school_name"] = [r[0] for r in resolved]
df["school_match_route"]    = [r[1] for r in resolved]
df["school_id"] = df["canonical_school_name"].map(
    lambda x: school_lookup.get(str(x).strip().lower()) if x else None)
df["curriculum"] = df["curriculum"].fillna("unknown")
df.to_csv(os.path.join(OUT_DIR, "typing_test_attempts_clean.csv"), index=False)
unmatched = (df["school_match_route"] == "unmatched").sum()
print(f"  ✓ {len(df)} rows | unmatched schools: {unmatched}")

# ── 5. typing_lesson_activity ─────────────────────────────────────────────────
print("\n── Cleaning typing_lesson_activity ──────────────────────────────────")
df = pd.read_csv(os.path.join(PLAT_DIR, "typing_lesson_activity.csv"))
df = standardise_columns(df)
df["date"] = parse_date(df["date"])
df = df.drop(columns=["sso_school_id", "sso_school_folder"])
resolved = df["school_name"].apply(resolve_school_name)
df["canonical_school_name"] = [r[0] for r in resolved]
df["school_match_route"]    = [r[1] for r in resolved]
df["school_id"] = df["canonical_school_name"].map(
    lambda x: school_lookup.get(str(x).strip().lower()) if x else None)
df["progress_pct"] = df["progress_pct"].fillna(-1)
df.to_csv(os.path.join(OUT_DIR, "typing_lesson_activity_clean.csv"), index=False)
unmatched = (df["school_match_route"] == "unmatched").sum()
print(f"  ✓ {len(df)} rows | unmatched schools: {unmatched}")

# ── 6. quill_activity_long ────────────────────────────────────────────────────
print("\n── Cleaning quill_activity_long ─────────────────────────────────────")
df = pd.read_csv(os.path.join(PLAT_DIR, "quill_activity_long.csv"))
df = standardise_columns(df)
df["date"] = parse_date(df["date"])
df = df.drop(columns=["mismatch_classification"])
df["standard"]       = df["standard"].fill
