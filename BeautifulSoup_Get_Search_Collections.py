#----------------------------------------------------------------#
# File name: BeautifulSoup_Get_Search_Collections.py
# Author: Youssef Riahi
# Date created: 12/11/2015
# Date last modified: 12/11/2015
# Script version: 1.0
# Python Version: 2.7.10
#----------------------------------------------------------------
# 1.0 - Initial version to find search collections per portal site.
#     - Target Server/URL is now hardcoded.
#----------------------------------------------------------------#
'''
Description: 
   A python script that finds GSA  collections on each portal site on mass.gov. 

Usage: 
   python BeautifulSoup_Get_Search_Collections.py
'''
import requests # an HTTP library
from bs4 import BeautifulSoup # html parser

# target server with portal site to scan
my_base_url = 'http://www.mass.gov/'

# list of portalized sites
PortalSites = ['ago', 'anf', 'auditor', 'berkshireda', 'capeda',
'childadvocate', 'cjc', 'courts', 'dor', 'dppc', 'edu', 'eea','elders',
'eohhs', 'eopss', 'essexda', 'essexsheriff', 'ethics', 'governor', 'hdc',
'hed', 'ig', 'informedma', 'itdemployee', 'lwd', 'massworkforce', 'mcad',
'mdaa', 'mova', 'msa', 'mtrs', 'ocabr', 'osc', 'pca', 'perac', 'portal',
'recovery', 'srbtf', 'treasury','veterans', 'women']

# main function
def BeautifulSoup_Get_Search_Collections():
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

BeautifulSoup_Get_Search_Collections()
