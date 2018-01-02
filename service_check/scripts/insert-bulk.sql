INSERT INTO Host(hostname) VALUES
('web-nginx-01'),
('proxy-nginx-01'),
('proxy-nginx-02'),
('dhcp-isc-01'),
('kdc-mit-01'),
('dns-bind-01'),
('log-elk-01'),
('pxe-cobbler-01'),
('repo-yum-01'),
('nagios-01'),
('web-apache-01');

INSERT INTO Service(name, port, protocol) VALUES
('nginx', 443, 'tcp'),
('nginx', 80, 'tcp'),
('dhcpd', 67, 'udp'),
('krb5kdc', 88, 'udp'),
('kadmin', 464, 'udp'),
('named', 53, 'udp'),
('elasticsearch', 9200, 'tcp'),
('kibana', 5601, 'tcp'),
('httpd', 80, 'tcp'),
('httpd', 443, 'tcp');

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'web-nginx-01'),
 (SELECT service_id FROM Service WHERE name = 'nginx' AND port = 443 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'proxy-nginx-01'),
 (SELECT service_id FROM Service WHERE name = 'nginx' AND port = 443 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'proxy-nginx-02'),
 (SELECT service_id FROM Service WHERE name = 'nginx' AND port = 443 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'dhcp-isc-01'),
 (SELECT service_id FROM Service WHERE name = 'dhcpd' AND port = 67 AND protocol = 'udp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'kdc-mit-01'),
 (SELECT service_id FROM Service WHERE name = 'krb5kdc' AND port = 88 AND protocol = 'udp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'kdc-mit-01'),
 (SELECT service_id FROM Service WHERE name = 'kadmin' AND port = 464 AND protocol = 'udp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'dns-bind-01'),
 (SELECT service_id FROM Service WHERE name = 'named' AND port = 53 AND protocol = 'udp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'log-elk-01'),
 (SELECT service_id FROM Service WHERE name = 'elasticsearch' AND port = 9200 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'log-elk-01'),
 (SELECT service_id FROM Service WHERE name = 'kibana' AND port = 5601 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'pxe-cobbler-01'),
 (SELECT service_id FROM Service WHERE name = 'httpd' AND port = 80 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'repo-yum-01'),
 (SELECT service_id FROM Service WHERE name = 'httpd' AND port = 443 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'nagios-01'),
 (SELECT service_id FROM Service WHERE name = 'httpd' AND port = 443 AND protocol = 'tcp'));

INSERT INTO Host_Service(host_id, service_id) VALUES
((SELECT host_id FROM HOST WHERE hostname = 'web-apache-01'),
 (SELECT service_id FROM Service WHERE name = 'httpd' AND port = 443 AND protocol = 'tcp'));
