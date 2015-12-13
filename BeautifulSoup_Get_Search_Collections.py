#----------------------------------------------------------------#
# File name: BeautifulSoup_Get_Search_Collections.py
# Author: Youssef Riahi
# Date created: 12/11/2015
# Date last modified: 12/13/2015
# Script version: 1.1
# Python Version: 2.7.10
#----------------------------------------------------------------
# 1.0 - Initial version to find search collections per '/site'.
#     - Target Server URL is hardcoded.
# 1.1 - Added server URL as params.
# 1.2 - Added error handling for missing params.
#----------------------------------------------------------------#
'''
Description: 
   A python script that finds GSA  collections on each portal site on mass.gov. 

Usage: 
   python BeautifulSoup_Get_Search_Collections.py
'''
import requests, sys # an HTTP library and others
from bs4 import BeautifulSoup # html parser
from sys import argv # building args

# list of portalized sites
PortalSites = ['ago', 'anf', 'auditor', 'berkshireda', 'capeda',
'childadvocate', 'cjc', 'courts', 'dor', 'dppc', 'edu', 'eea','elders',
'eohhs', 'eopss', 'essexda', 'essexsheriff', 'ethics', 'governor', 'hdc',
'hed', 'ig', 'informedma', 'itdemployee', 'lwd', 'massworkforce', 'mcad',
'mdaa', 'mova', 'msa', 'mtrs', 'ocabr', 'osc', 'pca', 'perac', 'portal',
'recovery', 'srbtf', 'treasury','veterans', 'women']

# main function
def BeautifulSoup_Get_Search_Collections():
	# enure that we have 2 params
	if len(sys.argv) == 2:		
		for PortalSite in PortalSites:
			# build the url
			PortalSiteUrl = str(my_base_url) + str(PortalSite)
			
			# initiate a requets and get content
			r = requests.get(PortalSiteUrl)
			
			# feed that content to BeautifulSoup and specify a parser
			soup = BeautifulSoup(r.content, 'html.parser')
			
			# the content being searched for is:
			# <select name="site" id="search_scope">
			optionz = soup.find_all('select', {'name':'site'})
			for option in optionz:
				option_elements = option.find_all('option')
				print option.get_text()
	else:
	   # Print usage if missing params
	   print '\n[ ! ] Usage: python ' + str(sys.argv[0]) + ' http://www.yourwebsite.tld/ \n'

BeautifulSoup_Get_Search_Collections()
