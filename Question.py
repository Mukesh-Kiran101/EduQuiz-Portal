from main import connect
cur , mydb = connect()
def mockup(q):
    print("Questions")
    print(q[0],".",q[1])
    print("A.%s\nB.%s\nC.%s\nD.%s" % (q[2],q[3],q[4],q[5]))
    stu_ans = input("Enter your answer : ").lower()
    if stu_ans.lower() == q[6] or stu_ans.upper() == q[6] :return 1
    else : return 0

'''def quiz(q):
    print(q[0],".",q[1])
    print("A.%s\nB.%s\nC.%s\nD.%s" % (q[2],q[3],q[4],q[5]))
    stu_ans = input("Enter your answer : ")
    if stu_ans.lower() == q[6] or stu_ans.upper() == q[6] :return 1
    else : return 0'''

def quiz(q):
    print(q[0],".",q[1])
    print("A.%s\nB.%s\nC.%s\nD.%s" % (q[2],q[3],q[4],q[5]))
    stu_ans = input("Enter your answer : ")
    if stu_ans.lower() == q[6] or stu_ans.upper() == q[6] :return 1
    else : return 0

