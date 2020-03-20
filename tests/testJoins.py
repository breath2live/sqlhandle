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
sql.setDebug(level=1, value=True)

######

# make database available
sql.dbUse("myDatabase", force=1)

# make clean table available, default with ID column
sql.tblCreate("myTable1", "conId INT unique", "symbol varchar(255)", 'strike int', force=0)
sql.tblCreate("myTable2", "conId INT unique", "symbol varchar(255)", 'strike int', force=0)


# insert data from arrays
myHead = np.array(["conId", "symbol", "strike"])
myData1 = np.array([[401479054, "aaa", 34], [401339057, "bbb", 27], [401759007, "ccc", 46], [401479073, "ddd", 12]])
myData2 = np.array([[40147912, "aaa", 47], [401339057, "bbb", 27], [401759457, "ccc", 70], [401467586, "ddd", 55]])

myArray1 = np.row_stack([myHead, myData1])
myArray2 = np.row_stack([myHead, myData2])


# head & headless array
sql.tblInsertArray("myTable1", myArray1)
sql.tblInsertArray('myTable2', myArray2)
# INSERT IGNORE INTO myTable1 (conId, symbol, strike) VALUES ('40147912', 'aaa', '47'), ('401339057', 'bbb', '27'), ('401759457', 'ccc', '70'), ('401467586', 'ddd', '55');




# drop db, clean up
#sql.dbDrop("myDatabase")

######

# disconnect
sql.disconnect()
