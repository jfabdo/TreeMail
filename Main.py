#Written by Jack Abdo
#
from Connections import sqlconnection,checkqueuedemails,storeemails
from multiprocessing import Process
from ParseFile import splitmessages
from Subscription import senddigest
from Summarize import summarize
from time import sleep, time


def hold(timeofrun, holdtime = 60): #sleeps for t - current_time or 0 
   timeleft = timeofrun + holdtime - time()
   sleep(timeleft if timeleft>0 else 0)

def macroresults(): #fetch results and return them
   pass

def checkmacro():#tests the macro connection
   connection = sqlconnection("insert_macro")
   timeofrun = time()
   if not connection:
      open("error.log",'r').write("Cannot open SQL connection\n").close()
      exit(1)
   hold(timeofrun)
   print("macroran " + str(time()))

def prunt(strng): #prints safely, prints #s for unknown chars
   try:
      print(strng)
   except UnicodeEncodeError:
#      print("unicode ran")
      for chrcr in strng:
         try:
            print(chrcr,end='')
         except:
            print('#', end='')
   except:
      print("unicode did not run")

#returns true if one element in list is in the second string(or list)
#usage: onein(["frank","thomas"],"frank the builder") returns true
#usage: onein(["frank","thomas"],"dora the explorer") returns false
def onein(lst,strng):
   for i in lst:
      if i in strng:
         return True
   return False

#returns true if all elements in list is in the second string(or list)
#usage: allin(["frank","thomas"],"frank the builder rides thomas the tank engine") returns true
#usage: allin(["frank","thomas"],"frank the builder") returns false
#usage: allin(["frank","thomas"],"dora the explorer") returns false
def allin(lst,strng):
   for i in lst:
      if i not in strng:
         return False
   return True

def proccessmessages():
   results = checkqueuedemails()#actually we probably need this. Acutally take this and throw it into summary. Actually maybe not. Actually figure it out.
   resultstring = results[0][1]
   #exchanges characters for actual tabs and newlines
   #this may become redundant in future versions depending on the macro, but...
   #for now it solves a bug in the SQL results
   resultstring = resultstring.replace(chr(0x5c)+chr(0x74),chr(0x09)).replace(chr(0x5c)+chr(0x6e),chr(0x0A)) #wacky slappy hacky taffy
   parsedresults = splitmessages(resultstring)
   #print(type(parsedresults),len(parsedresults))
   storeemails(parsedresults)
   #for lrst in parsedresults:#for testing purposes.
   #   for strng in lrst:
   #      prunt(strng)
   #      #pass
   hold(time(),120)

def main():
   checkmacro() #macropolo

tasks = ["checkmacro","proccessmessages"] #list of tasks

def testprocess(procname=""):
   while(1):
      proccessmessages()
      hold(time(),60)

if __name__ == '__main__':
   testprocess()#for testing purposes only. otherwise, reenable the rest of...
   #the commented out lines
   #processes = {}
   #for i in tasks:
   #   print("running " + i)
   #   processes[i] = Process(target=eval(i),args=())
   #   processes[i].start()
   #while(1): #main loop
   #   waitrun = time()
   #   print(i + ": " + str(processes[i].is_alive()))
   #   for i in processes.keys():
   #      if not processes[i].is_alive():
   #         print("running " + i)
   #         processes[i] = Process(target=eval(i),args=())
   #         processes[i].start()
   #   hold(waitrun,30)
   #   print(time())
