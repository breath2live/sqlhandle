from sqlhandle import sqlhandle

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

# check if available
if sql.dbAvailable("myDatabase") == True:
	showMe("myDatabase is available")
else:
	showMe("myDatabase is not available")

# forcing to make it available
sql.dbAvailable("myDatabase", force=1)

# create db
sql.dbCreate("myDatabaseNew")
# force it, -> drop -> create
sql.dbCreate("myDatabase", force=1)

# use db if available
sql.dbUse("myDatabase")
# create if not available
sql.dbUse("myDatabaseNewer", force=1)
# drop and recreate if available
sql.dbUse("myDatabaseNewer", force=2)

# drop db, clean up
sql.dbDrop("myDatabase")
sql.dbDrop("myDatabaseNew")
sql.dbDrop("myDatabaseNewer")

######

# disconnect
sql.disconnect()
