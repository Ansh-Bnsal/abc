#PROJECT
#BANK DBMS


#PART 1 OPENING BANK DATABASE
import mysql.connector as m
a=input('Enter your MySQL password: ') #abcdefg
con=m.connect(host="localhost", user="root", password=a)
c=con.cursor()
bank=input("Enter bank name (Use '_' instead of ' '):")
c.execute("Show Databases")
r=c.fetchall()
for i in r:
    if i[0] == bank:
        c.execute("Use "+bank)
        print(bank, "Database Opened.")
        break
else:
    c.execute("Create Database "+bank)
    c.execute("Use "+bank)
    print("Bank Database Created and Opened.")
print("*****************************************************************************")
print("Welcome to",bank,"Database")

#PART 2 CREATING TABLES

def C_TABLE():
    try:
        c.execute("Create Table Customer (Cust_ID char(8) primary key, Cust_Name varchar(20) not null, Cust_Address varchar(50), Cust_PNo integer(11), L_ID char(5), B_ID char(4) )")
        print("The Customer Table with following Fields has been Created.")
        print("1) Cust_ID")
        print("2) Cust_Name")
        print("3) Cust_Address")
        print("4) Cust_PNo")
        print("5) L_ID")
        print("6) B_ID")
        print("To add or delete a column, refer MAIN MENU.")
    except:
        print("Technical Error.. Table Cannot be Created.")

def A_TABLE():
    try:
        c.execute("Create Table Accounts (Acc_No integer(8) primary key, Cust_ID char(8) not null, Acc_Type char(1) , Opening_Date date, Amount float not null )")
        print("The Accounts Table with following Fields has been Created.")
        print("1) Acc_No")
        print("2) Cust_ID")
        print("3) Acc_Type")
        print("4) Opening_Date")
        print("5) Amount")
        print("To add or delete a column, refer MAIN MENU.")
    except:
        print("Technical Error.. Table Cannot be Created.")

def B_TABLE():
    try:
        c.execute("Create Table Branch (B_ID char(4) primary key, B_Name  varchar(20) not null, Location  varchar(50) )")
        print("The Branch Table with following Fields has been Created.")
        print("1) B_ID")
        print("2) B_Name")
        print("3) Location")
        print("To add or delete a column, refer MAIN MENU.")
    except:
        print("Technical Error.. Table Cannot be Created.")

def L_TABLE():
    try:
        c.execute("Create Table Loans (L_ID char(5) primary key, Cust_ID char(8) not null, L_Type char(1), L_Amount integer )")
        print("The Loans Table with following Fields has been Created.")
        print("1) L_ID")
        print("2) Cust_ID")
        print("3) L_Type")
        print("4) L_Amount")
        print("To add or delete a column, refer MAIN MENU.")
    except:
        print("Technical Error.. Table Cannot be Created.")

def CREATE_TABLE(table):
    try:
        n=int(input("Enter number of columns:"))
        count=0
        for i in range(n):
            cname=input("Enter Column Name:")
            datatype=input("Enter Datatype:")
            constraint=input("Enter Constraint,if any. To skip press enter key:")
            count+=1
            if count==1:
                if constraint == None:
                    c.execute("Create table {} ({} {})".format(table,cname,datatype))
                else:
                    c.execute("Create table {} ({} {} {})".format(table,cname,datatype,constraint))
            elif count>1:
                if constraint == None:
                    c.execute("Alter table {} add ({} {})".format(table,cname,datatype))
                else:
                    c.execute("Alter table {} add ({} {} {})".format(table,cname,datatype,constraint))
        print("Table has been Created.")
    except:
        print("Technical Error.. Table Cannot be Created.")

#PART 3 OPERATIONS ON RECORDS

def INSERT_RECORD(table):
    try:
        c.execute("desc "+table)
        r=c.fetchall()
        n=int(input("Enter number of rows to be inserted:"))
        l,t=list(),tuple()
        for i in range(n):
            print("Values for",i+1,"Record")
            print('*'*40)
            print()
            for j in r:
               N=j[0]
               a=input("Enter value for {}:".format(N))
               if type(a) in (int,float):
                   a=eval(a)
               t+=(a,)
            l+=[t]
            print(l)
            t=tuple()
        for x in l:
                c.execute("insert into {} values {}".format(table,x))
                con.commit()
        print("Data has been Inserted.")
    except:
        con.rollback()
        print("Technical Error.. Data Cannot be Inserted.")

def DISPLAY_RECORDS(table):
    try:
        c.execute("desc "+table)
        r=c.fetchall()
        for i in r:
            print(i[0],end='\t\t')
        print()
        print('__'*45)
        c.execute("select * from "+table)
        r=c.fetchall()
        for i in r:
            for j in i:
                print(str(j),end='\t\t')
            print()
    except:
        print("Technical Error.. Data Cannot  be Fetched.")

    '''try:
        c.execute("select * from "+table)
        r=c.fetchall()
        for i in r:
            print(i)
    except:
        print("Technical Error.. Data Cannot  be Fetched.")'''

def SEARCH_RECORD(table):
    try:
        c.execute("desc "+table)
        r=c.fetchall()
        column=""
        for i in r:
            if i[3].lower()=="pri":
                column=i[0]
        v=input("Enter value for the %s column whose record is to be searched: "%(column))
        if v.isdigit():
            v=eval(v)
            c.execute("select * from %s where %s = %s"%(table,column,v))
        else:
            v=str(v)
            c.execute("select * from %s where %s = '%s'"%(table,column,v))
        r1=c.fetchone()
        print(r1)
    except:
        print("Technical Error.. Data Cannot be Fetched.")

def UPDATE_RECORD(table):
    try:
        c.execute("desc "+table)
        r=c.fetchall()
        print("Select column from following list:")
        for i in r:
            print(i[0])
        sc=input("Enter Column name by which you want to update the record(s):")
        sr=input("Enter value(s) for that column:")
        uc=input("Enter Column name whose value is to be updated:")
        nv=input("Enter new value for that column:")
        sr=sr.split(",")
        if len(sr)>1:
            sr=tuple(sr)
            sr1=tuple()
            for i in sr:
                if i.isdigit():
                    sr1+=(float(i),)
                else:
                    sr1+=(i,)
            sr=sr1
            if nv.isdigit():
                nv=eval(nv)
                c.execute("update {} set {} = {} where {} in {}".format(table,uc,nv,sc,sr))
            else:
                nv=str(nv)
                c.execute("update {} set {} = '{}' where {} in {}".format(table,uc,nv,sc,sr))
        else:
            sr="".join(sr)
            if nv.isdigit() and sr.isdigit():
                nv,sr=eval(nv),eval(sr)
                c.execute("update {} set {} = {} where {} = {}".format(table,uc,nv,sc,sr))
            elif nv.isdigit() or sr.isdigit():
                if nv.isdigit():
                    nv,sr=eval(nv),str(nv)
                    c.execute("update {} set {} = {} where {} = '{}'".format(table,uc,nv,sc,sr))
                else:
                    nv,sr=str(nv),eval(sr)
                    c.execute("update {} set {} = '{}' where {} = {}".format(table,uc,nv,sc,sr))
            else:
                nv,sr=str(nv),str(sr)
                c.execute("update {} set {} = '{}' where {} = '{}'".format(table,uc,nv,sc,sr))
        con.commit()
        print("Records have been Updated")
    except:
        con.rollback()
        print("Technical Error.. Data Cannot Be Updated.")

def ADD_RECORD(table):
    try:
        c.execute("desc "+table)
        n_c=0
        for i in c:
            n_c+=1
        t=tuple()
        for j in range(n_c):
           a=input("Enter value:")
           if type(a) in (int,float):
               a=float(a)
           t+=(a,)
        for x in l:
            c.execute("insert into {} values {}".format(table,x))
            con.commit()
        print("Record has been Added..")
    except:
        con.rollback()
        print("Technical Error.. Record Cannot be Added.")

def DELETE_RECORD(table):
    try:
        c.execute("desc "+table)
        r=c.fetchall()
        print("Select column from following list:")
        for i in r:
            print(i[0])
        dc=input("Enter Column name whose entered value's record will be deleted:")
        dr=input("Enter value(s) from selected column whose record is to be deleted:")
        dr=dr.split(",")
        if len(dr)>1:
            dr=tuple(dr)
            c.execute("delete from {} where {} in {}".format(table,dc,dr))
        else:
            dr="".join(dr)
            if dr.isdigit():
                dr=eval(dr)
                c.execute("delete from {} where {} = {}".format(table,dc,dr))
            else:
                dr=str(dr)
                c.execute("delete from {} where {} = '{}'".format(table,dc,dr)) 
        con.commit()
        print("Data has been Deleted.")
    except:
        con.rollback()
        print("Technical Error.. Data Cannot be Deleted.")

def NO_RECORDS(table):
    try:
        
        print("Number of records in",table,": ",c.rowcount)
    except:
        print("Technical Error.. Total Number of Records Cannot be Fetched.")

#PART 4 SORTING AND FILTERING

def SORT_ASC(table):
    try:
        s_c=input("Enter name of column by which you want to sort the table:")
        c.execute("select * from {} order by {}".format(table,s_c))
        r=c.fetchall()
        for i in r:
            print(i)
    except:
        print("Technical Error.. Data Cannot be Fetched.")

def SORT_DESC(table):
    try:
        s_c=input("Enter name of column by which you want to sort the table:")
        c.execute("select * from {} order by {} desc".format(table,s_c))
        r=c.fetchall()
        for i in r:
            print(i)
    except:
        print("Technical Error.. Data Cannot be Fetched.")
        
def FILTER_RECORD(table):
    try:
        c.execute("desc "+table)
        r=c.fetchall()
        print("Select column from following list:")
        for i in r:
            print(i[0])
        sc=input("Enter Column name whose entered value's record is to be searched:")
        sr=input("Enter ',' separated value(s) from selected column whose record is to be searched:")
        sr=sr.split(",")
        if len(sr)>1:
            sr=tuple(sr)
            c.execute("select * from {} where {} in {}".format(table,sc,sr))
        else:
            sr="".join(sr)
            if sr.isdigit():
                sr=eval(sr)
                c.execute("select * from %s where %s = %s"%(table,sc,sr))
            else:
                sr=str(sr)
                c.execute("select * from %s where %s = '%s'"%(table,sc,sr))
        r1=c.fetchall()
        for x in r1:
            print(x)
    except:
        print("Technical Error.. Data Cannot be Fetched.")

#PART 5 MODIFICATIONS IN TABLE STRUCTURE

def ADD_COLUMN(table):
    try:
        cname=input("Enter Column Name:")
        datatype=input("Enter Datatype:")
        constraint=input("Enter Constraint,if any. To skip press enter key:")
        if constraint == None:
            c.execute("Alter table {} add ({},{})".format(table,cname,datatype))
        else:
            c.execute("Alter table {} add ({},{},{})".format(table,cname,datatype,constraint))
        print("Column has been Added.")
    except:
        print("Technical Error.. Column Cannot be Added.") 
 
def DELETE_COLUMN(table):
    try:
        cname=input("Enter Column Name:")
        c.execute("desc "+table)
        r=c.fetchall()
        for i in r:
            if i[0] == cname:
                c.execute("Alter table {} drop {}".format(table,cname))
                print("Column has been Deleted.")
                break
        else:
            print("Column doesnot exists.")
    except:
        print("Technical Error.. Column Cannot be Deleted.") 
       
def NAME_COLUMN(table):
    try:
        c.execute("desc "+table)
        r=c.fetchall()
        cname=input("Enter Column Name to be changed:")
        nname=input("Enter New Column Name:")
        for i in r:
            if cname == i[0]:
                datatype=i[1]
                print(datatype)
        constraint=input("Enter Constraint,if any. To skip press enter key:")   
        if constraint == None:
            c.execute("Alter table {} change {} {} {}".format(table,cname,nname,datatype))
        else:
            c.execute("Alter table {} change {} {} {} {}".format(table,cname,nname,datatype,constraint))
        print("Column Name has been changed.")
    except:
       print("Technical Error.. Column name cannot be changed.. ")
       
def MODIFY_COLUMN(table):
    try:
        cname=input("Enter Column Name:")
        datatype=input("Enter changed datatype:")
        constraint=input("Enter new Constraint,if any. To skip press enter key:") 
        c.execute("desc "+table)
        r=c.fetchall()
        for i in r:
            if cname == i[0]:
                if constraint == None:
                    c.execute("Alter table {} modify {} {} {}".format(table,cname,nname,datatype))
                    print("Column definition has changed.")
                    break
                else:
                    c.execute("Alter table {} modify {} {} {} {}".format(table,cname,nname,datatype,constraint))
                    print("Column definiton has changed.")
        else:
            print("Column doesnot exists..")
    except:
       print("Technical Error.. Column definiton cannot be Changed.")

#PART 6 TRANSACTIONS

def DEPOSIT():
    try:
        deposit=input("Enter Depositor's Account Number:")
        amount=input("Enter amount:")
        c.execute("select * from Accounts")
        r=c.fetchall()
        for i in r:
            if deposit == i[0]:
                c.execute("Update Accounts set Amount = Amount + {} where Acc_No = {}".format(amount,deposit))
                con.commit()
                break
        else:
            print("Account doesnot exists.")
    except:
        con.rollback()
        print("Technical Error.. Money Cannot be Deposited..") 
             
def WITHDRAW():
    try:
        withdraw=input("Enter Withdrawer's Account Number:")
        minimum=input("Enter minimum balance:")
        amount=input("Enter amount:")
        c.execute("select Acc_No, Amount from Accounts")
        r=c.fetchall()
        for i in r:
            if withdraw == i[0]: 
                if i[1] - amount > minimum:
                    c.execute("Update Accounts set Amount = Amount -{} where Acc_No = {}".format(amount,withdraw))
                    con.commit()
                    break
                else:
                    print("Alert... Amount cannot go under minimum balance.")
        else:
            print("Account doesnot exists.")
    except:
        con.rollback()
        print("Technical Error.. Transaction Failure.")     

def MINIMUM_BALANCE():
    try:
        min=input("Enter your Minimum Balance:")
        c.execute("select * from Accounts where amount < "+min)
        r=c.fetchall()
        for i in r:
            print(i)
    except:
        print("Technical Error.. Data Cannot be Fetched.")

def TRANSACTION():
    try:
        sender=int(input("Enter Sender's Account Number:"))
        receiver=int(input("Enter Receiver's Account Number:"))
        amount=int(input("Enter amount:"))
        c.execute("select * from Accounts")
        r=c.fetchall()
        for i in r:
            if receiver == i[0]:
                c.execute("Update Accounts set Amount = Amount + {} where Acc_No = {}".format(amount,receiver))
                print('done')
                con.commit()
            elif sender==i[0]:
                c.execute("Update Accounts set Amount = Amount - {} where Acc_No = {}".format(amount,sender))
                print('done')
                con.commit()
                break
        else:
            print("Either one of the Accounts or both Accounts doesnot exists.")
    except:
        con.rollback()
        print("Technical Error.. Transaction Failure.")      

#PART 7 FORMS AND REPORTS

def FORMS(table):
    try:
        c.execute("desc "+table)
        print("****FORM****")  
        r=c.fetchall()
        for i in r:
             print(i[0],":")
    except:
        print("Technical Error.. Report Cannot be Fetched.")        

def REPORTS(table):
    try:
        c.execute("desc "+table)
        f=c.fetchall()
        c.execute("select * from {}".format(table))
        r=c.fetchall()
        print("****REPORT****")
        for i in f:
            print(i[0],end="\t\t\t")
        print()
        print("********************************************************************************************************************")
        for i in r:
            for j in i:
                print(j,end="\t\t\t")
            print()
            print("********************************************************************************************************************")
    except:
        print("Technical Error.. Report Cannot be Fetched.")

#PART 8 MAIN MENU

while True:
    print("*****************************************************************************")
    print("*********MAIN MENU*********")
    print("1)  Create Tables in Database")
    print("2)  Insert Records in a Table")
    print("3)  Display Records from a Table")
    print("4)  Search Records from a Table")
    print("5)  Update Records in a Table")
    print("6)  Add a Record into a Table")
    print("7)  Delete a record from a Table")
    print("8)  Total Number of Records in a Table")
    print("9)  Sort Records from a Table")
    print("10) Filter Records from a Table")
    print("11) Modify Table Structure")
    print("12) Deposit/Withdraw Money")
    print("13) Check for Minimum Balance")
    print("14) Make a Transaction")
    print("15) Create Forms")
    print("16) Create Reports")
    print("17) Shut Down RDBMS")
    print("*****************************************************************************")
    print()
    ch=int(input("Enter Your Choice:"))
    print()
    
    if ch == 1:
        print("****SUB MENU****")
        print("a) Customer Table")
        print("b) Accounts Table")
        print("c) Branch Table")
        print("d) Loan Table")
        print("e) Custom Table")
        ch1=input("Enter your choice:")
        if ch1 in "aA":
            C_TABLE()
        elif ch1 in "bB":
            A_TABLE()
        elif ch1 in "cC":
            B_TABLE()
        elif ch1 in "dD":
            L_TABLE()
        elif ch1 in "eE":
            t=input("Enter name of table:")
            CREATE_TABLE(t)
        else:
            print("Invalid Choice...")
        
    elif ch == 2:
        t=input("Enter name of table:")
        INSERT_RECORD(t)
        
    elif ch == 3:
        t=input("Enter name of table:")
        DISPLAY_RECORDS(t)
    
    elif ch == 4:
        t=input("Enter name of table:")
        SEARCH_RECORDS(t)
    
    elif ch == 5:
        t=input("Enter name of table:")
        UPDATE_RECORDS(t)
    
    elif ch == 6:
        t=input("Enter name of table:")
        ADD_RECORD(t)
    
    elif ch == 7:
        t=input("Enter name of table:")
        DELETE_RECORD(t)
    
    elif ch == 8:
        t=input("Enter name of table:")
        NO_RECORDS(t)
        
    elif ch == 9:
        t=input("Enter name of table:")    
        print("****SUB MENU****")
        print("a) In Ascending Order")
        print("b) In Descending Order")
        ch9=input("Enter your choice:")
        if ch9 in 'aA':
            SORT_ASC(t)
        elif ch9 in 'bB':
            SORT_DESC(t)
        else:
            print("Invalid Choice...")
            
    elif ch == 10:
        t=input("Enter name of table:")
        FILTER_RECORD(t)
        
    elif ch == 11:
        t=input("Enter name of table:")
        print("****SUB MENU****")
        print("a) Add a Column")
        print("b) Delete a Column")
        print("c) Change name of Column")
        print("d) Modify Existing Column Definition")
        ch11=input("Enter your choice:")
        if ch11 in 'aA':
            t=input("Enter name of table:")
            ADD_COLUMN(t)
        elif ch11 in 'bB':
            t=input("Enter name of table:")
            DELETE_COLUMN(t)
        elif ch11 in 'cC':
            t=input("Enter name of table:")
            NAME_COLUMN(t)
        elif ch11 in 'dD':
            t=input("Enter name of table:")
            MODIFY_COLUMN(t)
        else:
            print("Invalid Choice...")
        
    elif ch == 12:
        print("****SUB MENU****")
        print("a) Deposit Money")
        print("b) Withdraw Money")
        ch12=input("Enter your choice:")
        if ch12 in 'aA':
            DEPOSIT()         
        elif ch12 in 'bB':
             WITHDRAW()
        else:
             print("Invalid Choice...")
        
    elif ch == 13:
        MINIMUM_BALANCE()
        
    elif ch == 14:
        TRANSACTION()
        
    elif ch == 15:
        t=input("Enter name of table:")
        FORMS(t)
    
    elif ch == 16:
        t=input("Enter name of table:")
        REPORTS(t)
        
    elif ch == 17:
        print("Thank you for using our DBMS... ")
        print("Meet you soon... :-D ")
        con.close()
        break
            
    else:
        print("Invalid Choice...")

    print()

#END OF PROJECT
