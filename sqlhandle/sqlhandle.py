import pymysql
import numpy as np
import pandas as pd
from datetime import datetime


class modArray():
	# [ 	[a1, a2],				[	[a1, b1, c1],
	#		[b1, b2],	---> 			[a2, b2, c2] ]
	#		[c1, c2] ]
	def flip(self, arr):
		newarr = []
		for item_y in range(0, len(arr[0])) :
			element = []
			cnt = 1
			for item_x in range(0, len(arr)):
				element.append(arr[item_x][item_y])
			newarr.append(element)
		return newarr

	# is in Array?
	def find(self, value, arr):
		res = []
		for row in range(0, len(arr)):
			for col in range(0, len(arr[row])):
				if value == arr[row][col]:
					res.append([row, col])
		return res




class sqlhandle():
	__debugEN = 1
	__debugEN01 = 0
#	__instance   = None
	__host       = None
	__user       = None
	__password   = None
	__database   = None
	__session    = None
	__connection = None

	#################
	### INTERNALs ###
	#################

	# Debug method
	def __debug(self, str):
		if self.__debugEN == 1 :
			print("[SQL] {}".format(str))
	def __debug01(self, str):
		if self.__debugEN01 == 1 :
			print("[SQL] {}".format(str))

	# set debug
	def setDebug(self, level=0, value=1):
		if level == 0:
			self.__debugEN = value
			return 0
		elif level == 1:
			self.__debugEN01 = value
			return 0
		else:
			return 1

	# init instance of object
	def __init__(self, host='localhost', user='root', password='', database=''):
		self.__host     = host
		self.__user     = user
		self.__password = password
		self.__database = database
		self.__open()
	# END def __init__

	# __open - opens connection to database
	def __open(self):
		try:
			cnx = pymysql.connect(self.__host, self.__user, self.__password, self.__database)
			self.__connection = cnx
			self.__session    = cnx.cursor()
			self.__debug01("__open: {}@{} db '{}'".format(self.__user, self.__host, self.__database))
			return 0
		except pymysql.Error as e:
			self.__debug01("ERROR: __open: {}".format(e))
			return e
	# END def __open

	# __close - closes connection
	def __close(self):
		try:
			self.__session.close()
			self.__connection.close()
			self.__debug01("__close: CLOSED")
		except pymysql.Error as e:
			self.__debug01("ERROR: __close: {}".format(e))
			return e
	# END __close

	# __exec - executes commands
	def __exec(self, query, values):
		if self.isConnected() == False:
			self.__debug01("reconnecting...")
			self.connect()
		try:
			req = "{} {} ;".format(query, values)
			self.__debug01("__exec: {}".format(req))
			return self.__session.execute(req)
		except pymysql.Error as e:
			self.__debug01("ERROR: __exec: {}".format(e))
			return e
	# END __exec

	# __modTubs
	def __modTubs(self, *args):
		values = ""
		cnt = 1
		for item in args :
			values += item
			if cnt != len(args):
				values += ", "
			cnt += 1
		return values

	# __modTubs
	def __modTubsBrcks(self, *args):
		values = ""
		cnt = 1
		for item in args :
			values += "({})".format(item)
			if cnt != len(args):
				values += ", "
			cnt += 1
		return values

	################
	###  BASICs  ###
	################

	# connect
	def connect(self):
		"""
		Connects sqlhandle
		"""
		self.__open()

	# isconnected
	def isConnected(self):
		"""
		Checks if the sqlhandle is connected.
		Connected: True
		Desconnected: False
		"""
		if hasattr(self.__session, 'execute'):
			return 1
		return 0

	# disconnect
	def disconnect(self):
		"""
		Disonnects sqlhandle
		"""
		self.__close()

	################
	### DATABASE ###
	################

	# check if db is available
	def dbAvailable(self, db, force=0):
		"""
		Checks if Database is available.
		force=0, Just check (default)
		force=1, Create if not exists
		"""
		if force == 1 :
			self.__exec("CREATE DATABASE", db)
		res = self.__exec("SHOW DATABASES LIKE", "'{}'".format(db))
		self.__debug("dbAvailable: <{}> f{} {}".format(db, force, res))
		return res
	# END dbAvailable

	# drop database
	def dbDrop(self, db):
		"""
		Drops a Database
		"""
		res = self.__exec("DROP DATABASE", db)
		self.__debug("dbDrop: <{}> {}".format(db, res))
		return res
	# END dbDrop

	# create db
	def dbCreate(self, db, force=0):
		"""
		Creats a Database
		force=0, Just create (default)
		force=1, Drop and recreate
		"""
		if force == 1 :
			self.__exec("DROP DATABASE", db)
		res = self.__exec("CREATE DATABASE", db)
		self.__debug("dbCreate: <{}> f{} {}".format(db, force, res))
		return res

	# list db --- BUG
	#def dbList(self):
	#	try:
	#		databases = ("show databases")
	#		self.cursor.execute(databases)
	#		for (databases) in cursor:
	#			print (databases[0])
	#	except pymysql.Error as e:
	#		print(e)
	#		return e

	# db use
	def dbUse(self, db, force=0):
		"""
		Uses a Database
		force=0, Just use (default)
		force=1, Create if not exists
		force=2, Drop and recreate
		"""
		if force == 1 :
			self.__exec("CREATE DATABASE", db)
		elif force == 2:
			self.__exec("DROP DATABASE", db)
			self.__exec("CREATE DATABASE", db)
		res = self.__exec("USE", db)
		self.__debug("dbUse: <{}> f{} {}".format(db, force, res))
		return res
	# END dbUse

	# table available?
	def tblAvailable(self, tbl, *cmd, force=0):
		"""
		Checks if a Table is available
		*cmd, describe Table if you want to force one
		default - "ID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID)"
		force=0, Just Check (default)
		force=1, Create Table if not exists
		"""
		res = self.__exec("SHOW TABLES LIKE", """ "{}" """.format(tbl))
		if res == 0 :
			if force == 1 :
				if len(cmd) != 0 :
					values = self.__modTubs(*cmd)
				else:
					values = "ID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID)"
				self.__exec("CREATE TABLE", "{} ({})".format(tbl, values))
				self.__debug("tblAvailable: <{}> 1".format(tbl))
				return 1
			self.__debug("tblAvailable: <{}> {}".format(tbl, res))
			return 0
		else:
			self.__debug("tblAvailable: <{}> {}".format(tbl, res))
			return res

	# create table
	def tblCreate(self, tbl, *cmd, force=0):
		"""
		Creates a Table.
		*cmd, describe Table for creation
		default - "ID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID)"
		force=0, Just Create (default)
		force=1, Drop and recreate
		"""
		if len(cmd) != 0 :
			values = self.__modTubs(*cmd)
		else:
			values = "ID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID)"
		if force == 1 :
			self.__exec("DROP TABLE", tbl)
		res = self.__exec( "CREATE TABLE",  "{} ({})".format(tbl, values))
		self.__debug("tblCreate: <{}> {}".format(tbl, res))
		return res

	# table drop
	def tblDrop(self, *tbl):
		"""
		Drops a Table(s)
		"""
		values = self.__modTubs(*tbl)
		res = self.__exec("DROP TABLE", values)
		self.__debug("tblDrop: <{}> {}".format(values, res))
		return res

	# alter table
	def tblAlter(self, tbl, *args):
		"""
		Alters Table
		"""
		values = self.__modTubs(*args)
		res = self.__exec("ALTER TABLE", "{} {}".format(tbl, values))
		self.__debug("tblAlter: <{}> {}".format(tbl, res))
		return res

	# select
	def select(self, select, tbl, *cmd):
		values = ""
		header = []
		for item in cmd:
			values += "{} ".format(item)
		res=self.__exec( "SELECT", "{} FROM {} {}".format(select, tbl, values))
		number_rows = self.__session.rowcount
		if self.__session.rowcount == 0 :
			self.__debug("select: <{}> {}".format(tbl, res))
			return res
		number_columns = len(self.__session.description)
		for item in self.__session.description:
			header.append(item[0])
		res = [header]
		for cnt in range(0,number_rows):
			item_x = []
			for x in self.__session.fetchone():
				item_x.append(x)
			res.append(item_x)
		self.__debug("select: <{}> len: {}".format(tbl, len(res)))
		return res
		# select Name from Summary union select Name from Customer;


	# INSERT
	def tblInsert(self, tbl, col, *args):
		values = self.__modTubsBrcks(*args)
		res = self.__exec("INSERT INTO", "{} ({}) VALUES {}".format(tbl, col, values))
		self.__connection.commit()
		self.__debug("tblInsert: <{}> {}".format(tbl, res))
		return res
		# tabInsertAdv
		# - List Array
		# - 1st Colums NO ""
		# - 2st values convert to -> ''


	#	[ 	[h1, h2, h3],
	#		[v1, v2, v3],
	#		[v1, v2, v3],
	#		...
	#	]
	def tblInsertArray(self, tbl, array, dtype=0):
		arr = array.copy()
		col = self.__modTubs(*arr[0])
		if dtype == 1 :
			arr.pop(1)
		values = ''
		cnt_y = 1
		for item_y in range(0, len(arr)-1):
			values += '('
			cnt_x = 1
			for item_x in arr[item_y+1]:
				values += "'{}'".format(item_x)
				if cnt_x != len(arr[item_y+1]):
					values += ", "
				cnt_x += 1
			values += ')'
			if cnt_y != len(arr)-1:
				values += ", "
			cnt_y += 1
		res = self.__exec("INSERT INTO", "{} ({}) VALUES {}".format(tbl, col, values))
		self.__connection.commit()
		self.__debug("tblInsertArray: <{}> {}".format(tbl, res))
		return res


	# tblCreateFromArrayH
	# [ 	[h1, h2, h3, ...],
	#		[d1, d2, d3, ...]
	# ]
	def tblCreateFromArrayH(self, tbl, arr, force=0):
		values = 'ID INT NOT NULL AUTO_INCREMENT,PRIMARY KEY (ID), '
		cnt = 1
		for x in range(0,len(arr[0])):
			values += "{} {}".format(arr[0][x], arr[1][x])
			if cnt != len(arr[0]):
				values += ", "
			cnt += 1
		if force == 1 :
			self.tblDrop(tbl)
		res = self.__exec( "CREATE TABLE",  "{} ({})".format(tbl, values))
		self.__debug("tblCreateFromArray: <{}> {}".format(tbl, res))
		return res
	# END tblCreateFromArrayH

	# tblCreateFromArrayV
	# [ [h1, d1],
	# 	[h2, d2],
	#	...
	# ]
	#
	def tblCreateFromArrayV(self, tbl, arr, force=0):
		values = 'ID INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID), '
		cnt = 1
		for x in range(0,len(arr)):
			values += "{} {}".format(arr[x][0], arr[x][1])
			if cnt != len(arr):
				values += ", "
			cnt += 1
		if force == 1 :
			self.tblDrop(tbl)
		res = self.__exec( "CREATE TABLE",  "{} ({})".format(tbl, values))
		self.__debug("tblCreateFromArray: <{}> {}".format(tbl, res))
		return res
	# END tblCreateFromArrayV

	# exec
	def exec(self, *args, list=0):
		values=''
		for item in args:
			values += ' ' + item
		res = self.__exec(values, '')
		self.__debug("exec: {}".format(res))
		return res
	# def update
	# update Summary set Last='Ting' where Last='jung';
	# tbl, change, condi
