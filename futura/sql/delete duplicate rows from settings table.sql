DELETE FROM settings
WHERE oid IN (SELECT oid
              FROM (SELECT oid,
                             row_number() over (partition BY setting_name, setting_value, type_info, category ORDER BY oid) AS rnum
                     FROM settings) t
              WHERE t.rnum > 1);