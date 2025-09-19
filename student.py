import time

from main import connect

cur , mydb = connect()

def who():
    name = input("Enter your name : ").lower().strip()
    id = int(input("Enter your id : "))
    age = int(input("Enter you age : "))
    gender = None
    gr = input("1.Male\n2.Female\n3.Other\nEnter you gender : ")
    if gr == "1":
        gender = "Male"
    elif gr == "2":
        gender = "Female"
    elif gr == "3":
        gender = "Other"
    else:
        print("Invalid choice !!")
        breakpoint()
    grade = input("Enter your grade : ")
    return name , id , age , gender , grade

def who_log():
    name = input("Enter your name : ").lower().strip()
    id = int(input("Enter your id : "))
    return name, id

def remove_student():
    id = input("Enter student ID : ")
    cur.execute("delete from student where id = %s ;" % id)
    mydb.commit()
    print("Done")
    time.sleep(1)

def modify_student():
    id = int(input("Enter student ID : "))
    cur.execute("select * from student where id = %s;" % id)
    stu = cur.fetchall()
    if stu:
        print("Student found !!")
        time.sleep(1)
        print(stu)
        time.sleep(1)
        print("1.Change Name\n2.Change ID\n3.Change gender\n4.Change Age\n5.Change Grade\n6.Exit")
        cho = input("Enter your choice : ")
        if cho == "1":
            new_name = input("Enter the new name : ").lower()
            cur.execute("update student set student = %s where id = %s;" , (new_name,id))
            mydb.commit()
            print("Done")
            time.sleep(1)
        elif cho == "2" :
            new_id = int(input("Enter new ID : "))
            cur.execute("update student set id = %s where id = %s;" , (new_id,id))
            mydb.commit()
            print("Done")
            time.sleep(1)
        elif cho == "3":
            print("Gender\n1.Male\n2.Female\n3.Other")
            new_gender = input("Enter choice : ")
            print("Done !!")
            time.sleep(1)
            if new_gender == "1":
                cur.execute("update student set gender = male where id = %s;" , (id,))
                mydb.commit()
            elif new_gender == "2":
                cur.execute("update student set gender = female where id = %s;" , (id,))
                mydb.commit()
            elif new_gender == "3":
                cur.execute("update student set gender = other where id = %s;" , (id,))
                mydb.commit()
            else:
                print("Invalid choice !!")
                time.sleep(1)
                pass

        elif cho == "4":
            new_age = int(input("Enter the new age : "))
            cur.execute("update student set age = %s where id = %s;" , (new_age,id))
            mydb.commit()
            print("Done !!")
            time.sleep(1)

        elif cho == "5":
            new_grade = input("Enter new grade : ")
            cur.execute("update student set grade = %s where id = %s;" , (new_grade,id))
            mydb.commit()
            print("Done !!")
            time.sleep(1)

        elif cho == "6":
            pass
        else :
            print("Invalid choice !!")
            time.sleep(1)
        mydb.commit()

    else:
        print("Student not present in Database !!")
        time.sleep(1)

def view_students():
    number = 1
    cur.execute("select * from student;")
    res = cur.fetchall()
    if res:
        for i in res :
            print(number , i , sep=".")
            number += 1
        print("Done")
    else:
        print("None Found !!")


def better(id,new_mark,new_time):
    cur.execute("select * from leaderboard where id = %s;" , (id,))
    old_rec = cur.fetchone()
    old_mark = int(old_rec[3])
    old_time = float(old_rec[4])
    if new_mark >= old_mark and new_time <= old_time:
            return True
    else:
        return False

