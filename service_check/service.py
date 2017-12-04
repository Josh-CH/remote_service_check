#!/usr/bin/env python

class Service():

	def __init__(self):
			self._records = None
	@property
		def records(self): return self._records
	
		@records.setter
		def records(self, cursor): self._records = cursor.fetchall()
		
		def execute(self, sql):
				self.cursor.execute(sql)
		
		def pprint(self):
				""" Prints contents of SQL database """
				if self.records:
					for record in self.records:
							print('Hostname: {0: <15} ServiceName: {1: <15} Port: {2: <15} Protocol: {3}'.format(*record))
