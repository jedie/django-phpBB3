# coding: utf-8

"""
    scripts
    ~~~~~~~
    
    HACK!
    
    Parse data from:
        http://wiki.phpbb.com/index.php?title=Tables&action=edit
    
    and insert them into model descriptions.

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import os
import shutil
import urllib2
import re
import pprint


CONTENT_RE = re.compile(
    r'<textarea.*?>(.*?)</textarea>', re.IGNORECASE | re.VERBOSE | re.UNICODE | re.DOTALL
)
LINK_RE = re.compile(
    r'\[\[(.*?)\|(.*?)\]\]', re.IGNORECASE | re.VERBOSE | re.UNICODE | re.DOTALL
)
TABLE_RE = re.compile(
    r'\{\|(.*?)\|\}', re.IGNORECASE | re.VERBOSE | re.UNICODE | re.DOTALL
)
HEADINGS_RE = re.compile(
    r'^\! (.*?)$', re.IGNORECASE | re.UNICODE | re.MULTILINE
)
COLUMN_BLOCK_RE = re.compile(
    r'(?:\-)([^-]*)', re.UNICODE | re.DOTALL
)

COLUMN_RE = re.compile(
    r'\| (.+)', re.UNICODE
)


TEMP_DIR = "./temp/"
TEMP_NAME = "%s%%s.txt" % TEMP_DIR
if not os.path.isdir(TEMP_DIR):
    print "Create %r" % TEMP_DIR
    os.mkdir(TEMP_DIR)
else:
    print "Use %r" % TEMP_DIR

def get_wiki_page(site_name):
    temp_file = TEMP_NAME % site_name
    
    if os.path.isfile(temp_file):
        print "Use cache file %r" % temp_file
        with file(temp_file, "r") as f:
            content = f.read()
    else:
        url = "http://wiki.phpbb.com/index.php?title=%s&action=edit" % site_name
        print "Request %r" % url
        
        f = urllib2.urlopen(url)
        content = f.read()
        
        content = content.decode("utf-8")
        
        with file(temp_file, "w") as f:
            f.write(content)
            
    return content


def get_textarea(content):
    content = CONTENT_RE.findall(content)[0]
    return content


def get_table_data(content):
    table_data = {}
    use_next_line = False
    table_name = None
    for line in content.splitlines():
        if table_name:
            description = line.strip("| ")
            table_data[table_name]["description"]=description
            table_name = None
    #        print description
    #        print
            continue
        
        if line.startswith("| [[Table."):
            page_name, table_name = LINK_RE.findall(line)[0]          
            #table_name = line.split(".",1)[1].split("|",1)[0].split("_",1)[1]
            table_name = "".join(["%s%s" % (p[0].upper(), p[1:]) for p in table_name.split("_")])
#            print table_name
            table_data[table_name]={"page_name": page_name}
            
    return table_data


def fill_table_data(table_data):
    for table_name in table_data:
        print "_"*79
        print table_name
        data = table_data[table_name]
        print data
        content = get_wiki_page(data["page_name"])
        if "Login required" in content or "no text in this page" in content:
            # Page is not creaed, yet.
            print "Skip not existing page!"
            continue
        
        content = get_textarea(content)
        try:
            table_info = TABLE_RE.findall(content)[0]
        except:
            print " *** Error with:", table_name
            continue
    
#        print table_info
        headings = HEADINGS_RE.findall(table_info)
        
        column_data = {}
        for column_block in COLUMN_BLOCK_RE.findall(table_info):
#            print "***", column_block
            column_info = COLUMN_RE.findall(column_block)
#            print column_info
            for key, value in zip(headings, column_info):
                column_data[key] = value
#            print "----"
            
        column_name = column_data.pop("column")
#        print column_data
        table_data[table_name][column_name] = column_data
#        print "=" * 79

        

if __name__=="__main__":
    content = get_wiki_page("Tables")
#    print repr(content)
#    print content
#    print "="*79
    content = get_textarea(content)
    table_data = get_table_data(content)
#    print table_data

#    print "="*79    
    fill_table_data(table_data)
#    print table_data    

    pprint.pprint(table_data)
    
    