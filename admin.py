import time

from main import connect

cur , mydb = connect()


def ad_login ():
    ad_name = input("Enter your name : ").lower()
    ad_password = input("Enter password : ")
    cur.execute("select * from admin where admin = %s and password = %s;" , (ad_name,ad_password))
    res = cur.fetchall()
    if res :
        print("Login Successful for " , res)
        time.sleep(1)
        return True
    else:
        print("Login Failed !!")
        time.sleep(1)
        return False

def ad_add_teacher():
    teach_name = input("Enter teacher name : ").lower().strip()
    teach_id  = int(input("Enter teacher id : "))
    teach_pass = input("Enter teacher password : ").strip()
    cur.execute("select * from teacher where id = %s;" % teach_id)
    res = cur.fetchall()
    if res :
        print("Duplicate Found !!")
        print(res)
    else:
        cur.execute("insert into teacher values(%s,%s,%s);", (teach_id, teach_name, teach_pass))
        mydb.commit()
        print("Added !!")


def ad_remove_teacher():
    teach_id = int(input("Enter teacher id : "))
    cur.execute("select * from teacher where id = %s" % teach_id)
    res = cur.fetchall()
    if res :
        print("Teacher found !!")
        print("Removing ",res)
        cur.execute("delete from teacher where id = %s;" % teach_id)
        mydb.commit()
        time.sleep(2)
        print("Removed !!")
        time.sleep(1)
    else:
        print("Teacher not found in the Database !!")

