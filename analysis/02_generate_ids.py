"""
generate_ids.py
---------------
Generates unique, stable, reproducible IDs for learners and schools
starting from the master reference files.

ID Format:
- School ID:  SCH001 to SCH040  (alphabetical by canonical school name)
- Learner ID: LRN00001 to LRN01001 (alphabetical by canonical learner name)

Design decisions:
- Alphabetical sorting ensures stability: same input always produces same ID
- Zero-padded numbers allow system to scale to future cohorts
- IDs are generated from canonical names only — no manual assignment
"""

import pandas as pd
import os

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REF_DIR  = os.path.join(DATA_DIR, "reference")
OUT_DIR  = os.path.join(DATA_DIR, "reference")

# ── 1. SCHOOL IDs ─────────────────────────────────────────────────────────────
print("Generating school IDs...")

schools = pd.read_csv(os.path.join(REF_DIR, "master_school.csv"))

# Sort alphabetically by canonical name for stability
schools = schools.sort_values("canonical_name").reset_index(drop=True)

# Generate school IDs: SCH001, SCH002, ...
schools["school_id"] = ["SCH{:03d}".format(i + 1) for i in range(len(schools))]

# Reorder columns
schools = schools[["school_id", "canonical_name", "active"]]

# Save mapping table
school_mapping = schools[["school_id", "canonical_name"]].copy()
school_mapping.to_csv(os.path.join(OUT_DIR, "school_id_mapping.csv"), index=False)
print(f"  ✓ {len(schools)} school IDs generated")
print(schools[["school_id", "canonical_name"]].to_string(index=False))

# ── 2. LEARNER IDs ────────────────────────────────────────────────────────────
print("\nGenerating learner IDs...")

students = pd.read_csv(os.path.join(REF_DIR, "master_student.csv"))

# Sort alphabetically by canonical name for stability
students = students.sort_values("canonical_name").reset_index(drop=True)

# Generate learner IDs: LRN00001, LRN00002, ...
students["learner_id"] = ["LRN{:05d}".format(i + 1) for i in range(len(students))]

# Save learner mapping table
learner_mapping = students[["learner_id", "canonical_name", "gender", "combinations", "is_admitted"]].copy()
learner_mapping.to_csv(os.path.join(OUT_DIR, "learner_id_mapping.csv"), index=False)

print(f"  ✓ {len(students)} learner IDs generated")
print(learner_mapping.head(10).to_string(index=False))

# ── 3. VERIFY ─────────────────────────────────────────────────────────────────
print("\n── Verification ──────────────────────────────────────────────────────")
print(f"Total schools:  {len(schools)}")
print(f"Total learners: {len(students)}")
print(f"Duplicate school IDs:  {schools['school_id'].duplicated().sum()}")
print(f"Duplicate learner IDs: {students['learner_id'].duplicated().sum()}")
print(f"Null school IDs:  {schools['school_id'].isnull().sum()}")
print(f"Null learner IDs: {students['learner_id'].isnull().sum()}")
print("\n✓ ID generation complete. Mapping files saved to data/reference/")
