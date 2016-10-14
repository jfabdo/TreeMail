#Written by Jack Abdo
#
import pypyodbc
from datetime import datetime as now
from Summarize import summarize

#Connecting to the Database

#WARNING: DANGEROUS- please read the comments. 
#Please do not call this function outside this file.
#Make a connection function and call that for the specific user/permissions you need
#It's ok to return and pass a connection, just please don't pass around the password dictionary
def __getusers(): #don't call this function outside this file, under pain of Keurig machine
    userlookup = {}
    f = open("keyfile.txt", 'r')
    for i in f.readlines():
        tempuser = i.strip().split(" ")
        userlookup[tempuser[0]] = tempuser[1]
    f.close()
    return userlookup

def sqlconnection(user):
    usertable = __getusers()
    connstring = 'Driver={SQL Server};Server=INDYD9Q5TJS1\\ILLIUM;Database=Noti-FYI;uid=' + user + ";" + "pwd=" + usertable[user] + ";"
    ourconn = pypyodbc.connect(connstring)
    return ourconn

 def scopeid(name):
   connection = sqlconnection("checkentries")
   cursor = connection.cursor()
   cursor.execute("select ident_current('" + "')" )
   results = cursor.fetchone()
   return results

def selectfromdb(SQLCommand):
   connection = sqlconnection("checkentries")
   cursor = connection.cursor()
   cursor.execute(SQLCommand)
   results = cursor.fetchall()
   return results

#this checks to see if there are any new emails that have been pushed
def checkqueuedemails():
   connection = sqlconnection("checkentries")
   cursor = connection.cursor()
   SQLCommand = ("SELECT MessageID, MessageFull FROM ParseMessage") 
   try: 
      cursor.execute(SQLCommand) 
      results = cursor.fetchall()
   except:
      results = ""
      print("SQL exception")
   
   return results #if results else "" #legacy

#Sample of inserting record
def sqlinsert(table,entries,Values):
   for i in Values:
      if ((i) is list) or (type(i) is tuple):
         raise Exception("Fix the SQL pull")
   connection = sqlconnection("checkentries")
   cursor = connection.cursor()
   SQLCommand = "INSERT INTO dbo.[" + table + "] ("
   for val in entries:
      SQLCommand = SQLCommand + val + ", "
   SQLCommand = SQLCommand[:-2] + ") VALUES ("
   for _ in range(len(entries)):
      SQLCommand = SQLCommand + "?,"
   #Values = ['Susan','Ibach','Toronto'] 
   SQLCommandT = (SQLCommand[:-1] + ")")
   cursor.execute(SQLCommandT,Values)
   connection.commit()
   connection.close()

#this function fetches a user ID if it is in the table or returns -1 if it
#does not exist
def getuser(user):

   if type(user) is list:
      temp = user[0]
      del user
      user = temp

   if type(user) is not str:
      raise Exception("Wrong datatype")
      exit(1)

   connection = sqlconnection("checkentries")
   cursor = connection.cursor()
   SQLCommand = ("select id from dbo.[User] WHERE email = '" + user + "'")
   #try:
   cursor.execute(SQLCommand)
   results = cursor.fetchall()
   #except:
   #   print("SQL exception")
   #   exit(1)

   if len(results) == 0:
      return -1

   return results[0][0]




#returns a list of lists containing people and emails.
def splitemailfields(email):
   emails = email.replace("\n","").split(";")
   allemails = []
   for i in emails:
      i = i.strip()
      templist = []
      if "[" in i:
         templist = i.split("[")
      elif "<" in i:
         templist = i.split("<")
      elif "@" not in i:
         templist = [i,""]
      elif "@" in i and " " not in i:
         templist = ["",i]
      else:
         print("Not split correctly")

      if not templist:
         continue

      templist[1] = templist[1].replace("]","").replace(">","").strip()
      templist[0] = templist[0].strip()

      if len(emails) == 1:
         return [templist]
      else:
         allemails.append(templist)

   return allemails



#This function accepts pre-parsed emails and puts them into the sql table...
#If you don't have emails that are already split up, don't run this function.
#Instead, run splitmessages() from ParseFile.py on this first. Or parse them..
#yourself. I don't care. I'm not your mother.
#TODO: Add to email table
#TODO: Add to CCs
#TODO: Add reply ID
#TODO: Add summary to summary table
#TODO: 
def storeemails(parsedmessages):
   sender = [] #declaring vars for readability
   date = now.now()
   recipient = []
   cc = []
   subject = ""
   body = ""
   reply = 0
   length = len(parsedmessages)
   count = 0
   for email in parsedmessages:
      count += 1
      #fetch the email address, which is after the first front angle bracket

      date = email[1]


      if "<" in email[0]:
         char = ["<", ">"]
      elif "[" in email[0]:
         char = ["[","]"]
      else:
         raise Exception("Unexpected email format")

      sender.append(email[0].split(char[0])[1].replace(char[1],"").strip())  #retrieves the email from the first segment

      uid = getuser(sender)

      if uid == -1:
         sender.append(email[0].split("<")[0])
         sqlinsert("user",["email","name"],sender)
         uid = getuser(sender)
      
      date = " ".join(email[1].split()[1:]).replace("at","")
      subject = email[4].replace("'","''")
      body = email[5].replace("'","''")
      cc = splitemailfields(email[3])
      
      sqlcommand = "select id from dbo.[email] where subject = '" + subject + "' and sent = '" + date + "'"# and body = '" + body + "'"

      checkforemail = selectfromdb(sqlcommand)

      if None in checkforemail or checkforemail == []:
         sqlinsert("email",["sent","subject","body","reply"],[date,subject,body,reply]) #add search for duplicate emails here
         reply = selectfromdb(sqlcommand)[0][0]
         test = 0

         sqlinsert("message",["userid","role","fmailid"],[uid,"sender",reply])
         for i in cc:
            checkuser = "select id from dbo.[user] where"
            if not(i[0] or i[1]):
               continue
            if i[0]:
               checkuser = checkuser + " name = '" + i[0] + "'"
            if i[0] and i[1]:
               checkuser = checkuser + " and"
            if i[1]:
               checkuser = checkuser + " email = '" + i[1] + "'"
            ccid = selectfromdb(checkuser)
            if ccid == [] or None in ccid:
               sqlinsert("user",["name","email"],i)
               ccid = selectfromdb(checkuser)
            sqlinsert("message",["userid","role","fmailid"],[ccid[0][0],"cc",reply])

         summary = summarize(body)
         if not summary:
            summary = ["NULL"]

         summarystatement = ""
         for i in summary:
            summarystatement = summarystatement + i
         sqlinsert("summary",["fmailid","summarybody"],[reply,summarystatement])

      else:
         reply = checkforemail[0][0]

   return 0

#Retrieving multiple rows
"""
import pypyodbc connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost;'
                                'Database=testdb;'
                                'uid=sa;pwd=P@ssw0rd') 
cursor = connection.cursor() SQLCommand = ("INSERT INTO Customers "
                 "(firstName, lastName, city) "
                 "VALUES (?,?,?)")
Values = ['Susan','Ibach','Toronto'] cursor.execute(SQLCommand,Values) connection.commit() connection.close()
"""