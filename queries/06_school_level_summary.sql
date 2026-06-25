-- Query 6: School-level summary table with one row per school showing
-- active learners per platform, learners per assessment, and learners
-- with no assessment at all.

SELECT
    ms.canonical_name AS school,
    COUNT(DISTINCT tla.learner_id) AS typing_active_learners,
    COUNT(DISTINCT qal.learner_id) AS quill_active_learners,
    COUNT(DISTINCT ef.learner_id)  AS efset_learners,
    COUNT(DISTINCT det.learner_id) AS det_learners,
    COUNT(DISTINCT ns.learner_id)  AS northstar_learners,
    COUNT(DISTINCT CASE 
        WHEN ef.learner_id IS NULL 
        AND det.learner_id IS NULL 
        AND ns.learner_id IS NULL 
        THEN mst.learner_id END) AS learners_with_no_assessment
FROM master_school ms
LEFT JOIN master_student mst ON mst.school_id = ms.school_id
LEFT JOIN typing_lesson_activity tla ON tla.learner_id = mst.learner_id
LEFT JOIN quill_activity_long qal ON qal.learner_id = mst.learner_id
LEFT JOIN efset_results ef ON ef.learner_id = mst.learner_id
LEFT JOIN det_scores det ON det.learner_id = mst.learner_id
LEFT JOIN northstar_results ns ON ns.learner_id = mst.learner_id
GROUP BY ms.canonical_name
ORDER BY typing_active_learners DESC;
