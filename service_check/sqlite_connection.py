#!/usr/bin/env python
import sqlite3
class SqliteConnection():
	""" 
	Class that interacts with a SQLite database as a context manager
	"""
	def __init__(self, db):
			self.db = db
			self.conn = sqlite3.connect(self.db)
			self.cursor = self.conn.cursor()

	def __enter__(self):
			return Sqlite_Connection(self.db)
	def __exit__(self, exc_type, exc_val, exc_tb):
			if self.conn:
					self.conn.close()
