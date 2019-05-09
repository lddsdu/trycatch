import pymysql

# connect mysql database
# MYSQLdb.connect("localhost", testuser", "test123", "testDB", charset='utf8')
db = pymysql.connect("localhost", "root", "abc", "trycatch", charset="utf8")
cursor = db.cursor()
cursor.execute("select VERSION()")
data = cursor.fetchone()
print "db version : %s " % data
db.close()

#create a table
db = pymysql.connect("localhost", "root", "abc", "trycatch", charset="utf8")
cursor = db.cursor()
cursor.execute("drop table if exists steaf")

sql = "create table steaf(" \
      "name varchar(100) NOT NULL," \
      "age int," \
      "sex char(1)," \
      "image_path varchar(200)," \
      "serialize_file varchar(200))"

cursor.execute(sql)
db.close()
print "create table done."

#insert some values
db = pymysql.connect("localhost", "root", "abc", "trycatch", charset="utf8")
cursor = db.cursor()

age = 20
image_path = "/home/jack/Desktop/target/lidongdong.jpg"
sql = "insert into steaf values(" \
      "'lidongdong'," \
      "%d," \
      "'m'," \
      "'%s'," \
      "'%s')" % (age, image_path, "")

try:
    cursor.execute(sql)
    db.commit()
except:
    print "error"
    db.rollback()

db.close()
print "insert data done."

#select
db = pymysql.connect("localhost", "root", "abc", "trycatch", charset="utf8")
cursor = db.cursor()

sql = "select * from steaf"
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        name = row[0]
        age = row[1]
        sex = row[2]
        image_path = row[3]
        serialize_file = row[4]
        print name, age, sex, image_path, serialize_file
except:
    print "error"
db.close()

print "select done."

