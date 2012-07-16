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

source = """Tables –– List of Database Tables used within phpBB3

==Tables==
{|border="1" cellspacing="0" cellpadding="3"
! name
! content
|-
| [[Table.phpbb_acl_groups|phpbb_acl_groups]]
| Permission roles and/or individual permissions assigned to groups
|-
| [[Table.phpbb_acl_options|phpbb_acl_options]]
| List of possible permissions
|-
| [[Table.phpbb_acl_roles|phpbb_acl_roles]]
| Permission roles (Standard Moderator, Simple Moderator etc.)
|-
| [[Table.phpbb_acl_roles_data|phpbb_acl_roles_data]]
| Permissions each role contains
|-
| [[Table.phpbb_acl_users|phpbb_acl_users]]
| Permission roles and/or individual permissions assigned to users
|-
| [[Table.phpbb_attachments|phpbb_attachments]]
| Information on attachments (Post, physical filename, original filename, MIME type...)
|-
| [[Table.phpbb_banlist|phpbb_banlist]]
| Banned users/IPs/emails...
|-
| [[Table.phpbb_bbcodes|phpbb_bbcodes]]
| Custom BBCodes
|-
| [[Table.phpbb_bookmarks|phpbb_bookmarks]]
| Bookmarked topics
|-
| [[Table.phpbb_bots|phpbb_bots]]
| Spiders/Robots
|-
| [[Table.phpbb_config|phpbb_config]]
| Configuration information ($config table)
|-
| [[Table.phpbb_confirm|phpbb_confirm]]
| Contains session information for confirm pages ("are you sure you want to delete foo")
|-
| [[Table.phpbb_disallow|phpbb_disallow]]
| Disallowed usernames
|-
| [[Table.phpbb_drafts|phpbb_drafts]]
| Drafts of future posts/private messages
|-
| [[Table.phpbb_extension_groups|phpbb_extension_groups]]
| Extensions Groups (associate extensions with a file type - Images, text...)
|-
| [[Table.phpbb_extensions|phpbb_extensions]]
| Extensions (.xxx) allowed for attachments
|-
| [[Table.phpbb_forums|phpbb_forums]]
| Forums (Name, description, rules...)
|-
| [[Table.phpbb_forums_access|phpbb_forums_access]]
| Stores who is logged in to password protected forums
|-
| [[Table.phpbb_forums_track|phpbb_forums_track]]
| Unread post information is stored here
|-
| [[Table.phpbb_forums_watch|phpbb_forums_watch]]
| Subscribed forums
|-
| [[Table.phpbb_groups|phpbb_groups]]
| Usergroups
|-
| [[Table.phpbb_icons|phpbb_icons]]
| Post icons
|-
| [[Table.phpbb_lang|phpbb_lang]]
| Installed languages
|-
| [[Table.phpbb_log|phpbb_log]]
| Administration/Moderation/Error logs
|-
| [[Table.phpbb_login_attempts|phpbb_login_attempts]]
| tbd
|-
| [[Table.phpbb_moderator_cache|phpbb_moderator_cache]]
| Who is a moderator in which forum (for display on forum index)
|-
| [[Table.phpbb_modules|phpbb_modules]]
| Configuration of acp, mcp and ucp modules
|-
| [[Table.phpbb_poll_options|phpbb_poll_options]]
| Options text of all votes ("Yes", "No", "Maybe"...)
|-
| [[Table.phpbb_poll_votes|phpbb_poll_votes]]
| Users which have voted on a poll
|-
| [[Table.phpbb_posts|phpbb_posts]]
| Topics posts
|-
| [[Table.phpbb_privmsgs|phpbb_privmsgs]]
| Private messages text
|-
| [[Table.phpbb_privmsgs_folder|phpbb_privmsgs_folder]]
| Custom privates messages folders (for each user)
|-
| [[Table.phpbb_privmsgs_rules|phpbb_privmsgs_rules]]
| Messages rules, e.g. "if the username of the sender is ..., move the message to this folder".
|-
| [[Table.phpbb_privmsgs_to|phpbb_privmsgs_to]]
| Information (sender, new, replied...) on private messages.
|-
| [[Table.phpbb_profile_fields|phpbb_profile_fields]]
| Custom profile fields (name, min/max number of characters, allowed characters...)
|-
| [[Table.phpbb_profile_fields_data|phpbb_profile_fields_data]]
| Data that users enter in custom profile fields
|-
| [[Table.phpbb_profile_fields_lang|phpbb_profile_fields_lang]]
| tbd (empty on my forum with some custom profile fields)
|-
| [[Table.phpbb_profile_lang|phpbb_profile_lang]]
| Localized name and description of custom profile fields (presented to users)
|-
| [[Table.phpbb_ranks|phpbb_ranks]]
| Ranks (Name, image, minimal # of posts)
|-
| [[Table.phpbb_reports|phpbb_reports]]
| Reported posts
|-
| [[Table.phpbb_reports_reasons|phpbb_reports_reasons]]
| Reasons for reported posts and disapprovals
|-
| [[Table.phpbb_search_results|phpbb_search_results]]
| Last searches
|-
| [[Table.phpbb_search_wordlist|phpbb_search_wordlist]]
| Indexed words (for search)
|-
| [[Table.phpbb_search_wordmatch|phpbb_search_wordmatch]]
| Associate a post with indexed words
|-
| [[Table.phpbb_sessions|phpbb_sessions]]
| Sessions (to identify users browsing the forum)
|-
| [[Table.phpbb_sessions_keys|phpbb_sessions_keys]]
| Autologin feature
|-
| [[Table.phpbb_sitelist|phpbb_sitelist]]
| Secure Downloads of attachments - list of IPs and hostnames
|-
| [[Table.phpbb_smilies|phpbb_smilies]]
| Smilies (text => image)
|-
| [[Table.phpbb_styles|phpbb_styles]]
| Style = template + theme + imageset
|-
| [[Table.phpbb_styles_imageset|phpbb_styles_imageset]]
| [[Templating_Tutorial#Customizing_the_Imageset|Imagesets]]
|-
| [[Table.phpbb_styles_imageset_data|phpbb_styles_imageset_data]]
| tbd
|-
| [[Table.phpbb_styles_template|phpbb_styles_template]]
| tbd
|-
| [[Table.phpbb_styles_template_data|phpbb_styles_template_data]]
| tbd
|-
| [[Table.phpbb_styles_theme|phpbb_styles_theme]]
| theme = css file
|-
| [[Table.phpbb_topics|phpbb_topics]]
| Topics in forums
|-
| [[Table.phpbb_topics_posted|phpbb_topics_posted]]
| Who posted to which topic (used for the small dots in viewforum)
|-
| [[Table.phpbb_topics_track|phpbb_topics_track]]
| Unread post information is stored here
|-
| [[Table.phpbb_topics_watch|phpbb_topics_watch]]
| "notify me upon replies"
|-
| [[Table.phpbb_user_group|phpbb_user_group]]
| Users groups
|-
| [[Table.phpbb_users|phpbb_users]]
| Registered users
|-
| [[Table.phpbb_warnings|phpbb_warnings]]
| Warnings given to users
|-
| [[Table.phpbb_words|phpbb_words]]
| censored words
|-
| [[Table.phpbb_zebra|phpbb_zebra]]
| Friends and foes
|}
<br>

==Info==
* Script used to create this list: [[User:Pyramide/DB2wiki]].
* Updated to reflect the wiki guidelines (battye, January 2009)<br><br>

[[Category:Database]]
[[Category:Database Tables]]

[[ja:Tables]]
"""

table_data = {}
use_next_line = False
for line in source.splitlines():
    if use_next_line:
        description = line.strip("| ")
        table_data[table_name]=description
        use_next_line = False
#        print description
#        print
        continue
    if line.startswith("| [[Table."):
        table_name = line.split(".",1)[1].split("|",1)[0].split("_",1)[1]
        table_name = "".join(["%s%s" % (p[0].upper(), p[1:]) for p in table_name.split("_")])
        print table_name       
        use_next_line = True

print "="*79

new_file_content = ""
with file("../django_phpBB3/models.py", "r") as f:
    for line in f:
        new_file_content += line
#        print line
        if "(models.Model):" in line:
            model_name = line.split(" ",1)[1].split("(",1)[0]
            print model_name
            if not model_name in table_data:
                model_name += "s"
                
            if model_name in table_data:
                print " *** ", table_data[model_name]
                new_file_content += '    """\n'
                new_file_content += "    %s\n" % table_data[model_name]
                new_file_content += '    """\n'

with file("../django_phpBB3/models.py", "w") as f:
    f.write(new_file_content)

print "="*79

new_file_content = ""
with file("../django_phpBB3/admin.py", "r") as f:
    for line in f:
        new_file_content += line
#        print line
        if "Admin(admin.ModelAdmin):" in line:
            model_name = line.split(" ",1)[1].split("(",1)[0]
            model_name = model_name[:-5] # cut 'Admin'
            print model_name
            if not model_name in table_data:
                model_name += "s"
                
            if model_name in table_data:
                print " *** ", table_data[model_name]
                new_file_content += '    """\n'
                new_file_content += "    %s\n" % table_data[model_name]
                new_file_content += '    """\n'

print new_file_content
with file("../django_phpBB3/admin.py", "w") as f:
    f.write(new_file_content)
            
    