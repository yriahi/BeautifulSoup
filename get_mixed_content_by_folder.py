#----------------------------------------------------------------#
# File name: get_mixed_content_by_folder.py
# Author: Youssef Riahi
# Date created: 12/03/2015
# Date last modified: 02/09/2016
# Script version: 2.0
# Python Version: 2.7.10
#----------------------------------------------------------------
# Description: 
#    The script will walk a directory structure of a website and
#    scans the html code for "Mixed Content" (non-https items)
#    It looks for the following if the they start with 'http://':
#    - Linked IMAGES: <img src>
#    - Linked CSS files: <link rel>
#    - Linked SCRIPTS: <script src>
# 
# Usage:
#    python get_mixed_content_by_website_folder /var/www/
# 
# Notes:
#----------------------------------------------------------------#

# load the required modules
import os, sys, bs4, re
from os import path, walk
from sys import argv
from collections import Counter
from bs4 import BeautifulSoup

# setting up target folder as script argument
script, yourpath = argv

# folder from which this script is executed
Script_Home = os.getcwd()

# folder where results/reports are generated 
Output_Directory_Name = 'mixed_content_output'
Output_Directory_Path = os.path.join(Script_Home, Output_Directory_Name)

# check if the folder does not exist
if not os.path.isdir(Output_Directory_Name):
   print 'Creating output directory...'
   os.mkdir(Output_Directory_Name)

# list web page extensions to be parsed
file_extensions = ['.htm', '.html']

# regex for urls starting with...
URL_REGEX = 'http://.+'

# exclude files
exclude_mgs_files = ['file_01.html', 'file_02.html']

# exclude folders
Sub_Folders_List_Exclude = ['folder_a', 'folder_b']

# create and empty list of subfolders in 'yourpath'
Sub_Folders_List = []

# create and empty list of subfolders in 'yourpath'
Sub_Folders_List_Names = []

# create an empty dictionary with site names and matching path
Sub_Folders_Dictionary = {}

# keep track of the files that we are going to parse
files_2_parse_list = []

# create one output file if needed
all_mixed_content_pages = open('all_mixed_content_pages.csv','wb')
all_mixed_content_pages.write('Hotlink item, Page, Content ID' + os.linesep)

def get_sub_folders():
   for Sub_Folder in os.listdir(str(yourpath)):
      # get folders only
      if os.path.isdir(os.path.join(str(yourpath), Sub_Folder)):
         # skip symlinks
         if os.path.islink(os.path.join(str(yourpath), Sub_Folder)) == False:
            Sub_Folder_Name = os.path.basename(os.path.join(str(yourpath), Sub_Folder))
            # check exclude list
            if Sub_Folder not in Sub_Folders_List_Exclude:
               # save folder name only to a list
               Sub_Folders_List_Names.append(os.path.basename(os.path.join(str(yourpath), Sub_Folder)))
               # add folder path to a list
               Sub_Folders_List.append(os.path.join(str(yourpath), Sub_Folder))
               # create 'Sub_Folders_Dictionary' with key(foleder name) and value(path)
               Sub_Folders_Dictionary[os.path.basename(os.path.join(str(yourpath), Sub_Folder))] = str(os.path.join(str(yourpath), Sub_Folder))

# search directory recursively; and parse htm/html files.
def BeautifulSoup_Get_Mixed_Content_by_Directory():
   for Sub_Folder in Sub_Folders_List_Names:
      # show current folder being worked on...
      print '[+] Processing %s folder...' % (Sub_Folder)
      
      # create an output csv file with a header
      output_file_format = Sub_Folder + '_mixed_content_pages.csv'
      list_of_pages_file = open(os.path.join(Output_Directory_Path, output_file_format), 'wb')
      list_of_pages_file.write('Hotlink item, Page, Content ID' + os.linesep)

      #for root, dirs, files in os.walk(os.path.join(root,Sub_Folder)):
      #   print os.path.join(root,f)

      for root, dirs, files in os.walk(str(yourpath) +'/'+ str(Sub_Folder)):
         #print os.path.abspath(yourpath)
         for f in files:
            # get the file extension in 'Sub_Folder'
            file_extension = os.path.splitext(os.path.join(root, f))[1]
            
            # if extension matches...'htm or html'
            if file_extension in file_extensions:
               # if file is not in exclude list (to avoid apache html includes)
               if str(f) not in exclude_mgs_files:               
                  # build path to each page
                  one_page = os.path.join(root,f)
                  files_2_parse_list.append(one_page)
                  
                  try:
                     # open each web page in 'Read Binary' mode
                     fp = open(one_page,'rb')
                     
                     # feed the opened htm/html file to BeautifulSoup parser
                     soup = BeautifulSoup(fp.read(), 'html.parser')
                     
                     # Rhythmyx CMS content_id:    <meta name="contentID" content="1536015"  />
                     # not all the htm(l) files have 'meta' information, so we try first!
                     content_id_meta = soup.find('meta', {'name':'contentID'})
                     if content_id_meta is None:
                        # IMAGES:   <img src="http://notmysite.com/image.jpg" height="350" width="200">
                        img_urls = soup.find_all('img', attrs={'src': re.compile(URL_REGEX)})
                        for img_url in img_urls:
                           clean_img_url = img_url['src']
                           list_of_pages_file.write('%s, %s' % (clean_img_url, one_page) + os.linesep)
                           all_mixed_content_pages.write('%s, %s' % (clean_img_url, one_page) + os.linesep)
                     
                        # CSS:   <link rel="stylesheet" href="/resources/styles/main.css" />
                        css_urls = soup.find_all('link', attrs={'href': re.compile(URL_REGEX)})
                        for css_url in css_urls:
                           clean_css_url = css_url['href']
                        if clean_css_url.endswith('.css'): # get css only, we dont want schema.dcterms 
                           list_of_pages_file.write('%s, %s' % (clean_css_url, one_page) + os.linesep)
                           all_mixed_content_pages.write('%s, %s' % (clean_css_url, one_page) + os.linesep)

                        # JS:   <script src="http://notmyjs.com/resources/scripts/vendor/jquery.js"></script>
                        js_urls = soup.find_all('script', attrs={'src': re.compile(URL_REGEX)})
                        for js_url in js_urls:
                           clean_js_url = js_url['src']
                           if clean_js_url.endswith('.js'): # get urls ending with .js only 
                              list_of_pages_file.write('%s, %s' % (clean_js_url, one_page) + os.linesep)

                     else:
                        # get just the content id
                        content_id = soup.find('meta', {'name':'contentID'})['content']

                        # IMAGES:   <img src="http://notmysite.com/image.jpg" height="350" width="200">
                        img_urls = soup.find_all('img', attrs={'src': re.compile(URL_REGEX)})
                        for img_url in img_urls:
                           clean_img_url = img_url['src']
                           list_of_pages_file.write('%s, %s, %s' % (clean_img_url, one_page, content_id) + os.linesep)
                           all_mixed_content_pages.write('%s, %s, %s' % (clean_img_url, one_page, content_id) + os.linesep)
                     
                        # CSS:   <link rel="stylesheet" href="/resources/styles/main.css" />
                        css_urls = soup.find_all('link', attrs={'href': re.compile(URL_REGEX)})
                        for css_url in css_urls:
                           clean_css_url = css_url['href']
                        if clean_css_url.endswith('.css'): # get css only, we dont want schema.dcterms 
                           list_of_pages_file.write('%s, %s, %s' % (clean_css_url, one_page, content_id) + os.linesep)
                           all_mixed_content_pages.write('%s, %s, %s' % (clean_css_url, one_page, content_id) + os.linesep)

                        # JS:   <script src="http://notmyjs.com/resources/scripts/vendor/jquery.js"></script>
                        js_urls = soup.find_all('script', attrs={'src': re.compile(URL_REGEX)})
                        for js_url in js_urls:
                           clean_js_url = js_url['src']
                           if clean_js_url.endswith('.js'): # get urls ending with .js only 
                              list_of_pages_file.write('%s, %s, %s' % (clean_js_url, one_page, content_id) + os.linesep)
                     
                     # close htm/html file after reading and parsing.
                     fp.close()
                  
                  except IOError as e:
                     print "Unable to open '%s' file" % (one_page)
      
      # close the file after writing the matching results
      list_of_pages_file.close()

# run the code in this file only if it is called directly by python.
# a condition can be placed to allow/prevent other script to embded this file.
# details about this can be found here: http://ibiblio.org/g2swap/byteofpython/read/module-name.html
if __name__ == '__main__':
   # run the big function above
   get_sub_folders()
   BeautifulSoup_Get_Mixed_Content_by_Directory()

