from sqlhandle import sqlhandle
import numpy as np
import pandas as pd


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

# force to use database
sql.dbUse("myDb", force=1)

# define array
myHeadFull = np.array([["Name", "Last", "Age"], ["varchar(255)", "varchar(255)", "int"]])
myData = np.array([["Nina", "Boodo", 34], ["Afft", "Loong", 27], ["Tom", "Hoogo", 46], ["Michi", "Fliffi", 12]])
myArray = np.row_stack([myHeadFull, myData])
sql.tblCreateFromArray("myTable", myArray, force=1, data=1)

######

print(sql.select("*", "myTable"))
print(sql.execute("select * from myTable"))

######

# drop db, clean up
#sql.dbDrop("myDatabase")

# disconnect
sql.disconnect()
