import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="hisham"
)

mycursor = mydb.cursor()

# sql = "ALTER TABLE diary CHANGE COLUMN content content VARCHAR(10000);"
#
# mycursor.execute(sql)
#
#
#
# print(mycursor.rowcount, "record(s) deleted")

mycursor.execute("SELECT * FROM diary")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)


# #
# sql = "INSERT INTO userdata( name,username,email,password,phone) VALUES (%s, %s, %s, %s, %s)"
# val = ( "hisham" , "hisham123" , "hisham@gmail.com", "hisham321", "8606775510")
# mycursor.execute(sql, val)
# #
mydb.commit()

# print(mycursor.rowcount, "record inserted.")
