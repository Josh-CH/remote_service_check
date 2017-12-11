#!/usr/bin/env python
import sqlite3
import os
class SqliteConnection():
	""" 
	Class that interacts with a SQLite database as a context manager
	"""
	def __init__(self, db):
		self.db = os.path.abspath(db)
		self.conn = sqlite3.connect(self.db)
		self.cursor = self.conn.cursor()
		self.empty = self.is_empty()

	def __repr__(self):
			return '{0}(db={1}, conn={2}, cursor={3}, empty={4})'.format(self.__class__.__name__, 
																		self.db, 
																		self.conn, 
																		self.cursor, 
																		self.empty)
	def __enter__(self):
			return SqliteConnection(self.db)

	def __exit__(self, exc_type, exc_val, exc_tb):
			if self.conn:
					self.conn.close()

	def is_empty(self):
			""" Checks if the Sqlite database has any tables
			Returns:
				1 if there are no tables
				0 if there is one or more tables
			"""
			self.cursor.execute('SELECT name FROM sqlite_master')
			length = len(self.cursor.fetchall())
			return 0 if length >= 1 else 1
