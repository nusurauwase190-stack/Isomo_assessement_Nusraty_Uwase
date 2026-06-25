-- Query 1: How many unique learners appear in each platform and assessment source?
-- Format: one row per source with a learner count column.
-- This format was chosen for clarity — each source is easy to compare at a glance.

SELECT 'Typing (test attempts)'  AS source, COUNT(DISTINCT learner_id) AS unique_learners FROM typing_test_attempts
UNION ALL
SELECT 'Typing (lesson activity)', COUNT(DISTINCT learner_id) FROM typing_lesson_activity
UNION ALL
SELECT 'Quill (activity)',         COUNT(DISTINCT learner_id) FROM quill_activity_long
UNION ALL
SELECT 'Quill (sessions)',         COUNT(DISTINCT learner_id) FROM quill_connect_sessions
UNION ALL
SELECT 'EFSet',                    COUNT(DISTINCT learner_id) FROM efset_results
UNION ALL
SELECT 'DET',                      COUNT(DISTINCT learner_id) FROM det_scores
UNION ALL
SELECT 'Northstar',                COUNT(DISTINCT learner_id) FROM northstar_results
ORDER BY unique_learners DESC;
