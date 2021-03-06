#!/usr/bin/env python
import argparse, os, sys
from service_check import sqlite_connection, util, service, ansible_executor
PACKAGE_ROOT = os.path.dirname(service.__file__)

def main():
	
	parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--db', help='Path to Sqlite database',
						default=os.path.join(PACKAGE_ROOT, 'db/services.sql'))

	# NOTICE:
	# Redefine these variables as private variables in the service class
	init_script = os.path.join(PACKAGE_ROOT, 'scripts/create-service-db.sql')
	select_script = os.path.join(PACKAGE_ROOT, 'scripts/select-service.sql')
	remote_script = os.path.join(PACKAGE_ROOT, 'scripts/service_check.sh')

	# Create sub parsers
	subparsers = parser.add_subparsers(dest='subparser_name')
	insert_parser = subparsers.add_parser('insert')
	delete_parser = subparsers.add_parser('delete')
	check_parser = subparsers.add_parser('check')

	# Create sub options for insert parser
	insert_parser.add_argument('--hostname', help='Hostname of server running service', required=True)
	insert_parser.add_argument('--servicename', help='Name the host uses to identify the service', required=True)
	insert_parser.add_argument('--port', help='Numerical port the service listens on', required=True)
	insert_parser.add_argument('--protocol', help='Protocol the service runs on', required=True,
								choices=[ 'tcp', 'udp' ])

	# Create sub options for delete parser
	delete_parser.add_argument('--id', help='id of service to delete', required=True)

	# Create sub options for check parser
	check_parser.add_argument('--remote-script', help='script to run on remote host through ansibles script module',
						default = remote_script)

	# Parse the arguments
	args = parser.parse_args()

	# Create our objects
	with sqlite_connection.SqliteConnection(args.db) as conn:
		# Make foreign key support explicit
		conn.cursor.execute('pragma foreign_keys=ON;')
		svc = service.Service(PACKAGE_ROOT)

		# Initialize the database if no tables exist
		if conn.empty == 1:
			svc.init_script = init_script
			conn.cursor.executescript(util.read_file(svc.init_script))
			conn.conn.commit()
			print('Database was initialized')
	
		# Store the records of the database in a variable
		svc.select_script = select_script
		conn.cursor.execute(util.read_file(svc.select_script))
		svc.set_records(conn.cursor)
	
		# Perform main program logic
		# --------------------------
		# If no options are selected, pretty print content of the database
		if args.subparser_name is None:
				svc.pprint()
		elif args.subparser_name == 'insert':
				insert_args = (args.hostname, args.servicename, args.port, args.protocol)
				svc.insert_record(conn.cursor, insert_args)
		elif args.subparser_name == 'delete':
				delete_args = (args.id,)
				svc.delete_record(conn.cursor, delete_args)
		elif args.subparser_name == 'check':
				remote_exec = ansible_executor.Ansible_Executor(svc.records, args.remote_script) 
				remote_exec.execute()

if __name__ == '__main__':
		main()
