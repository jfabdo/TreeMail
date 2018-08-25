Written by Jack Abdo

Python3 script that summarizes long text patterns. Pair it with an email plugin to receive your. Can be broken out as an API.

Example code:

from Summarize import summarize
contents = open('TestArticle.txt').read()

for i in summarize(contents):
  print(i.strip(),end='')


API:
Summarize.py
One should import summarize.summarize to use the main module. Other modules may be useful as well

Summarize.py contains:
removewhitespace- Removes whitespace, including tabs and new lines into single spaced, single line
wordfreq- takes a string of words and returns the word frequency
countwords- wrapper for wordfreq, cleans text of punctuation and whitespace, calls whitespace and wordfreq
sortwords- Sorts the dict by value and returns the values, reversed.
mostcommonwords- returns the most common words used, takes no input
returntop- returns the most frequently used words above severity threshold, calls sortwords and mostcommonwords
countworddensity- counts the word density in the sentences
summarize- Returns a set of summary sentences that should describe the article


Parsefile.py
parsefile.splitemail should return the list of emails in a thread

Parsefile.py contains

populateheader
kickgarbage - Removes empty and whitespace entries, as well as leading and trailing whitespace
splitmessages - splits up input into separate entries.
