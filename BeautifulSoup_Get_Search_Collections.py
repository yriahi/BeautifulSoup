#----------------------------------------------------------------#
# File name: BeautifulSoup_Get_Search_Collections.py
# Author: Youssef Riahi
# Date created: 12/11/2015
# Date last modified: 12/11/2015
# Script version: 1.0
# Python Version: 2.7.10
#----------------------------------------------------------------
# 1.0 - Initial version to find search collections per portal site.
#     - Target Server/URL is now hardcoded. Can be 'argv'
#----------------------------------------------------------------#
'''
Description: 
   A python script that finds GSA  collections on each portal site on mass.gov. 
Usage: 
   python BeautifulSoup_Get_Search_Collections.py
'''
import requests, bs4
from bs4 import BeautifulSoup

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
		PortalSiteUrl = str(my_base_url) + str(PortalSite)
		r = requests.get(PortalSiteUrl)
		soup = BeautifulSoup(r.content, 'html.parser')
		#<select name="site" id="search_scope">
		optionz = soup.find_all('select', {'name':'site'})
		for option in optionz:
			option_elements = option.find_all('option')
			option_element = option.get_text()
			print str(option_element).strip('in ')
			# I am saving this loop for potential json output
			#for foo_element in option_elements:
			#	print foo_element.get_text()

BeautifulSoup_Get_Search_Collections()
