select *
from interface_errors
where error_type_string = 'IVR'
and datetime between '2013-06-01' and '2013-06-30'