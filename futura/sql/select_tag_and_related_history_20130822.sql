select t.tag_num, t.oid, t.record_id as tag_record_id, t.tag_status, th.record_id as history_record_id
from tags as t join tags_history as th on t.tag_num = th.tag_num
where t.tag_num in ('130820-T0717', '130822-T0001')
