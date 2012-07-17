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
import pprint

from model_data import data # generated with scripts/help_text.py

# Cut Phpbb from table names:
table_names = [k[5:] for k in data.keys()]

inner_rename = ["Forums", "Privmsgs", "Reports", "Sessions"]
inner_rename_data = dict([(i,i[:-1]) for i in inner_rename])
#pprint.pprint(inner_rename_data)
#{'Forums': 'Forum',
# 'Privmsgs': 'Privmsg',
# 'Reports': 'Report',
# 'Sessions': 'Session'}

rename_data = {}
for table_name in table_names:
    if table_name.endswith("s"):
        if table_name.endswith("Access"):
            clean_name = table_name
        else:
            clean_name = table_name[:-1]
        
        for source, dest in inner_rename_data.items():
            if source in clean_name:
                clean_name = clean_name.replace(source, dest)
                break
            
        rename_data[table_name] = clean_name

#pprint.pprint(rename_data)
#{'AclGroups': 'AclGroup',
# 'AclOptions': 'AclOption',
# 'AclRoles': 'AclRole',
# 'AclUsers': 'AclUser',
# 'Attachments': 'Attachment',
# 'Bbcodes': 'Bbcode',
# 'Bookmarks': 'Bookmark',
# 'Bots': 'Bot',
# 'Drafts': 'Draft',
# 'ExtensionGroups': 'ExtensionGroup',
# 'Extensions': 'Extension',
# 'Forums': 'Forum',
# 'ForumsAccess': 'ForumAccess',
# 'Groups': 'Group',
# 'Icons': 'Icon',
# 'LoginAttempts': 'LoginAttempt',
# 'Modules': 'Module',
# 'PollOptions': 'PollOption',
# 'PollVotes': 'PollVote',
# 'Posts': 'Post',
# 'Privmsgs': 'Privmsg',
# 'PrivmsgsRules': 'PrivmsgRule',
# 'ProfileFields': 'ProfileField',
# 'Ranks': 'Rank',
# 'Reports': 'Report',
# 'ReportsReasons': 'ReportReason',
# 'SearchResults': 'SearchResult',
# 'Sessions': 'Session',
# 'SessionsKeys': 'SessionKey',
# 'Smilies': 'Smilie',
# 'Styles': 'Style',
# 'Topics': 'Topic',
# 'Users': 'User',
# 'Warnings': 'Warning',
# 'Words': 'Word'}


def rename_file_content(filepath, rename_data):
    with file(filepath, "r") as f:
        content = f.read()
    
    for source, dest in rename_data.items():
        content = content.replace(source, dest)
    
    with file(filepath, "w") as f:
        f.write(content)
        
    print "%s patched!" % filepath


if __name__=="__main__":
    rename_file_content("../django_phpBB3/models.py", rename_data)
    rename_file_content("../django_phpBB3/admin.py", rename_data)
    


    
    