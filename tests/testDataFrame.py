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
sql.dbUse("historySTK", force=1)

# create table
sql.tblCreate("aapl", "date DATETIME NOT NULL UNIQUE PRIMARY KEY", "open FLOAT", "high FLOAT", "low FLOAT", "close FLOAT", force=0)

# create dataframe
df = pd.DataFrame(np.random.rand(40).reshape(10,4), pd.DatetimeIndex(np.random.randint(0,9999999999999999,10)), columns=['Open', 'High', 'Low', 'Close'])
df.index.name = 'date'
# insert data from DataFrame
sql.tblInsertDataFrame("aapl", df)


# create table from dataframe
dtype = ["DATETIME NOT NULL UNIQUE PRIMARY KEY", "FLOAT", "FLOAT", "FLOAT", "FLOAT"]
sql.tblCreateFromDataFrame("apple", df, dtype, data=1, force=1)


# read table
#print(sql.select("*", 'apple')[1:])
mydf = sql.tblReadToDataFrame(','.join(['Open', 'Close']), 'apple', index='')
print(mydf)

# drop db, clean up
#sql.dbDrop("myDatabase")

######

# disconnect
sql.disconnect()
