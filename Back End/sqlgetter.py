import mysql.connector
from mysql.connector import FieldType

def createConnection(): #returns a connector for mydatabase
    return mysql.connector.connect(
    host="lovelacecis2368db.cmaiyhlrrtwz.us-east-1.rds.amazonaws.com",
    user="admin",
    password="AISDdbpassword",
    database="LovelaceCIS2368DB",
    port=3306
)

def insert(connection:mysql.connector ,table:str, values, primarykey="id"): #designed to be able to insert new rows into any give table on the connected database without issue
    columnname = []
    columntype = []
    columnnull = []
    cursor = connection.cursor()
    cursor.execute("select * from " + table)
    info = cursor.description # used to find the names, data types and if it is required for each columnm I found out about this on stackoverflow https://stackoverflow.com/questions/5010042/mysql-get-column-name-or-alias-from-query
    cursor.fetchall()# this clears up the connection for the next use otherwise causes an error
    insertstring = "("
    valuesstring = "("
    for i in info:
        if i[0] != primarykey: #designed to skip the primary key because we usually use auto generated if primary key is needed to be inserted changing the value primarykey id
            columnname.append(i[0])
            columntype.append(FieldType.get_info(i[1]))#this takes the numerical value for an type and turns it into a string a person can understand, i found this on the mysql documentation https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-description.html
            columnnull.append(bool(i[6]))
    for i in range(len(columnname)):
        if(columnname[i] in values or columnnull[i]):#creates group of the order the values are inserted and the group of the inserted values
            insertstring += ((int(i != 0) * ",") + columnname[i])
            valuesstring += ((int(i != 0) * ",") + (int(columntype[i] == 'VAR_STRING') * '"') +values[columnname[i]] + (int(columntype[i] == 'VAR_STRING') * '"')) #will add quation marks around values that are intented to be strings
        else:
            raise  Exception("Missing a required vlue")
    insertstring += ")"
    valuesstring += ")"
    cursor.execute(f"insert into {table} {insertstring} values {valuesstring};")
    connection.commit()
    
def querry(connection:mysql.connector, table:str, Select="*", Where=None, Orderby=None):#desinged to make querry databases easier allows for order by and where and defaults the select statment to *
    cursor = connection.cursor(dictionary=True)
    qstring = "Select " + Select +" from " + table
    if(Where != None):
        qstring += " Where " + Where
    if(Orderby != None):
        qstring += " Order by " + Orderby
    qstring += ";"
    cursor.execute(qstring)
    return cursor.fetchall()

def update(connection,table,set,where):
    cursor = connection.cursor()
    cursor.execute(f"update {table} set {set} where {where}")
    connection.commit()

def remove(connection, table, where):
    cursor = connection.cursor()
    cursor.execute(f"delete from {table} where {where}")
    connection.commit()
