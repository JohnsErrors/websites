import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import sys
import msvcrt
from colorama import init
init()
import smtplib
import email.utils
from email.mime.text import MIMEText
import json
from datetime import datetime
import threading
import concurrent.futures
import os
import urllib.request as urllib
import random

user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

headers = { 'User-Agent': user_agent_desktop}


def GetSource(website):
    whileVariable = 0
    while True:
        try: 
            source = BeautifulSoup(requests.get(website, headers=headers, timeout=7).text, "html.parser")
        except:
            whileVariable += 1
            if whileVariable > 1:
                print("x", end="")
                return False
            continue
        if source is not None:
            break
    return source
def getDomain(href):
    return urlparse(href).netloc.replace("www.","")

def executeThread(threads, one=0):
    print("!",end="")
    if one != 0:
       threads.start() 
       threads.join()
       return 0
    for x in threads:
        x.start() 
    for x in threads:
        x.join(timeout=7)
        
def readFileToJson( fileName ):
    with open(fileName) as json_file:
        dataBase = json.load(json_file)
    return dataBase
    
def writeFileToJson( fileName, listDatabase ):
    with open(fileName, 'w') as outfile:
        json.dump(listDatabase, outfile)
        
SearchedDomains = ["facebook", "youtube", "blogspot", "wordpress", "pinterest", "vote", "networkadvertising", "security", "vimeo", "twitter", "instagram", "googletagmanager", "reddit", "googlesyndication", "samsung", "amazon", "paypal", "doubleclick", "mozilla", "schema", "w3", "apple", "move", "imgix", "shopify", "judge", "serif", "google", "github", "youtu", "mailchimp", "wordpress"]

def GetLinksFromPage(page):
	
	global siteDomain
	cleanLinksArray = []
	
	sourceXMLF = GetSource(page)
	if sourceXMLF == False:
		return
	linkFun = sourceXMLF.findAll("a", attrs={'href': re.compile("^https://")})
	global globalLinkData
	for href in linkFun:
		if getDomain(href["href"]) != "" and getDomain(href["href"]) != siteDomain:
			if getDomain(href["href"]) not in cleanLinksArray and len(getDomain(href["href"]).split(".",1)[0]) > 14 and getDomain(href["href"]).count(".") < 2 and getDomain(href["href"]) not in globalLinkData and getDomain(href["href"]).split(".",1)[0] not in SearchedDomains:
				cleanLinksArray.append(getDomain(href["href"]))
				
	globalLinkData += cleanLinksArray
	print(".", end="")
	if random.randint(0,30) == 7:
		print(len(globalLinkData), end="")
	
def printStatistics(pages=0):
    os.system('cls')
    print( "\n\n Working Program ", arraynumber , " ............." )
    print( "\n Website waiting to be parsed DataBase [" + str(len(WebToPeParsed_DATABASE)) + "]" )
    print( " Websites DataBase [" + str(len(Websites_DATABASE)) + "]\n" )
    if pages==0:
        print( " Checking [\033[91m" + siteDomain + "\033[39m]\n\n" )
    else:
        print( " Checking [\033[91m" + siteDomain + "\033[39m] - " + str(pages) + "\n\n" )
        
    
WebToPeParsed_DATABASE = True
Websites_DATABASE = readFileToJson('WEBSITES-dataBase.txt')

#executeThread( threading.Thread(target=FilterGoodSitesFast), 1 )

AllLinksParsed = []
globalLinkData = []
siteDomain = ""
domainNow = ""
arraynumber = int(os.path.basename(__file__).replace(".py", ""))

while WebToPeParsed_DATABASE:
	
	#Updating Data
	WebToPeParsed_DATABASE = readFileToJson('WebToBeParsed-dataBase.txt')
	domainNow = WebToPeParsed_DATABASE[arraynumber]
	WebToPeParsed_DATABASE.remove(domainNow)
	WebToPeParsed_DATABASE += globalLinkData
	writeFileToJson( 'WebToBeParsed-dataBase.txt', WebToPeParsed_DATABASE )
	
	
	url = "https://" + domainNow + "/sitemap.xml"
	siteDomain = getDomain(url)
	print("Sitemap ", arraynumber, " -- ",domainNow + " .....")
	
	AllLinksParsed = []
	globalLinkData = []

	sourceXML = GetSource(url)
	if sourceXML == False:
		continue
	sitemap = sourceXML.findAll("loc")

	for x in sitemap:
		if ".xml" in x.text:
			sourceXML2 = GetSource(x.text)
			if sourceXML2 == False:
				continue
			sitemap2 = sourceXML2.findAll("loc")
			for x2 in sitemap2:
				if ".xml" in x2.text:
					print(x2)
				else:
					AllLinksParsed.append(x2.text)
		else:
			AllLinksParsed.append(x.text)
    
	printStatistics( len(AllLinksParsed) )
	
	if len(AllLinksParsed) > 2000:
		AllLinksParsed = AllLinksParsed[:2000]
    
	if AllLinksParsed != []:
		t = []
		for url in AllLinksParsed:
			t.append(threading.Thread(target=GetLinksFromPage, args=[url]))  
		executeThread(t[:int(len(t)/4)]) # 0-500
		executeThread(t[ int((len(t)/4)+1) : int((len(t)/2)) ]) #500-1000
		executeThread(t[ int((len(t)/2)) : int((len(t)/4)*3) ]) #1000-1500
		executeThread(t[ int((len(t)/4)*3): ]) #1500-all
    
	Websites_DATABASE = readFileToJson('WEBSITES-dataBase.txt')
	Websites_DATABASE += globalLinkData
	writeFileToJson( "WEBSITES-dataBase.txt", Websites_DATABASE )
    


