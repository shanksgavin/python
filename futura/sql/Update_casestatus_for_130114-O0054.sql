-- Original casestatus = 'CauseFound'
-- though case was not showing up in OMS Client
-- Trying to understand why and how this occurred
update cases
set casestatus = 'CauseFound'
where casenum = '130114-O0054'