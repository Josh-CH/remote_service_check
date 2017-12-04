#!/usr/bin/env python
import sqlite3
import os
import argparse
import subprocess as sp
try:
	import colorama
except ImportError as e:
		print(e)
		raise SystemExit
# todo
# 1. Check if database isnt initialized
# 2. Add functionality to add, update, or remove database records through the command line
# 3. Create different output for when you fail to connect to a host

def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-d', '--database-file', help='sqlite3 database containing hosts and services',
						default='services.sql', nargs='?')
	parser.add_argument('--select-script', help='sql script containing select statement',
						default='sqlscripts/select-service.sql', nargs='?')
	parser.add_argument('--remote-script', help='Script to run on remote hosts',
						default='service_check.sh', nargs='?')
	parser.add_argument('--check-services', action='store_true',
						help='Execute Ansible to check service statuses remotely')

	args = parser.parse_args()
	select_cmd = read_file(args.select_script)

	with Service_Check(args.database_file) as sc:
		sc.set_records(select_cmd)
		if args.check_services:
				sc.run_ansible(args.remote_script)
		else:
			sc.pprint()

class Service_Check():
		""" 
		Class that interacts with a SQLlite database, and
		performs remote commands with ansible
		"""
		def __init__(self, db):
				self.db = db
				self.conn = sqlite3.connect(self.db)
				self.cur = self.conn.cursor()

		def set_records(self, sql):
				""" Executes SQL to select all joined records
				in the sqlite database, and saves to a varaible"""
				self.cur.execute(sql)
				self.records = sorted(self.cur.fetchall())

		def run_ansible(self, script):
				""" Checks status of services on remote hosts using ansible """
				colorama.init()
				try:
					for record in self.records:
							with open(os.devnull, 'w') as devnull:
									results = sp.run(['ansible', record[0], '-m', 'script', '-a', '{0} {1} {2} {3}'.format(script, record[1], record[2], record[3])], stdout=devnull, stderr=devnull)
							if results.returncode == 0:
								print('{0} Host {1} is successfully running service {2} on port {3}'.format(
									  colorama.Fore.BLUE, *record))
							else:
								print('{0} Host {1} is NOT running service {2} on port {3}'.format(
										colorama.Fore.RED, *record))
				except sp.CalledProcessError as e:
						print(e)
						raise SystemExit

		def pprint(self):
				""" Prints contents of SQL database """
				for record in self.records:
						print('Hostname: {0: <15} ServiceName: {1: <15} Port: {2: <15} Protocol: {3}'.format(*record))

		def __enter__(self):
				return Service_Check(self.db)
		def __exit__(self, exc_type, exc_val, exc_tb):
				if self.conn:
						self.conn.close()

def read_file(_file):
		""" Returns contents of file"""
		try:
			with open(_file, 'r') as f:
				data = f.read()
		except FileNotFoundError as e:
				print(e)
				raise SystemExit
		return data

if __name__ == '__main__':
	main()
