from sqlhandle.sqlhandle import sqlhandle

def showMe(str):
	print("[WorkFlow] {}".format(str))


# if docker available: docker run -it -e MYSQL_ROOT_PASSWORD=root -p3306:3306 mysql
# connect to database
sql = sqlhandle("127.0.0.1", password='root')


# test connection
if sql.isConnected() == True:
	showMe("connected")
else:
	showMe("not connected")
	exit(1)

# setDebug level=1 to True
sql.setDebug(level=0, value=True)

######

sql.dbUse("myDatabase", force=1)


# check if table is available
if sql.tblAvailable("table01") == True:
	showMe("Table is available")
else:
	showMe("Table is not available")


# make table available, default with ID column
sql.tblAvailable("table01", force=1)
sql.tblAvailable("tbl", "ID INT", "UID INT", force=1)


# create and drop table
sql.tblCreate("newTab")
sql.tblCreate("newTab", force=1)
sql.tblDrop("table01", "newTab")


# alter table
sql.tblAlter("tbl", "ADD col01 INT")


# insert INTO
sql.tblInsert("tbl", "ID, UID", "1, 2", "3, 4")


# drop db, clean up
#sql.dbDrop("myDatabase")

######

# disconnect
sql.disconnect()
