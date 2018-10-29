#Written by Jack Abdo
#
"""
FUNCTIONS:
removewhitespace- Removes whitespace, including tabs and new lines into single spaced, single line
wordfreq- takes a string of words and returns the word frequency
countwords- wrapper for wordfreq, cleans text of punctuation and whitespace, calls whitespace and wordfreq
sortwords- Sorts the dict by value and returns the values, reversed.
mostcommonwords- returns the most common words used, takes no input
returntop- returns the most frequently used words above severity threshold, calls sortwords and mostcommonwords
countworddensity- counts the word density in the sentences
picksentences- Returns a set of summary sentences that should describe the article

USAGE:

[   countwords<->removewhitespace
    countwords<->wordfreq
]

"""

from string import punctuation
from copy import deepcopy
testsample = "Test me. I am a sentence. I am also a sentence."

f = open("TestArticle.txt","r")

ourtext = f.read()
f.close()
severity = 3 #increase this for more reduction, default is 1

#Static

def mostcommonwords(): #these are the most common words in all published material, filler words for the most part. They will be biased against.
    f = open("mostcommonwords.txt","r")
    commonwords = []
    for i in f.readlines():
        commonwords.append(i.strip())
    return commonwords

def ranksentences():
    pass

#Simple Dynamic

def removewhitespace(textstring = ""): #strips out all the whitespace into a single lined block
    textstring = textstring.replace("\n","")

    while("  " in textstring):
        textstring = textstring.replace("  "," ") #remove duplicate whitespace

    return textstring

def sortwords(wordcount): #automagic sort
    return sorted(wordcount,key=wordcount.get,reverse=True)

def wordfreq(textstring): #takes a string of words and returns the word frequency
    wordcount = {} #
    for i in textstring.split(" "):#go through every word in the teststring
        if i in wordcount: #if in the dictionary, increment, otherwise add it
            wordcount[i] += 1
        else:
            wordcount[i] = 1
    return wordcount #return subsequent dictionary of word frequency

def countwords(textstring = ""): #returns the word frequency, wrapper for wordfreq, cleans text of punctuation and whitespace, calls whitespace and wordfreq
    if not textstring: #if the summary is empty, return nothing
        return {}
    
    for i in punctuation:
        textstring = removewhitespace(textstring.replace(i,"")) #remove all punctuation iteratively

    return wordfreq(textstring)

#Inter-Dynamic

def returntop(wordcount):#returns the most frequently used words above severity threshold. CALLS: sortwords,mostcommonwords
    global severity
    wordssorted = sortwords(wordcount) #pulls all the words in the article, sorted
    commonwords = mostcommonwords() #pulls all the common words
    mostfrequentwords = []
    for i in wordssorted:
        if (wordcount[i] > severity) and (i not in commonwords): 
            mostfrequentwords.append(i)
    return mostfrequentwords

def countworddensity(article,wordcount): #counts the top-word density in the sentences. CALLS:NOTHING
   sentencelist = article.split(".")
   sentencewordfreq = []
   for i in range(len(sentencelist)):
      keywordcount = 0
      ii = sentencelist[i]
      for k in wordcount:
         if k in ii:
            keywordcount += 1
      sentencewordfreq.append(keywordcount)
   return sentencewordfreq

def summarize(article): #picks the top sentences, CALLS:countworddensity,top
   wordcount = countwords(article)
   frequencies = 
    
    (wordcount)
   sentencewordfreq = countworddensity(article,frequencies) #list of keyword densities per sentence
   #freqlist = deepcopy(wordcount)
   summarysentences = []

   #for i in frequencies:
   #   j = freqlist.index(i)
   #   freqlist[j] = 0
   #   summarysentences.append(article[j])
   for i in zip(article.split("."),sentencewordfreq):
       if i[1] > (.55*max(sentencewordfreq)):
           summarysentences.append(i[0]+".")

   return summarysentences

#for i in summarize(ourtext):
#    print(i.replace("\n","")),
