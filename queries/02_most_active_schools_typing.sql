-- Query 2: Which schools have the most active learners on the Typing platform?
-- Measured by number of lesson activities per school.

SELECT 
    canonical_school_name AS school,
    COUNT(*) AS total_lesson_activities,
    COUNT(DISTINCT learner_id) AS unique_learners
FROM typing_lesson_activity
WHERE school_match_route != 'unmatched'
GROUP BY canonical_school_name
ORDER BY total_lesson_activities DESC;
