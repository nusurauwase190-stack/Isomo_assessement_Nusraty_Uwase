-- Query 4: Which learners appear in platform data but have no record 
-- in any of the three assessments?

SELECT DISTINCT p.learner_id
FROM (
    SELECT learner_id FROM typing_lesson_activity
    UNION
    SELECT learner_id FROM typing_test_attempts
    UNION
    SELECT learner_id FROM quill_activity_long
    UNION
    SELECT learner_id FROM quill_connect_sessions
) p
WHERE p.learner_id IS NOT NULL
AND p.learner_id NOT IN (
    SELECT learner_id FROM efset_results WHERE learner_id IS NOT NULL
    UNION
    SELECT learner_id FROM det_scores WHERE learner_id IS NOT NULL
    UNION
    SELECT learner_id FROM northstar_results WHERE learner_id IS NOT NULL
)
ORDER BY p.learner_id;
