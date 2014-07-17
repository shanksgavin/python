-- selecting duplicate values from OMS Settings table

-- setup the columns you want displayed 
-- NOTE: OID column must be first to identify unique record for deleting
-- followed by '*' is easiest as it displays all fields, but can be limited or omitted
select oid, *
-- table to be searched for duplicate values
from settings as s
-- identifying column where duplicates are to be checked
-- NOTE: be sure to update column name after the WHERE and SELECT (must match)
where s.setting_name in (select si.setting_name
                -- Be sure when changing table that the following table matches the table on line 8
		from settings as si
		-- NOTE: Define all required columns for the table being searched
		-- pay attention to the defined alias names
		where si.setting_name = s.setting_name
		and si.setting_value = s.setting_value
                and si.type_info = s.type_info
		and si.category = s.category
                -- DO NOT DELETE THE NEXT LINE; It is critical to showing duplicates
		and si.oid != s.oid)
-- Don't forget to update the order by columns to match the new table being searched
order by s.setting_name, s.setting_value asc ;

-- Here is another way to quickly find out if a table has duplicate data based on defined criteria

-- Specify all the columns {can be just one if desired} to be considered unique in search
select distinct(s.setting_name, s.setting_value, s.type_info, s.category), count(*)
-- Update table to be searched
from settings as s
-- Make sure group by columns match those in the SELECT DISTINCT()
group by s.setting_name, s.setting_value, s.type_info, s.category
-- The HAVING statement can be increased if trying to find higher frequency of matching records
having count(*) > 1;