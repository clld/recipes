SELECT
  q1.macroarea, Value, cast(count_one AS float) / count_all * 100
FROM
  (
    SELECT 
      l.macroarea, count(v.id) AS count_all 
    FROM 
      ValueTable AS v, LanguageTable AS l 
    WHERE 
      l.macroarea IS NOT NULL AND l.ID = v.Language_ID AND v.Parameter_ID = 'GB020'
    GROUP BY 
      l.macroarea
  ) as q1
  LEFT JOIN
  (
    SELECT 
      l.macroarea, v.Value, count(v.id) AS count_one 
    FROM 
      ValueTable AS v, LanguageTable AS l 
    WHERE 
      l.macroarea IS NOT NULL AND l.ID = v.Language_ID AND v.Parameter_ID = 'GB020' 
    GROUP BY 
      l.macroarea, v.Value
    ) as q2
    ON q1.macroarea = q2.macroarea
ORDER BY
  q1.macroarea, Value
;
