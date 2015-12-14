#----------------------------------------------------------------#
# File name: BeautifulSoup_Get_Mixed_Content_by_Directory.py
# Author: Youssef Riahi
# Date created: 12/03/2015
# Date last modified: 12/09/2015
# Script version: 1.2
# Python Version: 2.7.10
#----------------------------------------------------------------
# 1.0 - Initial version parsing webages for hot images, css and js
#     - Results are printed to screen or sent to file via shell.
# 1.1 - Fix to close each page after parsing is done.
#     - Added content id.
#     - Added exluded files list.
# 1.2 - Removed htm or html as usage arguments.
#     - Added list of web file extensions (.html, .html) for 
#       flexibility. Script can also scan asp, aspx...etc
#     - Changed output file format to CSV.
#     - Added: if __name__ == '__main__'   See comment at bottom.
#----------------------------------------------------------------#
'''
Description: 
   A python script that finds the hot linked items (https and https): Images, CSS and JS.
   The script can be expanded to find other HTML elements, tags, attributes...etc

Usage: 
The script accepts 2 args: 
   1- the target folder. 
   2- File extension (specify: html/html).
   python Get_Soup_Items_and_Pages.py.py /var/www/
'''

# load the required modules
import os, sys, bs4, re
from os import path, walk
from sys import argv
from collections import Counter
from bs4 import BeautifulSoup

# list web page types to be parsed
file_extensions = ['.htm', '.html']

# exclude files here; in case you are using include files
exclude_mgs_files = [
                     'mgsSnFooterLinks.html',
                     'mgsInMegadd.html',
                     'mgsInNavBreadcrumbs.html',
                     'mgsInNavAlertStatus.html',
                     'mgsInNavAlert.html',
                     'navon_includes.html'
                     ]

# setting up the arguments:
# the script takes 1 arg; and that is 'yourpath' being scanned for 
script, yourpath = argv

# this is a (dictionary) of all pages, it is empty now.
list_of_pages = {}

# creating a new file to which we can save the list of files
list_of_pages_file = open('list_of_pages.csv', 'wb')
list_of_pages_file.write('Hotlink item, Page, Content ID' + os.linesep)

# function to search directory recursively; and parse htm/html files.
def BeautifulSoup_Get_Mixed_Content_by_Directory():
   for root, dirs, files in os.walk(str(yourpath)):
      for f in files:
         #if yourext == os.path.splitext(f)[1][1:]:  # old version
         file_extension = os.path.splitext(os.path.join(root, f))[1]
         # webpage extensions being parsed. the list can be expanded.
         if file_extension in file_extensions:
            if str(f) not in exclude_mgs_files:               
               one_page = os.path.join(root,f)
               fp = open(one_page,'rb')
               soup = BeautifulSoup(fp.read(), 'html.parser')
               
               # Rhythmyx CMS content_id
               # <meta name="contentID" content="1536015"  />
               # not all the *.html files have 'meta' information, so we try first!
               try:
                  content_id = soup.find('meta', {'name':'contentID'})['content']
               except:
                  # if 'one_page' does not have it...keep going!
                  pass

               # IMAGES: match this pattern example:
               # <img src="http://notmysite.com/image.jpg" height="350" width="200">
               img_urls = soup.find_all('img', attrs={'src': re.compile('^http(s)?://')})
               for img_url in img_urls:
                  clean_img_url = img_url['src']
                  list_of_pages_file.write('%s, %s, %s' % (clean_img_url, one_page, content_id) + os.linesep)
               
               # CSS: match this pattern example: href that starts with http ot https
               # <link rel="stylesheet" href="/resources/styles/main.css" />
               css_urls = soup.find_all('link', attrs={'href': re.compile('^http(s)?://')})
               for css_url in css_urls:
                  clean_css_url = css_url['href']
               if clean_css_url.endswith('.css'): # get css only, we dont want schema.dcterms 
                  list_of_pages_file.write('%s, %s, %s' % (clean_css_url, one_page, content_id) + os.linesep)

               # JS: match this pattern: src that starts with http or https
               # <script src="http://notmyjs.com/resources/scripts/vendor/jquery.js"></script>
               js_urls = soup.find_all('script', attrs={'src': re.compile('^http(s)?://')})
               for js_url in js_urls:
                  clean_js_url = js_url['src']
                  if clean_js_url.endswith('.js'): # get urls ending with .js only 
                     list_of_pages_file.write('%s, %s, %s' % (clean_js_url, one_page, content_id) + os.linesep)
              
               # close the opened html/htm file being read 'one_page'.
               fp.close()

# run the code in this file only if it is called directly by python.
# a condition can be placed to allow/prevent other script to embded this file.
# details about this can be found here: http://ibiblio.org/g2swap/byteofpython/read/module-name.html
if __name__ == '__main__':
   # run the big function above
   BeautifulSoup_Get_Mixed_Content_by_Directory()
   # close the file after writing the matching results
   list_of_pages_file.close()


