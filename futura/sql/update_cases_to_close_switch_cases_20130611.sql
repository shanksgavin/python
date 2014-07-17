-- select *
-- from cases
-- where deleted = 'f'
-- and casestatus = 'CauseFound'
-- and cause = 'none provided!'
-- order by casenum desc

-- closed old switching cases
-- audit_cases table audit_id in (1425, 1426, 1427)

update cases set casestatus = 'Closed'
where deleted = 'f'
and casestatus = 'CauseFound'
and cause = 'none provided!'