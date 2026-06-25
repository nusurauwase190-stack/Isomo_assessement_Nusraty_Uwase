-- Query 7 (self-directed): Which learners are in the top 25% for platform 
-- engagement but have never appeared in any assessment?
-- This directly answers the core question of the project.

WITH engagement AS (
    SELECT
        learner_id,
        COUNT(*) AS total_activities
    FROM (
        SELECT learner_id FROM typing_lesson_activity WHERE learner_id IS NOT NULL
        UNION ALL
        SELECT learner_id FROM typing_test_attempts WHERE learner_id IS NOT NULL
        UNION ALL
        SELECT learner_id FROM quill_activity_long WHERE learner_id IS NOT NULL
        UNION ALL
        SELECT learner_id FROM quill_connect_sessions WHERE learner_id IS NOT NULL
    ) all_platform
    GROUP BY learner_id
),
assessed AS (
    SELECT DISTINCT learner_id FROM efset_results WHERE learner_id IS NOT NULL
    UNION
    SELECT DISTINCT learner_id FROM det_scores WHERE learner_id IS NOT NULL
    UNION
    SELECT DISTINCT learner_id FROM northstar_results WHERE learner_id IS NOT NULL
),
top_engagers AS (
    SELECT learner_id, total_activities
    FROM engagement
    WHERE total_activities >= (
        SELECT PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY total_activities)
        FROM engagement
    )
)
SELECT
    te.learner_id,
    te.total_activities,
    ms.canonical_name AS learner_name,
    CASE WHEN a.learner_id IS NOT NULL THEN 'Assessed' ELSE 'Never Assessed' END AS assessment_status
FROM top_engagers te
LEFT JOIN master_student ms ON ms.learner_id = te.learner_id
LEFT JOIN assessed a ON a.learner_id = te.learner_id
ORDER BY te.total_activities DESC;
