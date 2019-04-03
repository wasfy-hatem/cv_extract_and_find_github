import sys
import jsonpickle
#import json
import simplejson as json
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io

import glob
import os

import csv

#------------------------------------------------------------------------------
# colors
CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
CWHITEBG2  = '\33[107m'
#------------------------------------------------------------------------------



def append_csv(row):
	#row = "[\"Email\", \"Github Account\"]"
	print ("row inside csv function is: ", row)
	with open('github_accounts.csv', 'a', newline='') as csvFile:
    		writer = csv.writer(csvFile)
    		writer.writerow(row)

	csvFile.close()
	return



def readfiles(path):
   
   os.chdir(path)
   pdfs = []
   for file in glob.glob("*.pdf"):
       #print(CYELLOW, file)
       pdfs.append(file)

   return pdfs




def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

        match = re.search(r'[\w\.-]+@[\w\.-]+', data)
        match.group(0)
        if match.group(0):

           ###print(match.group(0))
           email = match.group(0)
           break
        else:
           email = ""
           pass
    
    return email #email


def get_github_profile(email):

	#https://api.github.com/search/users?q=solankiarpit1997@gmail.com

	base_url            = "https://api.github.com/search/users?q="
	#ending_url          = "+in:email&type=Users"
	#email = sys.argv[1] #input from outside
	#email               = "ha_wasfy@yahoo.com"
	result_start_url    = "https://github.com"
	site_url =  base_url + email



	#info_by_user_name = "https://api.github.com/users/hatemwasfy"
	#https://api.github.com/search/users?q=ha_wasfy@yahoo.com

	'''
	print("-------------------------------------------------------")
	print("email is: ", email)
	print("site URL is: ", site_url)
	print("-------------------------------------------------------")
	'''
	try:
		with urlopen(site_url) as url:
			data = json.loads(url.read().decode())
			#print(data["items"][0]["html_url"]) # "login" is login name only

			user_github_account = data["items"][0]["html_url"]
	except:
			user_github_account = "Not found"

	#print("Github account is: ", user_github_account)
	
	return user_github_account


#------------------__Main__-------------------

'''
with open("file.txt", "r") as ins:
    array = []
    for line in ins:
        array.append(line)
'''


'''
text_file = "email.tamago.ok.txt"
with open(text_file, "r") as ins:
	#array = []
	for line in ins:
		#array.append(line)
		#print(line)
		email = line
		
		#email 			= sys.argv[1] #input from outside

		user_github_account 	= get_github_profile(email)

		print("\n-------------------------------------------------------")
		print("Email account: ", email)
		print("Github account is: ", user_github_account)
		print("-------------------------------------------------------\n")

'''

pdfs = readfiles(sys.argv[1])

'''
print(CYELLOW + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(CYELLOW + "The following are the given CV files")
print(pdfs)
print(CYELLOW + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
'''

print(CYELLOW + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(CYELLOW + "The following are the given CV files")
print(CYELLOW + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

for rf in pdfs:
	print(CWHITE2, rf)

print(CYELLOW + "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


#email= "ha_wasfy@yahoo.com"
#email = pdfparser(sys.argv[1]) #path of pdf file from outside

#pdf = pdfs[0]

header_row = ["Email Address", "Github Account"]

append_csv(header_row)

for pdf in pdfs:

	email = pdfparser(pdf) #path of pdf file from outside

	user_github_account     = get_github_profile(email)

	print(CYELLOW + "\n-------------------------------------------------------")
	print(CBEIGE2 + "Email account:     " + CWHITE2, email)
	print(CBEIGE2 + "Github account is: " + CWHITE2, user_github_account)
	print(CYELLOW + "-------------------------------------------------------\n")
	
	row = [email, user_github_account]

	append_csv(row)


