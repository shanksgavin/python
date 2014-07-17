select *
from historicaloutages as out
join historicaltroublecalls as tc on out.prikey = tc.outageid
where out.prikey = 136578087