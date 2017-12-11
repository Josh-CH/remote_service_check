#!/usr/bin/env python
import os

def file_exists(path):
	""" Checks if a path exists
	Args: 
		path
	Exceptions: 
		FileNotFoundError
	"""
	if os.path.exists(path):
		return True
	else:
		raise FileNotFoundError(path)

def read_file(_file):
		""" Returns contents of file"""
		try:
			with open(_file, 'r') as f:
				data = f.read()
		except FileNotFoundError as e:
				print(e)
				raise SystemExit
		return data

