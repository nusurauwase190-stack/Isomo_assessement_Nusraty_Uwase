"""
04_load_to_postgres.py
----------------------
Loads all cleaned CSV files into PostgreSQL database (isomo_db).
"""

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

engine = create_engine('postgresql://postgres:postgres123@localhost:5432/isomo_db')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")

files = {
    "master_student":           "master_student_clean.csv",
    "master_school":            "master_school_clean.csv",
    "school_name_crosswalk":    "school_name_crosswalk_clean.csv",
    "typing_test_attempts":     "typing_test_attempts_clean.csv",
    "typing_lesson_activity":   "typing_lesson_activity_clean.csv",
    "quill_activity_long":      "quill_activity_long_clean.csv",
    "quill_connect_sessions":   "quill_connect_sessions_clean.csv",
    "efset_results":            "efset_results_clean.csv",
    "det_scores":               "det_scores_clean.csv",
    "northstar_results":        "northstar_results_clean.csv",
}

for table_name, filename in files.items():
    filepath = os.path.join(CLEAN_DIR, filename)
    df = pd.read_csv(filepath)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✓ Loaded {table_name}: {len(df)} rows")

print("\n✓ All tables loaded into isomo_db!")
