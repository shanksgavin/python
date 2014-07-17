SELECT column_name, data_type, 
	case when data_type = 'character varying' then  character_maximum_length
		when data_type = 'integer' then numeric_precision
		when data_type = 'double precision' then numeric_precision
		else NULL
	end as length,
column_default, is_nullable
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name= 'cases'
order by column_name asc