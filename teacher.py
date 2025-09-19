import time

from main import connect
cur , mydb = connect()

def login_teach(name , password):
    cur.execute("select * from teacher where teacher = %s and password = %s;",(name,password))
    res_log = cur.fetchall()
    if res_log :
        print("Login successful for : " , res_log)
        return True
    else :
        print("Login Failed")
        return False

def modify_mock_q() :

    q_num = int(input("Enter question number to update : "))
    print("You can ,\n1.update question text\n2.update option(A,B,C,D)\n3.update answer\n4.Exit")
    what_mod = input("What to change : ")

    if what_mod == "1":
        new_q = input("Enter new question : ")
        cur.execute("update mockup_q set question = %s where q_no = %s;" , (new_q,q_num))

    elif what_mod == "2":
        print("You can change ,\n1.option A\n2.Option B\n3.Option C\n4.Option D \n5.All the Option\n6.Exit")
        cho_mock = int(input("Enter you choice : "))
        if cho_mock >=1 and cho_mock<=4:
            option_mock = input("Enter option text to replace : ")
            if cho_mock == 1 :
                cur.execute("update mockup_q set A = %s where q_no = %s;", (option_mock, q_num))
            elif cho_mock == 2 :
                cur.execute("update mockup_q set B = %s where q_no = %s;", (option_mock, q_num))
            elif cho_mock == 3 :
                cur.execute("update mockup_q set C = %s where q_no = %s;", (option_mock, q_num))
            elif cho_mock == 4 :
                cur.execute("update mockup_q set D = %s where q_no = %s;", (option_mock, q_num))

        elif cho_mock == 5 :
            op_A = input("Enter A :")
            op_B = input("Enter B :")
            op_C = input("Enter C :")
            op_D = input("Enter D :")
            cur.execute("update mockup_q set A = %s , B = %s , C = %s , D = %s where q_no = %s;", (op_A,op_B,op_C,op_D, q_num))
        elif cho_mock == 6 :
            pass
        else :
            print("Invalid Choice !!")
            print("Try again !!")
            time.sleep(1)
    elif what_mod == "3":
        new_ans = input("Enter the new answer : ")
        cur.execute("update mockup_q set answer = %s where q_no = %s ;" , (new_ans,q_num))
    elif what_mod == "4" :
        pass
    else :
        print("Invalid choice !!\nTry Again !!")
    mydb.commit()




def modify_main_q():

    q_num = int(input("Enter question number to update : "))
    print("You can ,\n1.update question text\n2.update option(A,B,C,D)\n3.update answer\n4.Exit")
    what_mod = input("What to change : ")

    if what_mod == "1":
        new_q = input("Enter new question : ")
        cur.execute("update questions set question = %s where q_no = %s;" , (new_q,q_num))


    elif what_mod == "2":
        print("You can change ,\n1.option A\n2.Option B\n3.Option C\n4.Option D \n5.All the Option\n6.Exit")
        cho_main = int(input("Enter you choice : "))
        if cho_main >=1 and cho_main<=4:
            option_main = input("Enter option text to replace : ")
            if cho_main == 1 :
                cur.execute("update questions set A = %s where q_no = %s;", (option_main, q_num))
            elif cho_main == 2 :
                cur.execute("update questions set B = %s where q_no = %s;", (option_main, q_num))
            elif cho_main == 3 :
                cur.execute("update questions set C = %s where q_no = %s;", (option_main, q_num))
            elif cho_main == 4 :
                cur.execute("update questions set D = %s where q_no = %s;", (option_main, q_num))


        elif cho_main == 5 :
            op_A = input("Enter A :")
            op_B = input("Enter B :")
            op_C = input("Enter C :")
            op_D = input("Enter D :")
            cur.execute("update questions set A = %s , B = %s , C = %s , D = %s where q_no = %s;", (op_A,op_B,op_C,op_D, q_num))
            mydb.commit()
        elif cho_main == 6 :
            pass
        else :
            print("Invalid Choice !!")
            print("Try again !!")
            time.sleep(1)
    elif what_mod == "3":
        new_ans = input("Enter the new answer : ")
        cur.execute("update questions set answer = %s where q_no = %s ;" , (new_ans,q_num))
    elif what_mod == "4" :
        pass
    else :
        print("Invalid choice !!\nTry Again !!")
    mydb.commit()
    print("Done !!")


def view_teachers():
    number = 1
    cur.execute("select * from teacher;")
    res = cur.fetchall()
    if res:
        for i in res :
            print(number , i , sep=".")
            number += 1
        print("Done")
    else:
        print("None !!")


def modify_teacher():
    id = int(input("Enter teacher ID : "))
    cur.execute("select * from teacher where id = %s;" % id)
    teach = cur.fetchone()
    if teach:
        print("Teacher found !!")
        time.sleep(1)
        print(teach)
        time.sleep(1)
        print("1.Change Name\n2.Change ID\n3.Change password\n4.Exit")
        cho = input("Enter your choice : ")
        if cho == "1":
            new_name = input("Enter the new name : ").lower()
            cur.execute("update teacher set teacher = %s where id = %s;" , (new_name,id))
            mydb.commit()
            print("Done")
            time.sleep(1)
        elif cho == "2" :
            new_id = int(input("Enter new ID : "))
            cur.execute("update teacher set id = %s where id = %s;" , (new_id,id))
            mydb.commit()
            print("Done")
            time.sleep(1)
        elif cho == "3":
            new_pass = input("Enter new password : ")
            cur.execute("update teacher set password = %s where id = %s;" , (new_pass,id))
            mydb.commit()
            print("Done")
            time.sleep(1)
        elif cho == "4":
            pass
        else :
            print("Invalid choice !!")
        mydb.commit()

    else:
        print("Teacher not in system !!")

