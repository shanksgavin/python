select distinct(message), count(message)
from obj_model
where category = 'objectmodel.ModelCentral[0]'
group by message
