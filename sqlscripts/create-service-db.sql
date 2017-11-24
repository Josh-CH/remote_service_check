DROP TABLE IF EXISTS HOST;
CREATE TABLE Host(
	host_id	INTEGER PRIMARY KEY,
	hostname	TEXT	NOT NULL	UNIQUE
);

DROP TABLE IF EXISTS Service;
CREATE TABLE Service(
	service_id	INTEGER PRIMARY KEY,
	name	TEXT NOT NULL,
	port	INTEGER NOT NULL,
	protocol	TEXT	NOT NULL,
	UNIQUE(name, port, protocol)
);

DROP TABLE IF EXISTS Host_Service;
CREATE TABLE Host_Service(
		host_id	INTEGER NOT NULL,
		service_id INTEGER NOT NULL,
		PRIMARY KEY(host_id, service_id),
		FOREIGN KEY(host_id)	REFERENCES	Host(host_id),
		FOREIGN	KEY(service_id)	REFERENCES	Service(service_id)
);
