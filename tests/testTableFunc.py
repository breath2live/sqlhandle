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

# make database available
sql.dbUse("myDatabase", force=1)

# make clean table available, default with ID column
sql.tblCreate("myTable", force=1)
sql.tblAlter("myTable", "ADD Name varchar(255)")




# drop db, clean up
#sql.dbDrop("myDatabase")

######

# disconnect
sql.disconnect()
