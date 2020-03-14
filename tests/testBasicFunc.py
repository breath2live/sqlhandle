from sqlhandle import sqlhandle

# if docker available: docker run -it -e MYSQL_ROOT_PASSWORD=root -p3306:3306 mysql

# connect to database
sql = sqlhandle("127.0.0.1", password='root')


# test connection
if sql.isConnected() == True:
	print("connected")
else:
	print("not connected")


# setDebug level=1 to True
sql.setDebug(level=0, value=True)
sql.setDebug(level=1, value=True)

# disconnect
sql.disconnect()

# connect agian
sql.connect()

# execute command
sql.execute("CREATE DATABASE", "HelloWorld")
