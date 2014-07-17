SELECT
  cases.record_id::text,
  cases.casenum::text,
  cases.feeder::text,
  cases.custout::text,
  cases.totalcustdownstream::text,
  cases.phase::text,
  cases.datestrt::date,
  cases.dateend::date,
  ((cases.enddate - cases.startdate)/ (1000*60.0) + 0.04)::decimal AS duration_minutes,
  ((cases.enddate - cases.startdate)/ (1000*60.0) * cases.totalcustdownstream)::decimal AS customer_interruption_duration,
  cases.timestrt,
  cases.timeend,
  cases.element::text,
  cases.elementname::text,
  cases.custhours::text,
  cases.cause::text,
  substation_breakers.name::text as sub_name
FROM
  public.cases
  CROSS JOIN
  public.substation_breakers
 WHERE
  position (ltrim(rtrim(CAST (cases.feeder AS text))) IN CAST(substation_breakers.breaker_list AS text)) != 0
  AND ltrim(rtrim(upper(casestatus))) LIKE '%CLOSED%'
  and cases.deleted = 'false'
  and cases.datestrt >= '2013-03-26'::date
  and cases.dateend <= '2014-04-10'::date
  --AND substation_breakers.name = $P{sub_name}

UNION

SELECT
	h_outs.prikey::text as record_id,
	h_outs.prikey::text as casenum,
	h_outs.source_branch::text as feeder,
	h_outs.customercount::text as custout,
	h_outs.customercount::text as totalcustdownstream,
	h_outs.traceattribute::text as phase,
	h_outs.creationdate::date as datestrt,
	h_outs.closedtime::date as dateend,
	(EXTRACT(EPOCH FROM (h_outs.closedtime - h_outs.creationdate)) / 60)::decimal as duration_minutes,
	((EXTRACT(EPOCH FROM (h_outs.closedtime - h_outs.creationdate)) / 60) * h_outs.customercount)::decimal AS customer_interruption_duration,
	h_outs.creationdate::time without time zone as timestrt,
	h_outs.closedtime::time without time zone as timeend,
	'element'::text as element,
	'elementname'::text as elementname,
	'custhours'::text as custhours,
	'cause'::text as cause,
	h_outs.source::text as sub_name
FROM historic_data.historicaloutages h_outs
WHERE h_outs.creationdate >= '2013-03-26'::date
	and h_outs.closedtime <= '2014-04-10'::date
	--AND h_outs.source = $P{sub_name}
ORDER BY
	feeder,
	datestrt asc;