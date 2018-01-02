-- Parameters are a tuple of (Hostname, Service, Port, Protocol
INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id 
  FROM HOST 
  WHERE hostname = ?),
 (SELECT service_id 
  FROM Service 
  WHERE name = ? 
  AND port = ? 
  AND protocol = ?));
