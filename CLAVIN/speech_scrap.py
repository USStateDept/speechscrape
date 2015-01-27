# -*- coding: utf-8 -*-
import bs4
import requests
from pymongo import MongoClient
from dateutil import parser
import json
import sys
sys.setrecursionlimit(7400)

DEBUG = True

YEARINDEX = [2009,2010,2011,2012,2013,2014]
BASEURL = "http://www.state.gov/r/pa/ei/speeches/****/index.htm"

#connected to DB
moncon = MongoClient()
dosdb = moncon['dosspeeches']
doscollection = dosdb.collection

#pull all speech links from this page
    #each has an index check if it is already in our database
        #if not then 
            #get body of request
            #parse the metadata including index, location, state person, etc
            #store meta data inforomation with the output from CLIFF in mongo
                #this is dosspeechers ->collection

def processCLIFF(text):
    retries = 1
    #this might need to be a post
    while retries < 5:
        print retries
        if DEBUG == True:
            print "trying ", text[:50]
        rfrom = requests.post("http://localhost:8080/CLIFF/parse/text", params={'q':text})
        if rfrom.status_code == 200:
            print "CLIFF Success"
            return json.loads(rfrom.text)
        else:
            print rfrom.text
        retries += 1


    print "CLIFF failure"
    return {}


def processSpeech(speechurl, title):
    response = requests.get(speechurl)
    soup = bs4.BeautifulSoup(response.text)

    jsonObj = {"title":title, "cliffresponse":{},"date":"", "bodytext":"", 'url':speechurl }


    #try these
    BODYTRIES = ["#region-content", "#left-content", "#subpage"]
    #firsttry

    for bodyattempts in BODYTRIES:
        bodytext = soup.select(bodyattempts)
        if len(bodytext) == 0:
            continue
        else:
            if DEBUG == True:
                print bodytext[0].get_text()[:100]
            jsonObj['bodytext'] = bodytext[0].get_text()
            jsonObj['cliffresponse'] = processCLIFF(jsonObj['bodytext'])
            break

    DATETRIES = ['#date_long', '.date']

    for dateattempts in DATETRIES:
        datetext = soup.select(dateattempts)
        if len(datetext) == 0:
            continue
        else:
            if DEBUG == True:
                print "trying to get the date"
            jsonObj['date'] = parser.parse(datetext[0].get_text()) 
            break

    doscollection.insert(jsonObj)
    return True
                            


import dateutil.parser
from itertools import chain
import re

# Add more strings that confuse the parser in the list
UNINTERESTING = set(chain(dateutil.parser.parserinfo.JUMP, 
                          dateutil.parser.parserinfo.PERTAIN,
                          ['a']))

def _get_date(tokens):
    for end in xrange(len(tokens), 0, -1):
        region = tokens[:end]
        if all(token.isspace() or token in UNINTERESTING
               for token in region):
            continue
        text = ''.join(region)
        try:
            date = dateutil.parser.parse(text)
            return end, date
        except ValueError:
            pass

def find_dates(text, max_tokens=50, allow_overlapping=False):
    tokens = filter(None, re.split(r'(\S+|\W+)', text))
    skip_dates_ending_before = 0
    for start in xrange(len(tokens)):
        region = tokens[start:start + max_tokens]
        result = _get_date(region)
        if result is not None:
            end, date = result
            if allow_overlapping or end > skip_dates_ending_before:
                skip_dates_ending_before = end
                yield date



totals = {"success":0, "fails":0}
#index the speeches
for currentyear in YEARINDEX:
    currenturl = BASEURL.replace("****", str(currentyear))

    response = requests.get(currenturl)
    soup = bs4.BeautifulSoup(response.text)
    links = [a for a in soup.select('#tier3-landing-content-wide a')]
    #.attrs.get('href')
    #save memory
    soup = None
    print "working on ", currentyear
    counter = 1
    for link in links[:50]:
        print link.attrs.get('href')
        if (doscollection.find_one({"url": link.attrs.get('href')}) or not link.attrs.get('href') or link.attrs.get('href')[0] == "#"):
            print "    found one skip"
            continue
        
        try:
            print "     ", counter, " out of ", len(links), "for", link.attrs.get('href')
            processSpeech(link.attrs.get('href'), link.get_text())
            totals['success'] +=1
        except Exception, e:
            print "!!!!!!!!!failed on with ", link
            print "!!!!!!!!!", str(e)
            totals['fails'] +=1
        counter += 1
print "successes", totals['success']
print "fails", totals['fails']



