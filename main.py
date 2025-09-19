import datetime
import time



def connect():
    import mysql.connector as ms
    mydb = ms.connect(
        host="localhost",
        user="root",
        password="kiran@sql"
    )

    cur = mydb.cursor()
    cur.execute("create database if not exists EduQuiz_Portal;")
    cur.execute("use eduquiz_portal;")
    cur.execute("create table if not exists questions(q_no int , question text , A varchar(200) , B varchar(200) , C varchar(200) , D varchar(200) , answer char(1) , unique(q_no));")
    cur.execute("create table if not exists mockup_q(q_no int , question text , A varchar(200) , B varchar(200) , C varchar(200) , D varchar(200) , answer char(1) , unique(q_no));")

    cur.execute("create table if not exists admin(id int , admin text , password varchar(10), unique(id , password));")
    cur.execute("insert ignore into admin values(1 , 'founder chairman' , 'founder1') , (2 , 'principal' , 'principal1');")

    cur.execute("create table if not exists teacher(id int , teacher text , password varchar(10), unique(id , password));")
    cur.execute("create table if not exists student(id int , student text , age int , gender varchar(10) , grade varchar(5) , unique(id));")

    cur.execute("create table if not exists leaderboard(id int , student text , grade varchar(5) , correct_ans int , time float , date varchar(10), unique(id));")
    mydb.commit()
    return cur , mydb


def about_EduQuiz():
    print("="*40 )
    print(" "*10,"About EduQuiz System")
    print("="*40 )
    print("EduQuiz System is a simple quiz platform built to help students practice and test their knowledge.")
    print("Students can attempt mock quizzes\nor take the main quiz to enter the leaderboard.")
    print("Teachers can add and manage questions and students.")
    print("Admins manage teachers and system settings.")
    print("Note : There ONLY two admins privileges-The Principal and The founder chairman")
    print("=" * 40)
    time.sleep(5)


def leaderboard():
    cur , mydb = connect()
    cur.execute("select * from leaderboard order by correct_ans desc, time asc;")
    res = cur.fetchall()
    if res :
        print("Id , Name , Correct ans , Time Taken , Date(yyyy:mm:dd)")
        for i in res:
            print(i)
        time.sleep(3)
    else :
        print("None !!")
        time.sleep(1)

if __name__ == "__main__":
    connect()
    while True:

        print(10 * "-", "Welcome to EduQuiz System", "-" * 10)
        print(">> Who Are You ?\n1.Student\n2.Teacher\n3.Admin\n>> Other\n4.View Leaderboard\n5.About\n6.Exit")         # Main Menu
        cho = input("Enter your Choice : ")
        cur , mydb = connect()
        if cho == "1":
            #student
            print("New or returning\n1.Sign-in (New)\n2.Login (returning)")
            stu_who = input("Enter your choice : ")
            from student import who, remove_student, view_students, who_log

            if stu_who == "1":
                name_student, id_student, age_student, gender_student, grade_student = who()
            else:
                name_student,id_student = who_log()

            if stu_who == "1" :  # sign-in
                try:
                    cur.execute("insert into student values(%s,%s,%s,%s,%s);", (id_student, name_student,age_student,gender_student,grade_student))
                    mydb.commit()
                    print("Hello " , name_student , " ,you have been added to our system !!")
                except:
                    print("Duplicate Found !\nINVALID !")
                    time.sleep(5)
                    print("Retry")
                    continue

            elif stu_who == "2": # log-in
                try :
                    cur.execute("select * from student where id = %s and student = %s;" , (id_student,name_student))
                    result_login = cur.fetchall()
                    if result_login :
                        print("Welcome back" , name_student , "!!")
                        time.sleep(1)
                    else :
                        print("You are not in out system \nKindly sign-in first !!")
                        time.sleep(1)
                        continue
                except :
                    print("Something's Wrong , must be from us !!\nKindly retry !!")
                    pass
            elif stu_who == "3" :
                print("Good bye !!")
                break


            #mockup or main quiz
            print("Do you want a mockup quiz or enter the main quiz.")
            print("Note : Results from mockup WILL NOT be uploaded into the leaderboard")
            print("1.Mockup Quiz\n2.Main Quiz\n3.About\n4.View Leaderboard\n5.Quit")
            chostu = input("Enter your choice : ")

            if chostu == "1": # Mockup Quiz
                #mockup
                mock_mark=0
                print("Here comes the mockup quiz , GET READY !!",name_student, end=" ")
                for i in range(6):
                    time.sleep(1)
                    print("." , end=" ")
                cur.execute("select * from mockup_q;")
                from Question import mockup
                from teacher import modify_mock_q

                start_mock = time.time()
                for i in cur.fetchall():
                    mock_mark += mockup(i)
                end_mock = time.time()
                print("Your mockup mark is : " , mock_mark )
                print("And mock up time taken is : " , round(end_mock - start_mock,2) , " Seconds")
                time.sleep(3)

            elif chostu == "2": # Main Quiz
                main_mark = 0
                print("Get Ready for the EduQuiz\nGood Luck !!" , end=" ")
                for i in range(6):
                    time.sleep(1)
                    print("." , end=" ")
                print()
                cur.execute("select * from questions;")
                from Question import quiz

                start_quiz_time = time.time()
                for q in cur.fetchall():
                    main_mark += quiz(q)
                end_quiz_time = time.time()
                time_main = round(end_quiz_time - start_quiz_time,2)
                date = datetime.date.today()
                print("Your Quiz mark is : ", main_mark)
                print("And time taken is : ", time_main, " Seconds")
                time.sleep(1)
                cur.execute("select * from student where id = %s;" , (id_student,))
                gr = cur.fetchone()
                grade = gr[4]
                # insert into leaderboard , if not present
                try:
                    cur.execute("insert into leaderboard values (%s,%s,%s,%s,%s,%s);", (id_student, name_student , grade , main_mark, time_main, date))
                    mydb.commit()
                    print("Your record has been placed on the Leaderboard !!")
                except :
                    # If present , check if past record better that present one
                    time.sleep(1)
                    from student import better
                    if better(id_student,main_mark,time_main):
                        cur.execute("delete from leaderboard where id = %s;" , (id_student,))
                        cur.execute("insert into leaderboard values (%s,%s,%s,%s,%s,%s);",(id_student, name_student, grade, main_mark, time_main, date))
                        mydb.commit()
                        print("Your record has been updated !!")
                        time.sleep(1)
                    else:
                        print("Since your previous record is better that this , this score will not be considered !!")
                        print("Try harder next time !! ")
                        time.sleep(2)


            elif chostu == "3":  # about eduquiz
                about_EduQuiz()
                time.sleep(4)
            elif chostu == "4":  # displays leaderboard
                leaderboard()
                time.sleep(4)
            elif chostu == "5":
                pass
            else :
                print("Invalid choice !!")
                time.sleep(3)


         #Teacher
        elif cho == "2":
            from teacher import login_teach, view_teachers, modify_teacher

            if login_teach(input("Enter your name : "), input("Enter your password : ")) :
                time.sleep(1)
                print("What are your intentions ?")
                print("1.update Mock up question\n2.Update Main Quiz\n3.Modify Students\n4.View all Students\n5.View LeaderBoard\n6.Exit")
                choteach = input("Enter you choice : ")

                if choteach == "1":
                    print("1.Add question\n2.Remove Question\n3.Modify\n4.Exit")
                    choteach1 = input("Enter your choice : ")

                    if choteach1 == "1":
                        qmockno = int(input("Enter question number : "))
                        qmockq = input("Enter Question to add : ")
                        qmockop = list(input("Enter all the 4 option comma seperated : "))
                        qmockans = input("Enter the correct option : ")
                        cur.execute("insert into mockup_q values (%s,%s,%s,%s,%s,%s,%s);" , (qmockno , qmockq , qmockop[0] , qmockop[1] , qmockop[2] , qmockop[3] , qmockans))
                        mydb.commit()
                        print("Done")
                        time.sleep(1)

                    elif choteach1 == "2":
                        qmockrem = int(input("Enter question number to remove : "))
                        cur.execute("delete from mockup_q where q_no = %s" % qmockrem)
                        mydb.commit()
                        print("Done")
                        time.sleep(1)
                    elif choteach1 == "3":
                        from teacher import modify_mock_q
                        modify_mock_q()

                    elif choteach1 == "4":
                        pass
                    else:
                        print("Invalid choice")
                        time.sleep(2)


                elif choteach == "2":
                    print("1.Add question\n2.Remove Question\n3.Modify Question\n4.Exit")
                    choteach1 = input("Enter your choice : ")
                    if choteach1 == "1":
                        qmaino = int(input("Enter question number : "))
                        qmainq = input("Enter Question to add : ")
                        qmainop = list(input("Enter all the 4 option comma separated : ").split(","))
                        qmainans = input("Enter the correct option : ")
                        cur.execute("insert into questions values (%s ,%s,%s,%s,%s,%s,%s );" , (qmaino , qmainq , qmainop[0] , qmainop[1] , qmainop[2] , qmainop[3] , qmainans))
                        mydb.commit()
                        print("Done")
                        time.sleep(1)

                    elif choteach1 == "2":
                        qmainrem = int(input("Enter question number to remove : "))
                        cur.execute("delete from questions where q_no = %s" % qmainrem)
                        mydb.commit()
                        print("Done")
                        time.sleep(1)

                    elif choteach1 == "3":
                        from teacher import modify_main_q
                        modify_main_q()
                    elif choteach1 == "4" :
                        pass
                    else:
                        print("Invalid choice")
                        time.sleep(2)

                elif choteach == "3":
                    print(">> since students can sign-in by themself, no add student.\n1.Remove Student\n2.Modify Student")
                    stu_mod_cho = input("Enter you choice : ")
                    if stu_mod_cho == "1":
                        from student import remove_student
                        remove_student()
                    elif stu_mod_cho == "2":
                        from student import modify_student
                        modify_student()

                elif choteach == "4":
                    from student import view_students
                    view_students()
                    time.sleep(1)

                elif choteach == "5":
                    leaderboard()

                elif choteach == "6":
                    pass
                else:
                    print("Invalid choice")

            else:
                print("Access Denied !!")


        elif cho == "3":
            from admin import ad_login

            if ad_login():

                print("What is your intention ?\n1.Update\n2.View\n3.Reset Leaderboard\n4.Exit")
                ad_cho = input("Enter Your choice : ")
                if ad_cho == "1":
                    print("1.Student\n2.Teacher\n3.Exit")
                    ad_cho1 = input("Enter choice : ")
                    if ad_cho1 == "1":
                        print("1.Add Student\n2.Remove student\n3.Modify Students\n4.Exit")
                        ad_cho2 = input("Enter choice : ")
                        if ad_cho2 == "1":
                            print("Student can enter from the student menu !!")
                            time.sleep(1)
                        elif ad_cho2 == "2":
                            from student import remove_student
                            remove_student()
                        elif ad_cho2 == "3":
                            from student import modify_student
                            modify_student()
                        elif ad_cho2 == "4":
                            pass
                        else:
                            print("Invalid choice !!")

                    elif ad_cho1 == "2":
                        print("1.Add Teacher\n2.Remove Teacher\n3.Modify Teacher\n4.Exit")
                        ad_cho3 = input("Enter choice : ")
                        if ad_cho3 == "1":
                            from admin import ad_add_teacher
                            ad_add_teacher()
                        elif ad_cho3 == "2":
                            from admin import ad_remove_teacher
                            ad_remove_teacher()
                        elif ad_cho3 == "3":
                            from teacher import modify_teacher
                            modify_teacher()
                        elif ad_cho3 == "4":
                            pass
                        else:
                            print("Invalid choice !!")

                    elif ad_cho1 == "3":
                        pass

                elif ad_cho == "2":
                    print("1.View Students\n2.View Teachers\n3.Exit")
                    ad_cho4 = input("Enter choice : ")
                    if ad_cho4 == "1":
                        from student import view_students
                        view_students()
                        time.sleep(1)

                    elif ad_cho4 == "2":
                        from teacher import view_teachers
                        view_teachers()
                        time.sleep(1)

                    elif ad_cho4 == "3":
                        pass

                    else:
                        print("Invalid choice !!")
                        time.sleep(1)

                elif ad_cho == "3":
                    time.sleep(1)
                    print("Are you sure to reset the leaderboard")
                    sure = input("1.Yes\n2.No\nEnter choice : ")

                    if sure == "1":
                        cur.execute("delete from leaderboard;")
                        mydb.commit()
                        print("DONE !!")
                        time.sleep(1)

                    elif sure == "2":
                        print("Leaderboard Reset Cancel !!")
                        time.sleep(1)
                    else:
                        print("Invalid choice !!")
                        pass
                elif ad_cho == "4":
                    pass

                else:
                    print("Invalid choice !!")
                    time.sleep(1)

            else:
                print("Access Denied !!")
                continue


        elif cho == "4":
            leaderboard()

        elif cho == "5" :
            about_EduQuiz()

        elif cho == "6":
            print("See Ya !!!")
            break

        else :
            print("Invalid choice !!")
            time.sleep(3)

