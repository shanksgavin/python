-- View: audit_oms

-- DROP VIEW audit_oms;

CREATE OR REPLACE VIEW audit_oms AS 
	SELECT a.audit_id, a.operation, a.stamp, 'settings' AS orig_table
	FROM audit_settings AS a

	UNION

	SELECT b.audit_id, b.operation, b.stamp, 'setup' AS orig_table
	FROM audit_setup AS b;

-- 
--  SELECT c.casenum, c.shapefield[0] AS x, c.shapefield[1] AS y, c.casestatus, c.elementid, c.element, c.pole_num, c.datestrt, c.dateend, c.remarks, c.cause, c.assignedto, count(cc.customer) AS custcount, c.timestrt
--    FROM cases c, casescustomers cc, meterbase mb
--   WHERE c.casenum::text = cc.casenum::text AND cc.customer::text = mb.elementid::text AND c.deleted = false AND cc.deleted = false AND c.casestatus::text !~~* '%CREATED%'::text AND c.casestatus::text !~~* '%CLOSED%'::text
--   GROUP BY c.casenum, c.shapefield[0], c.shapefield[1], c.casestatus, c.elementid, c.element, c.pole_num, c.datestrt, c.dateend, c.remarks, c.cause, c.assignedto, c.timestrt;
-- 

ALTER TABLE audit_oms OWNER TO postgres;
GRANT ALL ON TABLE audit_oms TO postgres;
COMMENT ON VIEW audit_oms IS 'Compiled Audit Trail of 16 OMS Tables';

