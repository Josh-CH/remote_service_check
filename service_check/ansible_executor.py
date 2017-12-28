#!/usr/bin/env python
import os
import subprocess as sp
import colorama

class Ansible_Executor():
		""" Checks status of services on remote hosts using ansible """
		def __init__(self, records, script):
			self.records = records
			self.script = script

		def execute(self):
			colorama.init()
			try:
				for record in self.records:
						with open(os.devnull, 'w') as devnull:
								results = sp.run(['ansible', record[1], '-m', 'script', '-a', '{0} {1} {2} {3}'.format(self.script, record[2], record[3], record[4])], stdout=devnull, stderr=devnull)
						if results.returncode == 0:
							print('{0}Host {2} is successfully running service {3} on port {4}'.format(
								  colorama.Fore.BLUE, *record))
						else:
							print('{0}Host {2} is NOT running service {3} on port {4}'.format(
									colorama.Fore.RED, *record))
			except sp.CalledProcessError as e:
					print(e)
