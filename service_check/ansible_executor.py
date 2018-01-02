#!/usr/bin/env python
import os
import subprocess as sp
from subprocess import PIPE
import socket
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
								results = sp.run(['ansible', record[1], '--timeout', '5', '-m', 'script', '-a', '{0} {1} {2} {3}'.format(self.script, record[2], record[3], record[4])], stdout=PIPE, stderr=PIPE)
						if results.stderr:
							print('{0}{1}'.format(
									colorama.Fore.RED, results.stderr.decode('utf-8').split('\n')[0]))

						elif '"unreachable": true' in results.stdout.decode('utf-8'):
							print('{0}Could not automatically connect to host {1}'.format(colorama.Fore.YELLOW, record[1]))

						elif results.returncode == 0:
							print('{0}Host {2} is successfully running service {3} on port {4}'.format(
								  colorama.Fore.BLUE, *record))
						else:
							print('{0}Host {2} is NOT running service {3} on port {4}'.format(
									colorama.Fore.RED, *record))
			except sp.CalledProcessError as e:
					print(e)

