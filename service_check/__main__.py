#!/usr/bin/env python
import argparse
import sqlite_connection, util, service, ansible_executor

# Completed features
# 1. Auto initialize the database
# 2. Prett print the contents of the database as the default if no parameters are selected
# 3. Provided functionality to insert new services into the database. Inserting existing records do nothing
# 4. Provide functionality to delete a record based on unique ID

# Todo
# 1. Build ansible class to run ansible
# 2. Include colorama functionality to printing the content
# 3. Provide a watch subcommand that rechecks the service status every X seconds
# 4. Potentially add a 'show' subparser to customize output formatting
# 5. Convert my module imports to work with packages when I am ready to deploy
def main():
	
	parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--db', help='Path to Sqlite database',
						default='db/services.sql')

	# NOTICE:
	# Redefine these variables as private variables in the service class
	init_script = 'scripts/create-service-db.sql'
	select_script = 'scripts/select-service.sql'
	remote_script = 'scripts/service_check.sh'

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
		svc = service.Service()

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
