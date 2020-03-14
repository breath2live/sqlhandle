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

######

# make database available
sql.dbUse("myDatabase", force=1)

# make clean table available, default with ID column
sql.tblCreate("myTable", "Name varchar(255)", "Last varchar(255)", force=1)
sql.tblAlter("myTable", "ADD Age INT")


# insert data from arrays
myHead = np.array(["Name", "Last", "Age"])
myData = np.array([["Nina", "Boodo", 34], ["Afft", "Loong", 27], ["Tom", "Hoogo", 46], ["Michi", "Fliffi", 12]])
myArray = np.row_stack([myHead, myData])


# head & headless array
sql.tblInsertArray("myTable", np.row_stack([myHead, myData]))
# headfull array
sql.tblInsertArray("myTable", myArray)


# working with dtype
#array([['Name', 'Last', 'Age'],
#       ['Name varchar(255)', 'Last varchar(255)', 'Age INT'],
#       ['Nina', 'Boodo', '34'],
#       ['Afft', 'Loong', '27'],
#       ['Tom', 'Hoogo', '46']], dtype='<U17')
myHead = np.array([["Name", "Last", "Age"], ["varchar(255)", "varchar(255)", "int"]])
myArray = np.row_stack([myHead, myData])
sql.tblInsertArray("myTable", myArray, dtype=1)


# create new table from array, axis=0
sql.tblCreateFromArray("tableAx0", myArray)
sql.tblCreateFromArray("tableAx1", np.transpose(myArray), axis=1)

# crete new table from array and insert data
sql.tblCreateFromArray("tableAx3", myArray, data=1)


# drop db, clean up
#sql.dbDrop("myDatabase")

######

# disconnect
sql.disconnect()
