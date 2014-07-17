select substation.elementname, device.elementname
from device
join substation on device.elementid like '%' || substation.elementname || '%'
where device.element like 'BKR%'
order by device.elementid asc