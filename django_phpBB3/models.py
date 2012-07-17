# coding: utf-8

"""
    models
    ~~~~~~
    
    References:
        http://wiki.phpbb.com/Tables
        https://github.com/phpbb/phpbb3/tree/master/phpBB/install/schemas

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from django.db import models


#
#These classes would need Django to support composite keys:
#
#class AclGroups(models.Model):
#    """
#    Permission roles and/or individual permissions assigned to groups
#    """
#    # group_id = models.IntegerField()
#    group_id = models.ForeignKey("Groups", db_column="group_id", to_field="group_id",
#        # mediumint(8) unsigned
#        default=0,
#        help_text="{{fk|groups|group_id}}"
#    )
#    # forum_id = models.IntegerField()
#    forum_id = models.ForeignKey("Forums", db_column="forum_id", to_field="forum_id",
#        # mediumint(8) unsigned
#        default=0,
#        help_text="{{fk|forums|forum_id}}"
#    )
#    # auth_option_id = models.IntegerField()
#    auth_option_id = models.ForeignKey("Acl_options", db_column="auth_option_id", to_field="auth_option_id",
#        # mediumint(8) unsigned
#        default=0,
#        help_text="{{fk|acl_options|auth_option_id}}"
#    )
#    # auth_role_id = models.IntegerField()
#    auth_role_id = models.ForeignKey("Acl_roles", db_column="role_id", to_field="role_id",
#        # mediumint(8) unsigned
#        default=0,
#        help_text="{{fk|acl_roles|role_id}}"
#    )
#    auth_setting = models.IntegerField(
#        # tinyint(2)
#        default=0,
#        help_text="ACL_YES, ACL_NO or ACL_NEVER"
#    )
#    class Meta:
#        db_table = u'phpbb3_acl_groups'



class User(models.Model):
    """
    Registered users
    """
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="Primary key"
    )
    user_type = models.IntegerField(
        # tinyint(2)
        default=0,
        help_text="Defines what type the user is. 0 is normal user, 1 is inactive and needs to activate their account through an activation link sent in an email, 2 is a pre-defined type to ignore user (i.e. bot), 3 is Founder."
    )
    # group_id = models.ForeignKey("Group", db_column="group_id", to_field="group_id")
    group_id = models.ForeignKey("Groups", db_column="group_id", to_field="group_id",
        # mediumint(8) unsigned
        default=3,
        help_text="The user's default group. {{fk|groups|group_id}}"
    )
    user_permissions = models.TextField(
        # mediumtext
        help_text="A cached copy of the user's computed permissions."
    )
    # user_perm_from = models.ForeignKey(
    user_perm_from = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="The id of the user whose permissions are being tested. {{fk|users|user_id}}"
    )
    user_ip = models.CharField(max_length=40,
        # varchar(40)
        help_text="The IP of the user on registration, dotted QUAD style (ie: 127.0.0.1)"
    )
    user_regdate = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="User's registration date/time, UNIX timestamp"
    )
    username = models.CharField(max_length=255,
        # varchar(255)
        help_text="the username as it is shown all over the board"
    )
    username_clean = models.CharField(max_length=255, unique=True,
        # varchar(255)
        help_text="The all lower-case normalized version of the username for comparisons."
    )
    user_password = models.CharField(max_length=40,
        # varchar(40)
        help_text="The [[Function.phpbb_hash|hashed]] version of the user's password."
    )
    user_passchg = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp indicating when the user's password was last changed."
    )
    user_pass_convert = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating whether or not the user's password needs to be converted to the phpBB3 hashing. Used when converting from phpBB2."
    )
    user_email = models.CharField(max_length=100,
        # varchar(100)
        help_text="User's email address"
    )
    user_email_hash = models.BigIntegerField(
        # bigint(20)
        default=0,
        help_text="A hash of the user's email address."
    )
    user_birthday = models.CharField(max_length=10,
        # varchar(10)
        help_text="The user's birthday, in the form of dd-mm-yyyy."
    )
    user_lastvisit = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="User's last visit time, UNIX timestamp."
    )
    user_lastmark = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="The last time the user clicked 'Mark forums read'"
    )
    user_lastpost_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="The time of the latest post of the user, UNIX timestamp"
    )
    user_lastpage = models.CharField(max_length=200,
        # varchar(200)
        help_text="The last page visited by the user."
    )
    user_last_confirm_key = models.CharField(max_length=10,
        # varchar(10)
        help_text="Code used for security reasons by confirmation windows"
    )
    user_last_search = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the user performed a search. Used for search flood time limits."
    )
    user_warnings = models.IntegerField(
        # tinyint(4)
        default=0,
        help_text="The number of warnings the user has."
    )
    user_last_warning = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the user was warned."
    )
    user_login_attempts = models.IntegerField(
        # tinyint(4)
        default=0,
        help_text="The number of times a login to this account has failed. This is reset to zero upon successful login."
    )
    user_inactive_reason = models.IntegerField(
        # tinyint(2)
        default=0,
        help_text="Reason for being inactive"
    )
    user_inactive_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, when the user's account became inactive."
    )
    user_posts = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="Amount of posts the user has posted"
    )
    user_lang = models.CharField(max_length=30,
        # varchar(30)
        help_text="The user's selected board language"
    )
    user_timezone = models.DecimalField(max_digits=7, decimal_places=2,
        # decimal(5,2)
        default=0,
        help_text="The user's timezone offset from UTC."
    )
    user_dst = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Is the user on Daylight Savings Time"
    )
    user_dateformat = models.CharField(max_length=30,
        # varchar(30)
        default="d M Y H:i",
        help_text="The user's desired date [http://www.php.net/function.date.php format]"
    )
    # user_style = models.IntegerField()
    user_style = models.ForeignKey("Styles", db_column="style_id", to_field="style_id",
        # tinyint(4)
        default=0,
        help_text="Style the user uses to browse the board. {{fk|styles|style_id}}"
    )
    # user_rank = models.IntegerField()
    user_rank = models.ForeignKey("Ranks", db_column="rank_id", to_field="rank_id",
        # mediumint(8) unsigned
        default=0,
        help_text="User's rank. {{fk|ranks|rank_id}}"
    )
    user_colour = models.CharField(max_length=6,
        # varchar(6)
        help_text="User's colour, hex code."
    )
    user_new_privmsg = models.IntegerField(
        # tinyint(4)
        default=0,
        help_text="The number of new private messages that the user has."
    )
    user_unread_privmsg = models.IntegerField(
        # tinyint(4)
        default=0,
        help_text="The number of unread private messages that the user has."
    )
    user_last_privmsg = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the user sent a private message. Used for flood checking."
    )
    user_message_rules = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating whether or not the user has custom rules for private messages."
    )
    user_full_folder = models.IntegerField(
        # int(11)
        default=-3,
        help_text="The action to take when a user's private message folder is full."
    )
    user_emailtime = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the time the user last sent an email. Used for flood checking."
    )
    user_topic_show_days = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
        help_text="The maximum age of a topic that should be shown."
    )
    user_topic_sortby_type = models.CharField(max_length=1,
        # char(1)
        default="t",
        help_text="Topic sort order. a is Author, r is Replies, t is Post Time, s is Subject, v is Views"
    )
    user_topic_sortby_dir = models.CharField(max_length=1,
        # char(1)
        default="d",
        help_text="Topic sort direction. a is ascending, d is descending"
    )
    user_post_show_days = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
        help_text="Preferences for reading "
    )
    user_post_sortby_type = models.CharField(max_length=1,
        # char(1)
        default="t",
        help_text="Post sort order. a is Author, s is subject, t is Post Time"
    )
    user_post_sortby_dir = models.CharField(max_length=1,
        # char(1)
        default="a",
        help_text="Post sort direction. a is ascending, d is descending"
    )
    user_notify = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating whether the user should be notified upon replies to a topic by default or not."
    )
    user_notify_pm = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user should be notified upon the arrival of new private messages."
    )
    user_notify_type = models.IntegerField(
        # tinyint(4)
        default=0,
        help_text="How the user should be notified for the above events: email, IM, or both"
    )
    user_allow_pm = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating whether the user wants to receive private messages from other users or not."
    )
    user_allow_viewonline = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user should be visible or hidden."
    )
    user_allow_viewemail = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user can be contacted via email through the board's email form."
    )
    user_allow_massemail = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user wishes to receive mass emails."
    )
    user_options = models.PositiveIntegerField(
        # int(11) unsigned
        default=230271,
        help_text="A bitfield containing the options for: showing images in posts, showing flash in posts, showing similies in posts, showing signatures, showing avatars, enable word censoring, attach signature by default, enable bbcodes by default, enable smilies by default, show a popup for new private messages, enable bbcode in signature, enable smilies in signature, automatically parse links in signature"
    )
    user_avatar = models.CharField(max_length=255,
        # varchar(255)
        help_text="Avatar's file name. URI for remote avatar, file directory and name for gallery avatar, combination of user id and time stamp for uploaded avatar."
    )
    user_avatar_type = models.IntegerField(
        # tinyint(2)
        default=0,
        help_text="The type of avatar the user has: remote, gallery, or uploaded"
    )
    user_avatar_width = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
        help_text="Width of the avatar"
    )
    user_avatar_height = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
        help_text="Height of the avatar"
    )
    user_sig = models.TextField(
        # mediumtext
        help_text="The user's signature"
    )
    user_sig_bbcode_uid = models.CharField(max_length=8,
        # varchar(5)
        help_text="The bbcode uid used in the user's signature."
    )
    user_sig_bbcode_bitfield = models.CharField(max_length=255,
        # varchar(255)
        help_text="The bbcode, smiley, and url settings used when saving the user's signature."
    )
    user_from = models.CharField(max_length=100,
        # varchar(100)
        help_text="User's location field value"
    )
    user_icq = models.CharField(max_length=15,
        # varchar(15)
        help_text="User's ICQ field value"
    )
    user_aim = models.CharField(max_length=255,
        # varchar(255)
        help_text="User's AIM field value"
    )
    user_yim = models.CharField(max_length=255,
        # varchar(255)
        help_text="User's YIM field value"
    )
    user_msnm = models.CharField(max_length=255,
        # varchar(255)
        help_text="User's MSN field value"
    )
    user_jabber = models.CharField(max_length=255,
        # varchar(255)
        help_text="User's Jabber field value"
    )
    user_website = models.CharField(max_length=200,
        # varchar(200)
        help_text="User's website field value"
    )
    user_occ = models.TextField(
        # text
        help_text="User's occupation field value"
    )
    user_interests = models.TextField(
        # text
        help_text="User's interests field value"
    )
    user_actkey = models.CharField(max_length=32,
        # varchar(32)
        help_text="The key required to activate the user's account."
    )
    user_newpasswd = models.CharField(max_length=40,
        # varchar(32)
        help_text="A randomly generated password for when the user has forgotten their password."
    )
    user_form_salt = models.CharField(max_length=32)
    user_new = models.IntegerField()
    user_reminded = models.IntegerField()
    user_reminded_time = models.IntegerField()
    def __unicode__(self):
            return self.username
    class Meta:
        db_table = u'phpbb3_users'


class Group(models.Model):
    """
    Usergroups
    """
    group_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    group_type = models.IntegerField(
        # tinyint(4)
        default=1,
    )
    group_founder_manage = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    group_skip_auth = models.IntegerField()
    group_name = models.CharField(max_length=255,
        # varchar(255)
    )
    group_desc = models.TextField(
        # text
    )
    group_desc_bitfield = models.CharField(max_length=255,
        # varchar(255)
    )
    group_desc_options = models.PositiveIntegerField(
        # int(11) unsigned
        default=7,
    )
    group_desc_uid = models.CharField(max_length=8,
        # varchar(5)
    )
    group_display = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    group_avatar = models.CharField(max_length=255,
        # varchar(255)
    )
    group_avatar_type = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    group_avatar_width = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    group_avatar_height = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    group_rank = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    group_colour = models.CharField(max_length=6,
        # varchar(6)
    )
    group_sig_chars = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    group_receive_pm = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    group_message_limit = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    group_max_recipients = models.IntegerField()
    group_legend = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    def __unicode__(self):
            return self.group_name
    class Meta:
        db_table = u'phpbb3_groups'


class Config(models.Model):
    """
    Configuration information ($config table)
    """
    config_name = models.CharField(max_length=255, primary_key=True,
        # varchar(255)
        help_text="primary key"
    )
    config_value = models.CharField(max_length=255,
        # varchar(255)
        help_text="Value of config"
    )
    is_dynamic = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Is dynamic?"
    )
    def __unicode__(self):
            return u"%s: %s" % (self.config_name, self.config_value)
    class Meta:
        db_table = u'phpbb3_config'

#______________________________________________________________________________
# untouched models:

class AclOptions(models.Model):
    """
    List of possible permissions
    """
    auth_option_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    auth_option = models.CharField(max_length=50, unique=True,
        # varchar(50)
        help_text="the name of the permission, e.g. 'f_post'"
    )
    is_global = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="this permission can be granted globally (once for all forums)"
    )
    is_local = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="this permission can be granted locally (individual setting for each forum)"
    )
    founder_only = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="only founders can have this permission"
    )
    class Meta:
        db_table = u'phpbb3_acl_options'

class AclRoles(models.Model):
    """
    Permission roles (Standard Moderator, Simple Moderator etc.)
    """
    role_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    role_name = models.CharField(max_length=255,
        # varchar(255)
        help_text="Name of this role, can also be a language string"
    )
    role_description = models.TextField(
        # text
        help_text="description of this role, can also be a language string"
    )
    role_type = models.CharField(max_length=10,
        # varchar(10)
    )
    role_order = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_acl_roles'

class AclRolesData(models.Model):
    """
    Permissions each role contains
    """
    role_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    auth_option_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    auth_setting = models.IntegerField(
        # tinyint(2)
        default=0,
        help_text="ACL_YES, ACL_NO or ACL_NEVER"
    )
    class Meta:
        db_table = u'phpbb3_acl_roles_data'

class AclUsers(models.Model):
    """
    Permission roles and/or individual permissions assigned to users
    """
    # user_id = models.IntegerField()
    user_id = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    # forum_id = models.IntegerField()
    forum_id = models.ForeignKey("Forums", db_column="forum_id", to_field="forum_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|forums|forum_id}}"
    )
    # auth_option_id = models.IntegerField()
    auth_option_id = models.ForeignKey("Acl_options", db_column="auth_option_id", to_field="auth_option_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|acl_options|auth_option_id}}"
    )
    # auth_role_id = models.IntegerField()
    auth_role_id = models.ForeignKey("Acl_roles", db_column="role_id", to_field="role_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|acl_roles|role_id}}"
    )
    auth_setting = models.IntegerField(
        # tinyint(2)
        default=0,
        help_text="ACL_YES, ACL_NO or ACL_NEVER "
    )
    class Meta:
        db_table = u'phpbb3_acl_users'

class Attachments(models.Model):
    """
    Information on attachments (Post, physical filename, original filename, MIME type...)
    """
    attach_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    # post_msg_id = models.IntegerField()
    post_msg_id = models.ForeignKey("Posts", db_column="post_id", to_field="post_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|posts|post_id}}"
    )
    # topic_id = models.IntegerField()
    topic_id = models.ForeignKey("Topics", db_column="topic_id", to_field="topic_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|topics|topic_id}}"
    )
    in_message = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="1 if attachment is used inside private message, 0 if used inside post"
    )
    # poster_id = models.IntegerField()
    poster_id = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    is_orphan = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="1 if attachment is unused (user left posting.php without submiting post)"
    )
    physical_filename = models.CharField(max_length=255,
        # varchar(255)
        help_text="name of the file stored inside the $config['upload_path'] directory"
    )
    real_filename = models.CharField(max_length=255,
        # varchar(255)
        help_text="name of the file before the user uploaded it"
    )
    download_count = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="how many times was this attachment downloaded/viewed"
    )
    attach_comment = models.TextField(
        # text
        help_text="comment"
    )
    extension = models.CharField(max_length=100,
        # varchar(100)
        help_text="self explaining"
    )
    mimetype = models.CharField(max_length=100,
        # varchar(100)
        help_text="[[wikipedia:mime-type|mime-type]]"
    )
    filesize = models.PositiveIntegerField(
        # int(20) unsigned
        default=0,
        help_text="file size in bytes"
    )
    filetime = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="unix timestamp"
    )
    thumbnail = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="has this attachment a thumbnail (1/0)? The thumbnails physical filename is prefixed with thumb_"
    )
    class Meta:
        db_table = u'phpbb3_attachments'

class Banlist(models.Model):
    """
    Banned users/IPs/emails...
    """
    ban_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    ban_userid = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    ban_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    ban_email = models.CharField(max_length=100,
        # varchar(100)
    )
    ban_start = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    ban_end = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    ban_exclude = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    ban_reason = models.CharField(max_length=255,
        # text
    )
    ban_give_reason = models.CharField(max_length=255,
        # text
    )
    class Meta:
        db_table = u'phpbb3_banlist'

class Bbcodes(models.Model):
    """
    Custom BBCodes
    """
    bbcode_id = models.IntegerField(primary_key=True,
        # tinyint(3)
        default=0,
        help_text="primary key"
    )
    bbcode_tag = models.CharField(max_length=16,
        # varchar(16)
    )
    bbcode_helpline = models.CharField(max_length=255,
        # varchar(255)
    )
    display_on_posting = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    bbcode_match = models.TextField(
        # text
    )
    bbcode_tpl = models.TextField(
        # mediumtext
    )
    first_pass_match = models.TextField(
        # mediumtext
    )
    first_pass_replace = models.TextField(
        # mediumtext
    )
    second_pass_match = models.TextField(
        # mediumtext
    )
    second_pass_replace = models.TextField(
        # mediumtext
    )
    class Meta:
        db_table = u'phpbb3_bbcodes'

class Bookmarks(models.Model):
    """
    Bookmarked topics
    """
    topic_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
    )
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_bookmarks'

class Bots(models.Model):
    """
    Spiders/Robots
    """
    bot_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    bot_active = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    bot_name = models.CharField(max_length=255,
        # varchar(255)
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    bot_agent = models.CharField(max_length=255,
        # varchar(255)
    )
    bot_ip = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_bots'

class CaptchaAnswers(models.Model):
    question_id = models.IntegerField()
    answer_text = models.CharField(max_length=255)
    class Meta:
        db_table = u'phpbb3_captcha_answers'

class CaptchaQuestions(models.Model):
    question_id = models.IntegerField(primary_key=True)
    strict = models.IntegerField()
    lang_id = models.IntegerField()
    lang_iso = models.CharField(max_length=30)
    question_text = models.TextField()
    class Meta:
        db_table = u'phpbb3_captcha_questions'

class Confirm(models.Model):
    """
    Contains session information for confirm pages ("are you sure you want to delete foo")
    """
    confirm_id = models.CharField(max_length=96, primary_key=True,
        # char(32)
        help_text="primary key"
    )
    session_id = models.CharField(max_length=96, primary_key=True,
        # char(32)
        help_text="primary key, The session ID associated with the registration attempt."
    )
    confirm_type = models.IntegerField(
        # tinyint(3)
        default=0,
        help_text="Where the CAPTCHA was generated (registration, login, or posting)."
    )
    code = models.CharField(max_length=8,
        # varchar(8)
        help_text="The character code that will be displayed for the user to confirm. This will be used to cross-check the user entry during registration and deny the attempt if it does not match."
    )
    seed = models.IntegerField(
        # int(10)
        default=0,
        help_text="The seed that should be used to initialized the random number generator for the image generation."
    )
    attempts = models.IntegerField(
        # mediumint(8)
        default=0,
        help_text="The number of attempts that have been made at solving the CAPTCHA"
    )
    class Meta:
        db_table = u'phpbb3_confirm'

class Disallow(models.Model):
    """
    Disallowed usernames
    """
    disallow_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    disallow_username = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_disallow'

class Drafts(models.Model):
    """
    Drafts of future posts/private messages
    """
    draft_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    forum_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    save_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    draft_subject = models.CharField(max_length=255,
        # varchar(100)
    )
    draft_message = models.TextField(
        # mediumtext
    )
    class Meta:
        db_table = u'phpbb3_drafts'

class ExtensionGroups(models.Model):
    """
    Extensions Groups (associate extensions with a file type - Images, text...)
    """
    group_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    group_name = models.CharField(max_length=255,
        # varchar(255)
    )
    cat_id = models.IntegerField(
        # tinyint(2)
        default=0,
    )
    allow_group = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    download_mode = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    upload_icon = models.CharField(max_length=255,
        # varchar(255)
    )
    max_filesize = models.PositiveIntegerField(
        # int(20) unsigned
        default=0,
    )
    allowed_forums = models.TextField(
        # text
    )
    allow_in_pm = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_extension_groups'

class Extensions(models.Model):
    """
    Extensions (.xxx) allowed for attachments
    """
    extension_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    group_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    extension = models.CharField(max_length=100,
        # varchar(100)
    )
    class Meta:
        db_table = u'phpbb3_extensions'

class Forums(models.Model):
    """
    Forums (Name, description, rules...)
    """
    forum_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    parent_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="the forum_id of the parent forum (or category)"
    )
    left_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="forum_id of the forum left to the current forum in the binary tree (used e. g. to retrieve the list of all parents very fast to create the forum navigation)"
    )
    right_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="forum_id of the forum right to the current forum in the binary tree (used e. g. to retrieve the list of all parents very fast to create the forum navigation)"
    )
    forum_parents = models.TextField(
        # mediumtext
        help_text="Holds an serialized array of parent forums name, id "
    )
    forum_name = models.CharField(max_length=255,
        # varchar(255)
    )
    forum_desc = models.TextField(
        # text
    )
    forum_desc_bitfield = models.CharField(max_length=255,
        # varchar(255)
        help_text="see [[Parsing text]]"
    )
    forum_desc_options = models.PositiveIntegerField(
        # int(11) unsigned
        default=7,
        help_text="see [[Parsing text]]"
    )
    forum_desc_uid = models.CharField(max_length=8,
        # varchar(5)
        help_text="see [[Parsing text]]"
    )
    forum_link = models.CharField(max_length=255,
        # varchar(255)
    )
    forum_password = models.CharField(max_length=40,
        # varchar(40)
    )
    forum_style = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    forum_image = models.CharField(max_length=255,
        # varchar(255)
    )
    forum_rules = models.TextField(
        # text
    )
    forum_rules_link = models.CharField(max_length=255,
        # varchar(255)
    )
    forum_rules_bitfield = models.CharField(max_length=255,
        # varchar(255)
        help_text="see [[Parsing text]]"
    )
    forum_rules_options = models.PositiveIntegerField(
        # int(11) unsigned
        default=7,
        help_text="see [[Parsing text]]"
    )
    forum_rules_uid = models.CharField(max_length=8,
        # varchar(5)
        help_text="see [[Parsing text]]"
    )
    forum_topics_per_page = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    forum_type = models.IntegerField(
        # tinyint(4)
        default=0,
        help_text="category (forum_type = FORUM_CAT = 0) or forum (forum_type = FORUM_POST = 1) or link (forum_type = FORUM_LINK = 2)"
    )
    forum_status = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    forum_posts = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    forum_topics = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="Number of topics in a forum."
    )
    forum_topics_real = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="Number of topics in a forum. Includes unapproved topics."
    )
    forum_last_post_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    forum_last_poster_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    forum_last_post_subject = models.CharField(max_length=255,
        # varchar(100)
    )
    forum_last_post_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    forum_last_poster_name = models.CharField(max_length=255,
        # varchar(255)
    )
    forum_last_poster_colour = models.CharField(max_length=6,
        # varchar(6)
    )
    forum_flags = models.IntegerField(
        # tinyint(4)
        default=32,
    )
    forum_options = models.IntegerField()
    display_subforum_list = models.IntegerField()
    display_on_index = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    enable_indexing = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    enable_icons = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    enable_prune = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    prune_next = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    prune_days = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    prune_viewed = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    prune_freq = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_forums'

class ForumsAccess(models.Model):
    """
    Stores who is logged in to password protected forums
    """
    forum_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    session_id = models.CharField(max_length=96, primary_key=True,
        # char(32) binary
        help_text="primary key"
    )
    class Meta:
        db_table = u'phpbb3_forums_access'

class ForumsTrack(models.Model):
    """
    Unread post information is stored here
    """
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    forum_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    mark_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_forums_track'

class ForumsWatch(models.Model):
    """
    Subscribed forums
    """
    forum_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    notify_status = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_forums_watch'

class Icons(models.Model):
    """
    Post icons
    """
    icons_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    icons_url = models.CharField(max_length=255,
        # varchar(255)
    )
    icons_width = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    icons_height = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    icons_order = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    display_on_posting = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    class Meta:
        db_table = u'phpbb3_icons'

class Lang(models.Model):
    """
    Installed languages
    """
    lang_id = models.IntegerField(primary_key=True,
        # tinyint(4)
        help_text="primary key"
    )
    lang_iso = models.CharField(max_length=30,
        # varchar(30)
    )
    lang_dir = models.CharField(max_length=30,
        # varchar(30)
    )
    lang_english_name = models.CharField(max_length=100,
        # varchar(100)
    )
    lang_local_name = models.CharField(max_length=255,
        # varchar(255)
    )
    lang_author = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_lang'

class Log(models.Model):
    """
    Administration/Moderation/Error logs
    """
    log_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    log_type = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    forum_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    reportee_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    log_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    log_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    log_operation = models.TextField(
        # text
    )
    log_data = models.TextField(
        # mediumtext
    )
    class Meta:
        db_table = u'phpbb3_log'

class LoginAttempts(models.Model):
    """
    tbd
    """
    attempt_ip = models.CharField(max_length=40)
    attempt_browser = models.CharField(max_length=150)
    attempt_forwarded_for = models.CharField(max_length=255)
    attempt_time = models.IntegerField()
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    username_clean = models.CharField(max_length=255)
    class Meta:
        db_table = u'phpbb3_login_attempts'

class ModeratorCache(models.Model):
    """
    Who is a moderator in which forum (for display on forum index)
    """
    forum_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    username = models.CharField(max_length=255,
        # varchar(255)
    )
    group_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    group_name = models.CharField(max_length=255,
        # varchar(255)
    )
    display_on_index = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    class Meta:
        db_table = u'phpbb3_moderator_cache'

class Modules(models.Model):
    """
    Configuration of acp, mcp and ucp modules
    """
    module_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    module_enabled = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    module_display = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    module_basename = models.CharField(max_length=255,
        # varchar(255)
    )
    module_class = models.CharField(max_length=10,
        # varchar(10)
    )
    parent_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    left_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    right_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    module_langname = models.CharField(max_length=255,
        # varchar(255)
    )
    module_mode = models.CharField(max_length=255,
        # varchar(255)
    )
    module_auth = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_modules'

class PollOptions(models.Model):
    """
    Options text of all votes ("Yes", "No", "Maybe"...)
    """
    poll_option_id = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    poll_option_text = models.TextField(
        # text
    )
    poll_option_total = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_poll_options'

class PollVotes(models.Model):
    """
    Users which have voted on a poll
    """
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    poll_option_id = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    vote_user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    vote_user_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    class Meta:
        db_table = u'phpbb3_poll_votes'

class Posts(models.Model):
    """
    Topics posts
    """
    post_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    forum_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    poster_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    icon_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    poster_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    post_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    post_approved = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    post_reported = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    enable_bbcode = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    enable_smilies = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    enable_magic_url = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    enable_sig = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    post_username = models.CharField(max_length=255,
        # varchar(255)
    )
    post_subject = models.CharField(max_length=255,
        # varchar(100)
    )
    post_text = models.TextField(
        # mediumtext
    )
    post_checksum = models.CharField(max_length=32,
        # varchar(32)
    )
    post_attachment = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="| 1=This post has at least one attachment&lt;br/>0=no attachments in this post"
    )
    bbcode_bitfield = models.CharField(max_length=255,
        # varchar(255)
        help_text="see [[Parsing text]]"
    )
    bbcode_uid = models.CharField(max_length=8,
        # varchar(5)
        help_text="see [[Parsing text]]"
    )
    post_postcount = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    post_edit_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    post_edit_reason = models.CharField(max_length=255,
        # varchar(255)
    )
    post_edit_user = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    post_edit_count = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
    )
    post_edit_locked = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_posts'

class Privmsgs(models.Model):
    """
    Private messages text
    """
    msg_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    root_level = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="the initial message in this message chain (i.e. if you write messages A -> B (reply to A) -> C (reply to B), then B and C will have root_level=msg_id of A"
    )
    # author_id = models.IntegerField()
    author_id = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    # icon_id = models.IntegerField()
    icon_id = models.ForeignKey("Icons", db_column="icons_id", to_field="icons_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|icons|icons_id}}"
    )
    author_ip = models.CharField(max_length=40,
        # varchar(40)
        help_text="ip address of sender"
    )
    message_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="unix timestamp"
    )
    enable_bbcode = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="bbcode enabled? 1/0"
    )
    enable_smilies = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="smilies enabled? 1/0"
    )
    enable_magic_url = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="automatically convert urls to links? 1/0"
    )
    enable_sig = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="attach signature? 1/0"
    )
    message_subject = models.CharField(max_length=255,
        # varchar(100)
        help_text="subject"
    )
    message_text = models.TextField(
        # mediumtext
        help_text="the message itself"
    )
    message_edit_reason = models.CharField(max_length=255,
        # varchar(255)
        help_text="reason for editing"
    )
    message_edit_user = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="who edited this message"
    )
    message_attachment = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="does the message have files attached? 1/0"
    )
    bbcode_bitfield = models.CharField(max_length=255,
        # varchar(255)
        help_text="see [[Parsing text]]"
    )
    bbcode_uid = models.CharField(max_length=8,
        # varchar(5)
        help_text="see [[Parsing text]]"
    )
    message_edit_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    message_edit_count = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
    )
    to_address = models.TextField(
        # text
        help_text="colon separated list of recipients, e.g. u_1:u_23:g_5"
    )
    bcc_address = models.TextField(
        # text
        help_text="see to_address"
    )
    message_reported = models.IntegerField()
    class Meta:
        db_table = u'phpbb3_privmsgs'

class PrivmsgsFolder(models.Model):
    """
    Custom privates messages folders (for each user)
    """
    folder_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    folder_name = models.CharField(max_length=255,
        # varchar(255)
    )
    pm_count = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_privmsgs_folder'

class PrivmsgsRules(models.Model):
    """
    Messages rules, e.g. "if the username of the sender is ..., move the message to this folder".
    """
    rule_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    rule_check = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    rule_connection = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    rule_string = models.CharField(max_length=255,
        # varchar(255)
    )
    rule_user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    rule_group_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    rule_action = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    rule_folder_id = models.IntegerField(
        # int(4)
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_privmsgs_rules'

class PrivmsgsTo(models.Model):
    """
    Information (sender, new, replied...) on private messages.
    """
    msg_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="user_id of recipient"
    )
    author_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="user_id of sender when in inbox or in no_box"
    )
    pm_deleted = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    pm_new = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="new = 1"
    )
    pm_unread = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="unread = 1"
    )
    pm_replied = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="replied = 1"
    )
    pm_marked = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    pm_forwarded = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    folder_id = models.IntegerField(
        # int(4)
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_privmsgs_to'

class ProfileFields(models.Model):
    """
    Custom profile fields (name, min/max number of characters, allowed characters...)
    """
    field_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    field_name = models.CharField(max_length=255,
        # varchar(255)
    )
    field_type = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    field_ident = models.CharField(max_length=20,
        # varchar(20)
    )
    field_length = models.CharField(max_length=20,
        # varchar(20)
    )
    field_minlen = models.CharField(max_length=255,
        # varchar(255)
    )
    field_maxlen = models.CharField(max_length=255,
        # varchar(255)
    )
    field_novalue = models.CharField(max_length=255,
        # varchar(255)
    )
    field_default_value = models.CharField(max_length=255,
        # varchar(255)
    )
    field_validation = models.CharField(max_length=20,
        # varchar(20)
    )
    field_required = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    field_show_on_reg = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    field_show_on_vt = models.IntegerField()
    field_show_profile = models.IntegerField()
    field_hide = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    field_no_view = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    field_active = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    field_order = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_profile_fields'

class ProfileFieldsData(models.Model):
    """
    Data that users enter in custom profile fields
    """
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    class Meta:
        db_table = u'phpbb3_profile_fields_data'

class ProfileFieldsLang(models.Model):
    """
    tbd (empty on my forum with some custom profile fields)
    """
    field_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    lang_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    option_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    field_type = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    lang_value = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_profile_fields_lang'

class ProfileLang(models.Model):
    """
    Localized name and description of custom profile fields (presented to users)
    """
    field_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    lang_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    lang_name = models.CharField(max_length=255,
        # varchar(255)
    )
    lang_explain = models.TextField(
        # text
    )
    lang_default_value = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_profile_lang'

class QaConfirm(models.Model):
    session_id = models.CharField(max_length=96)
    confirm_id = models.CharField(max_length=96)
    lang_iso = models.CharField(max_length=30)
    question_id = models.IntegerField()
    attempts = models.IntegerField()
    confirm_type = models.IntegerField()
    class Meta:
        db_table = u'phpbb3_qa_confirm'

class Ranks(models.Model):
    """
    Ranks (Name, image, minimal # of posts)
    """
    rank_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    rank_title = models.CharField(max_length=255,
        # varchar(255)
    )
    rank_min = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    rank_special = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    rank_image = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_ranks'

class Reports(models.Model):
    """
    Reported posts
    """
    report_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    reason_id = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
    )
    post_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    pm_id = models.IntegerField()
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user_notify = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    report_closed = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    report_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    report_text = models.TextField(
        # mediumtext
    )
    class Meta:
        db_table = u'phpbb3_reports'

class ReportsReasons(models.Model):
    """
    Reasons for reported posts and disapprovals
    """
    reason_id = models.PositiveIntegerField(primary_key=True,
        # smallint(4) unsigned
        help_text="primary key"
    )
    reason_title = models.CharField(max_length=255,
        # varchar(255)
    )
    reason_description = models.TextField(
        # mediumtext
    )
    reason_order = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_reports_reasons'

class SearchResults(models.Model):
    """
    Last searches
    """
    search_key = models.CharField(max_length=32, primary_key=True,
        # varchar(32)
        help_text="primary key"
    )
    search_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    search_keywords = models.TextField(
        # mediumtext
    )
    search_authors = models.TextField(
        # mediumtext
    )
    class Meta:
        db_table = u'phpbb3_search_results'

class SearchWordlist(models.Model):
    """
    Indexed words (for search)
    """
    word_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    word_text = models.CharField(max_length=255, unique=True,
        # varchar(255)
    )
    word_common = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    word_count = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_search_wordlist'

class SearchWordmatch(models.Model):
    """
    Associate a post with indexed words
    """
    post_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    word_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    title_match = models.PositiveSmallIntegerField(unique=True,
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_search_wordmatch'

class Sessions(models.Model):
    """
    Sessions (to identify users browsing the forum)
    """
    session_id = models.CharField(max_length=96, primary_key=True,
        # varchar(32)
        help_text="primary key"
    )
    session_user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    session_forum_id = models.IntegerField()
    session_last_visit = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    session_start = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    session_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    session_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    session_browser = models.CharField(max_length=150,
        # varchar(150)
    )
    session_forwarded_for = models.CharField(max_length=255)
    session_page = models.CharField(max_length=255,
        # varchar(255)
    )
    session_viewonline = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    session_autologin = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    session_admin = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_sessions'

class SessionsKeys(models.Model):
    """
    Autologin feature
    """
    key_id = models.CharField(max_length=96, primary_key=True,
        # varchar(32)
        help_text="primary key"
    )
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    last_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    last_login = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_sessions_keys'

class Sitelist(models.Model):
    """
    Secure Downloads of attachments - list of IPs and hostnames
    """
    site_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    site_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    site_hostname = models.CharField(max_length=255,
        # varchar(255)
    )
    ip_exclude = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_sitelist'

class Smilies(models.Model):
    """
    Smilies (text => image)
    """
    smiley_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    code = models.CharField(max_length=50,
        # varchar(50)
    )
    emotion = models.CharField(max_length=50,
        # varchar(50)
    )
    smiley_url = models.CharField(max_length=50,
        # varchar(50)
    )
    smiley_width = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
    )
    smiley_height = models.PositiveIntegerField(
        # smallint(4) unsigned
        default=0,
    )
    smiley_order = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    display_on_posting = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    class Meta:
        db_table = u'phpbb3_smilies'

class Styles(models.Model):
    """
    Style = template + theme + imageset
    """
    style_id = models.IntegerField(primary_key=True,
        # tinyint(4)
        help_text="primary key"
    )
    style_name = models.CharField(max_length=255, unique=True,
        # varchar(255)
    )
    style_copyright = models.CharField(max_length=255,
        # varchar(255)
    )
    style_active = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
    )
    template_id = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    theme_id = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    imageset_id = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_styles'

class StylesImageset(models.Model):
    """
    [[Templating_Tutorial#Customizing_the_Imageset|Imagesets]]
    """
    imageset_id = models.IntegerField(primary_key=True,
        # tinyint(4)
        help_text="primary key"
    )
    imageset_name = models.CharField(max_length=255, unique=True,
        # varchar(255)
    )
    imageset_copyright = models.CharField(max_length=255,
        # varchar(255)
    )
    imageset_path = models.CharField(max_length=100,
        # varchar(100)
    )
    class Meta:
        db_table = u'phpbb3_styles_imageset'

class StylesImagesetData(models.Model):
    """
    tbd
    """
    image_id = models.IntegerField(primary_key=True)
    image_name = models.CharField(max_length=200)
    image_filename = models.CharField(max_length=200)
    image_lang = models.CharField(max_length=30)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    imageset_id = models.IntegerField()
    class Meta:
        db_table = u'phpbb3_styles_imageset_data'

class StylesTemplate(models.Model):
    """
    tbd
    """
    template_id = models.IntegerField(primary_key=True,
        # tinyint(4)
        help_text="primary key"
    )
    template_name = models.CharField(max_length=255, unique=True,
        # varchar(255)
    )
    template_copyright = models.CharField(max_length=255,
        # varchar(255)
    )
    template_path = models.CharField(max_length=100,
        # varchar(100)
    )
    bbcode_bitfield = models.CharField(max_length=255,
        # varchar(255)
        default="kNg=",
    )
    template_storedb = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    template_inherits_id = models.IntegerField()
    template_inherit_path = models.CharField(max_length=255)
    class Meta:
        db_table = u'phpbb3_styles_template'

class StylesTemplateData(models.Model):
    """
    tbd
    """
    template_id = models.IntegerField(
        # tinyint(4)
    )
    template_filename = models.CharField(max_length=100,
        # varchar(100)
    )
    template_included = models.TextField(
        # text
    )
    template_mtime = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    template_data = models.TextField(
        # mediumtext
    )
    class Meta:
        db_table = u'phpbb3_styles_template_data'

class StylesTheme(models.Model):
    """
    theme = css file
    """
    theme_id = models.IntegerField(primary_key=True,
        # tinyint(4)
        help_text="primary key"
    )
    theme_name = models.CharField(max_length=255, unique=True,
        # varchar(255)
    )
    theme_copyright = models.CharField(max_length=255,
        # varchar(255)
    )
    theme_path = models.CharField(max_length=100,
        # varchar(100)
    )
    theme_storedb = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    theme_mtime = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    theme_data = models.TextField(
        # mediumtext
    )
    class Meta:
        db_table = u'phpbb3_styles_theme'

class Topics(models.Model):
    """
    Topics in forums
    """
    topic_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="Primary key"
    )
    # forum_id = models.IntegerField()
    forum_id = models.ForeignKey("Forums", db_column="forum_id", to_field="forum_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|forums|forum_id}}"
    )
    # icon_id = models.IntegerField()
    icon_id = models.ForeignKey("Icons", db_column="icon_id", to_field="icon_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|icons|icon_id}}"
    )
    topic_attachment = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="1=at least one post in this topic has an attachment&lt;br/>0=no attachments in this topic"
    )
    topic_approved = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating whether the topic is awaiting approval or not."
    )
    topic_reported = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating that a post within the topic has been reported."
    )
    topic_title = models.CharField(max_length=255,
        # varchar(100)
        help_text="The title of the topic."
    )
    # topic_poster = models.IntegerField()
    topic_poster = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    topic_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the topic's creation date."
    )
    topic_time_limit = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="The number of seconds that a topic will remain as a sticky."
    )
    topic_views = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="The number of time the topic has been viewed."
    )
    topic_replies = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="The number of approved replies to this topic."
    )
    topic_replies_real = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="Total number of replies to this topic (including posts waiting for approval)."
    )
    topic_status = models.IntegerField(
        # tinyint(3)
        default=0,
        help_text="[[Constants|ITEM_UNLOCKED]](0), ITEM_LOCKED(1) or ITEM_MOVED(2)"
    )
    topic_type = models.IntegerField(
        # tinyint(3)
        default=0,
        help_text="[[Constants|POST_NORMAL]](0), POST_STICKY(1), POST_ANNOUNCE(2) or POST_GLOBAL(3)"
    )
    # topic_first_post_id = models.IntegerField()
    topic_first_post_id = models.ForeignKey("Posts", db_column="post_id", to_field="post_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|posts|post_id}}"
    )
    topic_first_poster_name = models.CharField(max_length=255,
        # varchar(255)
        help_text="The topic creator's username."
    )
    topic_first_poster_colour = models.CharField(max_length=6,
        # varchar(6)
        help_text="The colour of the topic creator's default user group."
    )
    # topic_last_post_id = models.IntegerField()
    topic_last_post_id = models.ForeignKey("Posts", db_column="post_id", to_field="post_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|posts|post_id}}"
    )
    # topic_last_poster_id = models.IntegerField()
    topic_last_poster_id = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    topic_last_poster_name = models.CharField(max_length=255,
        # varchar(255)
        help_text="The username of the topic's last poster."
    )
    topic_last_poster_colour = models.CharField(max_length=6,
        # varchar(6)
        help_text="The colour of the last poster's default user group."
    )
    topic_last_post_subject = models.CharField(max_length=255,
        # varchar(100)
        help_text="The subject of the topic's last post"
    )
    topic_last_post_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time a post was made in the topic."
    )
    topic_last_view_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the topic was viewed. Used in topic pruning."
    )
    topic_moved_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="If topic_status is ITEM_MOVED (a shadow topic), this field contains the topic id of the real topic."
    )
    topic_bumped = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Has this topic been bumped? 1 (yes), 0(no)"
    )
    # topic_bumper = models.IntegerField()
    topic_bumper = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    poll_title = models.CharField(max_length=255,
        # varchar(100)
        help_text="The poll's question"
    )
    poll_start = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, poll's creation date"
    )
    poll_length = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Poll duration, in seconds"
    )
    poll_max_options = models.IntegerField(
        # tinyint(4)
        default=1,
        help_text="The number of poll options a user can choose when casting a vote"
    )
    poll_last_vote = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, time of the last vote"
    )
    poll_vote_change = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="Are users allowed to change their vote(s)? 1 (yes), 0(no)"
    )
    class Meta:
        db_table = u'phpbb3_topics'

class TopicsPosted(models.Model):
    """
    Who posted to which topic (used for the small dots in viewforum)
    """
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    topic_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    topic_posted = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_topics_posted'

class TopicsTrack(models.Model):
    """
    Unread post information is stored here
    """
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        help_text="primary key"
    )
    forum_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
    )
    mark_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_topics_track'

class TopicsWatch(models.Model):
    """
    "notify me upon replies"
    """
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    notify_status = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_topics_watch'

class UserGroup(models.Model):
    """
    Users groups
    """
    # group_id = models.IntegerField()
    group_id = models.ForeignKey("Groups", db_column="group_id", to_field="group_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|groups|group_id}}"
    )
    # user_id = models.IntegerField()
    user_id = models.ForeignKey("Users", db_column="user_id", to_field="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    group_leader = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
        help_text="1 (true) if this user is a group leader"
    )
    user_pending = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=1,
        help_text="1 (true) if the user is waiting for approval"
    )
    class Meta:
        db_table = u'phpbb3_user_group'

class Warnings(models.Model):
    """
    Warnings given to users
    """
    warning_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    post_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    log_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    warning_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_warnings'

class Words(models.Model):
    """
    censored words
    """
    word_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        help_text="primary key"
    )
    word = models.CharField(max_length=255,
        # varchar(255)
    )
    replacement = models.CharField(max_length=255,
        # varchar(255)
    )
    class Meta:
        db_table = u'phpbb3_words'

class Zebra(models.Model):
    """
    Friends and foes
    """
    user_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
    )
    zebra_id = models.PositiveIntegerField(primary_key=True,
        # mediumint(8) unsigned
        default=0,
    )
    friend = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    foe = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u'phpbb3_zebra'

