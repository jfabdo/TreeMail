Written by Jack Abdo

This is a two part application that consists of an Outlook macro and a Python 
Web Application. It works to reduce clutter from long email chains by 
coordinating with the web application.

NOTICE: VERY IMPORTANT
Please do not share the key file. It contains sensitive information for our servers and information.

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