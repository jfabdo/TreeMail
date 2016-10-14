#Written by Jack Abdo

from re import search as rsrc,split as rspt,S as dotall
#from Main import prunt as prnt

f = open("","r")
emails = f.read()

#should break down the emails into discrete sections
regdict = {}
regdict["header"] = "From:(?:\s){0,}(.*)(?:\s){1,}Sent:(.*)(?:\s){1,}To:(.*)(?:\s){1,}Cc:([\s\S]*?)Subject:(.*)(\s){1,}([\s\S]*?)(?=(From:|$))" 
regdict["headeralt"] = "On(.*)wrote:(.*)" #sometimes, for whatever reason
regdict["body"] = "(?:From:)(?:.){1,}(?:\s){1,}(?:Sent:)(?:.){1,}(?:\s){1,}(?:To:)(?:.){1,}(?:\s){1,}(?:Cc:)(?:\s|\S){1,}(?:\s){1,}(?:Subject:)(?:.){1,}(?:\s){1}(\s|\S){1,}"
regdict["emailbody"] = "((?:From:)(?:.){1,}(?:\s){1,}(?:Sent:)(?:.){1,}(?:\s){1,}(?:To:)(?:.){1,}(?:\s){1,}(?:Cc:)(?:\s|\S){1,}(?:\s){1,}(?:Subject:)(?:.){1,}(?:\s){1}(\s|\S){1,})"
catchemailalt = ""

#def populateheader(splitemail):
#    emailist = []

#    for i in splitemail:
#        emailist.append(rspt(emailist,i))

#    print(emailist)

"""Removes empty and whitespace entries, as well as leading and trailing whitespace """
def kickgarbage(emailist):
    ouriter = list(range(len(emailist))) #wacky laughy hacky taffy
    for i in ouriter:
        if not emailist[i].strip() or emailist[i].strip() == "From:":
            emailist.pop(i) #remove empty ent
            ouriter.insert(i+1,i) #wacky laughy hacky taffy
            ouriter.pop() #wacky laughy hacky taffy
        else:
            emailist[i] = emailist[i].strip()
    return emailist

"""Splits up"""
def splitmessages(email):
    global regdict

    wroteflag = 0
    #deburg = rsrc(regdict["header"],email)
    #print(deburg)
#    if not rsrc(tempreg,email): #if this is false, then this is not an email, exit error 1
#        exit(1)

    if rsrc(regdict["headeralt"],email):
        wroteflag = 1 #use other pattern

    splitemail = rspt(regdict["header"],email)
    splitemail = kickgarbage(splitemail)

    for i in range(len(splitemail)//6):
        combineemail = [splitemail[i]]
        for _ in range(5):
            combineemail.append(splitemail.pop(i+1))
        splitemail[i] = combineemail

    if rsrc(regdict["headeralt"],email):
        ouriter = list(range(len(splitemail)))
        for i in ouriter:
            #print(rsrc(regdict["headeralt"],splitemail[i][-1]))
            if rsrc(regdict["headeralt"],splitemail[i][-1]):
                onwroteemail = rspt(regdict["headeralt"],splitemail[i][-1])
                splitemail[i][-1] = onwroteemail.pop(0)
                onwroteemail[0],onwroteemail[1] = onwroteemail[0][::-1].split(",")[0][::-1],','.join(onwroteemail[0][::-1].split(",")[1:])[::-1]#sorry
                for i in range(3):
                   onwroteemail.insert(3,"")                
                splitemail.insert(i+1,onwroteemail)
                ouriter.append(len(splitemail)-1)
                ouriter.pop(i+1)

    #TODO: Write this out
    #if wroteflag:
    #    for i in range(0,len(splitemail),2):
    #        pass
    #    pass
    
    #emailist = populateheader(splitemail)

    return splitemail


#test = splitmessages(emails)
#prunt(test)