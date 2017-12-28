#!/usr/bin/env python
import util
import sqlite3

class Service():
	""" Service object used to interact with Sqlite database 
	Properties:
		records - iterable containing results of SQLite select query
		init_script - SQL script used to create the database tables
		select_script - SQL script for select records from the database
	Private attributes:
		_sql_insert_service - SQL command to insert into the Service table
		_sql_insert_host - SQL command to insert into the Host table
		_sql_insert_host_service - SQL command to insert into the Host_Service table
	"""
	def __init__(self):
			self._records = None
			self._init_script = None
			self._select_script = None
			self._sql_insert_service = util.read_file('scripts/insert-service.sql')
			self._sql_insert_host = util.read_file('scripts/insert-host.sql')
			self._sql_insert_host_service = util.read_file('scripts/insert-host_service.sql')
			self._sql_delete_host_service = util.read_file('scripts/delete-host_service.sql')

	@property
	def records(self): return self._records

	@property
	def init_script(self): return self._init_script

	@init_script.setter
	def init_script(self, script): self._init_script = script

	@property
	def select_script(self): return self._select_script

	@select_script.setter
	def select_script(self, script): self._select_script = script

	def set_records(self, cursor): 
		""" Fetch contents of SQL cursor and store value into _records 
			args:
				cursor - SQLite cursor that has executed a select statement
		"""
		self._records = cursor.fetchall()

	def insert_record(self, cursor, fields):
		"""
		args:
			cursor - SQL cursor
			*fields - tuple of (Hostname, Service, Port, Protocol)

			ex:

			fields = ('web01', 'httpd', '443', 'tcp')
			svc.insert_record(cursor, fields)

			Warning: the arguments to the tuple must be presented in order
		"""
		hostname = fields[0]
		service = fields[1]
		port = fields[2]
		protocol = fields[3]

		# Execute parameterized insert queries
		# If the records already exist, we can pass silently
		try:
			cursor.execute(self._sql_insert_host, (hostname,))
		except sqlite3.IntegrityError:
				pass
		try:
			cursor.execute(self._sql_insert_service, (service, port, protocol))
		except sqlite3.IntegrityError:
				pass
		try:
			cursor.execute(self._sql_insert_host_service, (hostname, service, port, protocol))
		except sqlite3.IntegrityError:
				pass

	def delete_record(self, cursor, primary_id):
		"""
		args:
			cursor - SQL cursor
			primary_id - Primary key of the Host_Service table. 
					Displayed by default output of program as 'Id'
		"""
		cursor.execute(self._sql_delete_host_service, primary_id)

	def pprint(self):
		""" Pretty Prints contents of SQL database """
		if self.records:
			for record in self.records:
					print('Id: {0: <5}  Hostname: {1: <15} ServiceName: {2: <15} Port: {3: <15} Protocol: {4}'.format(*record))
		else:
			print('There are no no records in the database')
