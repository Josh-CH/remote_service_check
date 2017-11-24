SELECT Host.hostname, Service.name, Service.port, Service.protocol
FROM Host_Service
INNER JOIN Host ON Host_Service.host_id = Host.host_id
INNER JOIN Service ON Host_Service.service_id = Service.service_id;
