# Introduction
This is a simple sql handle for python

# How to import
from sqlhandle import sqlhandle

# Test Directory
Here you can find scripts, how to use the sqlhandle.

- Methods for internal use or basic stuff
- Methods for Database
- Methods for Table
- Methods and functions for Tables, like insert Array to Table
- A lot more easy methods


# Ideas, What I need, and Good to have

## Insert or Create Table from a DataFrame
df.as_matrix() -> for Data
df.columns.to_list() -> for Head
How could i structure and save the dType? dtype row?

df1 = pd.DataFrame([["var","var","var","int"]], index=["sqlType"], columns=df.columns.to_list())

df1
Out[46]:
           W    X    Y    Z
sqlType  var  var  var  int

df.append(df1)
Out[47]:
                W         X         Y         Z
A         2.70685  0.628133  0.907969  0.503826
B        0.651118 -0.319318 -0.848077  0.605965
C        -2.01817  0.740122  0.528813 -0.589001
D        0.188695 -0.758872 -0.933237  0.955057
E        0.190794   1.97876   2.60597  0.683509
sqlType       var       var       var       int
