-- sqlite doesnt implement inner joins in delete queries
-- so only the mapping table has the record removed.
-- The mapping table is required to join the records in the Host and Service
-- tables, so the records have the effect of being deleted
DELETE
FROM Host_Service
WHERE Host_Service.host_service_id = ?;
