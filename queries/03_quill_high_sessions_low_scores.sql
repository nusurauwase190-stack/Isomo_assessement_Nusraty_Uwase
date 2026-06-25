-- Query 3: Which schools have learners on Quill with high session counts 
-- but low average scores?
-- High session = above average sessions | Low score = below 50%

SELECT
    q.school_id,
    COUNT(DISTINCT q.learner_id) AS unique_learners,
    COUNT(*) AS total_sessions,
    ROUND(AVG(q.score_pct)::numeric, 2) AS avg_score_pct
FROM quill_connect_sessions q
WHERE q.score_pct != -1
GROUP BY q.school_id
HAVING 
    COUNT(*) > (SELECT AVG(session_count) FROM 
                (SELECT learner_id, COUNT(*) AS session_count 
                 FROM quill_connect_sessions GROUP BY learner_id) s)
    AND AVG(q.score_pct) < 50
ORDER BY total_sessions DESC;
