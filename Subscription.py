from Connections import selectfromdb as sdb
import datetime

def senddigest():
   results = selectfromdb("select UserID, FmailID, UpdateTime from Subscription")
   
   results = results.sort(key=lambda x: x[2])

   now = datetime.datetime.now().time#().replace(minute=0, second=0, microsecond=0)
   for i in results:
      while not (i[2] < now()):
         wait(30)

