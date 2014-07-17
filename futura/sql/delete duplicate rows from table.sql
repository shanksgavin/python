DELETE FROM oms_logfiles.omslogs
WHERE log_id IN (SELECT log_id
              FROM (SELECT log_id,
                             row_number() over (partition BY date_, time_, message, logfile ORDER BY log_id) AS rnum
                     FROM oms_logfiles.omslogs) t
              WHERE t.rnum > 1);