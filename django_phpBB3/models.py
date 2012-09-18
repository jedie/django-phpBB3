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

import datetime
import re

from django.conf import settings
from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.tzinfo import FixedOffset

from django_phpBB3.utils import clean_bbcode, deentity


def timestamp2datetime(timestamp, timezone=None):
    """
    convert the phpBB timestamp into a datetime with tzinfo
    FIXME: Don't know if timezone handling is correct
    """
    if timestamp == 0:
        return None

    if timezone is None:
        tzinfo = FixedOffset(0)
    else:
        offset_minutes = int(timezone) * 60
        tzinfo = FixedOffset(offset_minutes)

    return datetime.datetime.fromtimestamp(timestamp, tzinfo)



class PhpBBReverseSingleRelatedObjectDescriptor(models.fields.related.ReverseSingleRelatedObjectDescriptor):
    """
    Same as original, but accepts 0 also as none related objects.
    """
    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        try:
            return getattr(instance, self.cache_name)
        except AttributeError:
            val = getattr(instance, self.field.attname)
            if val in (0, None, ""):
                return None

        return super(PhpBBReverseSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)


class PhpBBForeignKey(models.ForeignKey):
    """
    phpBB stores a None ForeignKey as a numeric 0
    """
    def __init__(self, *args, **kwargs):
        kwargs2 = {
            "blank": True, "null": True,
            "default": 0,
        }
        kwargs2.update(kwargs)
        super(PhpBBForeignKey, self).__init__(*args, **kwargs2)

    def to_python(self, value):
        if value in ("", None, 0):
            return None
        return super(PhpBBForeignKey, self).to_python(value)

    def get_db_prep_save(self, value, connection):
        if value in ("", None, 0):
            return None
        return super(PhpBBForeignKey, self).get_db_prep_save(value, connection)

    def contribute_to_class(self, cls, name):
        super(PhpBBForeignKey, self).contribute_to_class(cls, name)
        setattr(cls, self.name, PhpBBReverseSingleRelatedObjectDescriptor(self))

#------------------------------------------------------------------------------
# important models first:

class User(models.Model):
    """
    Registered users
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        help_text="Primary key"
    )
    type = models.IntegerField(db_column="user_type",
        # tinyint(2)
        default=0,
        help_text="Defines what type the user is. 0 is normal user, 1 is inactive and needs to activate their account through an activation link sent in an email, 2 is a pre-defined type to ignore user (i.e. bot), 3 is Founder."
    )
    # group = models.ForeignKey("Group",
    group = models.ForeignKey("Group",
        # mediumint(8) unsigned
        default=3,
        help_text="The user's default group. {{fk|groups|group_id}}"
    )
    permissions = models.TextField(db_column="user_permissions",
        # mediumtext
        help_text="A cached copy of the user's computed permissions."
    )
    # user_perm_from = models.ForeignKey(, db_column="# user_perm_from"
    perm_from = PhpBBForeignKey("User", db_column="user_perm_from",
        # mediumint(8) unsigned - default=0,
        help_text="The id of the user whose permissions are being tested. {{fk|users|user_id}}"
    )
    ip = models.CharField(max_length=40, db_column="user_ip", blank=True,
        # varchar(40)
        help_text="The IP of the user on registration, dotted QUAD style (ie: 127.0.0.1)"
    )
    regdate = models.PositiveIntegerField(db_column="user_regdate",
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
    password = models.CharField(max_length=40, db_column="user_password",
        # varchar(40)
        help_text="The [[Function.phpbb_hash|hashed]] version of the user's password."
    )
    passchg = models.PositiveIntegerField(db_column="user_passchg",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp indicating when the user's password was last changed."
    )
    pass_convert = models.PositiveSmallIntegerField(db_column="user_pass_convert",
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating whether or not the user's password needs to be converted to the phpBB3 hashing. Used when converting from phpBB2."
    )
    email = models.CharField(max_length=100, db_column="user_email",
        # varchar(100)
        help_text="User's email address"
    )
    email_hash = models.BigIntegerField(db_column="user_email_hash",
        # bigint(20)
        default=0,
        help_text="A hash of the user's email address."
    )
    birthday = models.CharField(max_length=10, db_column="user_birthday", blank=True,
        # varchar(10)
        help_text="The user's birthday, in the form of dd-mm-yyyy."
    )
    lastvisit = models.PositiveIntegerField(db_column="user_lastvisit",
        # int(11) unsigned
        default=0,
        help_text="User's last visit time, UNIX timestamp."
    )
    lastmark = models.PositiveIntegerField(db_column="user_lastmark",
        # int(11) unsigned
        default=0,
        help_text="The last time the user clicked 'Mark forums read'"
    )
    lastpost_time = models.PositiveIntegerField(db_column="user_lastpost_time",
        # int(11) unsigned
        default=0,
        help_text="The time of the latest post of the user, UNIX timestamp"
    )
    lastpage = models.CharField(max_length=200, db_column="user_lastpage", blank=True,
        # varchar(200)
        help_text="The last page visited by the user."
    )
    last_confirm_key = models.CharField(max_length=10, db_column="user_last_confirm_key", blank=True,
        # varchar(10)
        help_text="Code used for security reasons by confirmation windows"
    )
    last_search = models.PositiveIntegerField(db_column="user_last_search",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the user performed a search. Used for search flood time limits."
    )
    warnings = models.IntegerField(db_column="user_warnings",
        # tinyint(4)
        default=0,
        help_text="The number of warnings the user has."
    )
    last_warning = models.PositiveIntegerField(db_column="user_last_warning",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the user was warned."
    )
    login_attempts = models.IntegerField(db_column="user_login_attempts",
        # tinyint(4)
        default=0,
        help_text="The number of times a login to this account has failed. This is reset to zero upon successful login."
    )
    inactive_reason = models.IntegerField(db_column="user_inactive_reason",
        # tinyint(2)
        default=0,
        help_text="Reason for being inactive"
    )
    inactive_time = models.PositiveIntegerField(db_column="user_inactive_time",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, when the user's account became inactive."
    )
    posts = models.PositiveIntegerField(db_column="user_posts",
        # mediumint(8) unsigned
        default=0,
        help_text="Amount of posts the user has posted"
    )
    lang = models.CharField(max_length=30, db_column="user_lang",
        # varchar(30)
        help_text="The user's selected board language"
    )
    timezone = models.DecimalField(max_digits=7, decimal_places=2, db_column="user_timezone",
        # decimal(5,2)
        default=0,
        help_text="The user's timezone offset from UTC."
    )
    dst = models.PositiveSmallIntegerField(db_column="user_dst",
        # tinyint(1) unsigned
        default=0,
        help_text="Is the user on Daylight Savings Time"
    )
    dateformat = models.CharField(max_length=30, db_column="user_dateformat",
        # varchar(30)
        default="d M Y H:i",
        help_text="The user's desired date [http://www.php.net/function.date.php format]"
    )
    # user_style = models.IntegerField()
    style = models.ForeignKey("Style", db_column="user_style", blank=True,
        # tinyint(4)
        default=0,
        help_text="Style the user uses to browse the board. {{fk|styles|style_id}}"
    )
    # user_rank = models.IntegerField()
    rank = PhpBBForeignKey("Rank", db_column="user_rank",
        # mediumint(8) unsigned - default=0,
        help_text="User's rank. {{fk|ranks|rank_id}}"
    )
    colour = models.CharField(max_length=6, db_column="user_colour", blank=True,
        # varchar(6)
        help_text="User's colour, hex code."
    )
    new_privmsg = models.IntegerField(db_column="user_new_privmsg",
        # tinyint(4)
        default=0,
        help_text="The number of new private messages that the user has."
    )
    unread_privmsg = models.IntegerField(db_column="user_unread_privmsg",
        # tinyint(4)
        default=0,
        help_text="The number of unread private messages that the user has."
    )
    last_privmsg = models.PositiveIntegerField(db_column="user_last_privmsg",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the user sent a private message. Used for flood checking."
    )
    message_rules = models.PositiveSmallIntegerField(db_column="user_message_rules",
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating whether or not the user has custom rules for private messages."
    )
    full_folder = models.IntegerField(db_column="user_full_folder",
        # int(11)
        default= -3,
        help_text="The action to take when a user's private message folder is full."
    )
    emailtime = models.PositiveIntegerField(db_column="user_emailtime",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the time the user last sent an email. Used for flood checking."
    )
    topic_show_days = models.PositiveIntegerField(db_column="user_topic_show_days",
        # smallint(4) unsigned
        default=0,
        help_text="The maximum age of a topic that should be shown."
    )
    topic_sortby_type = models.CharField(max_length=1, db_column="user_topic_sortby_type",
        # char(1)
        default="t",
        help_text="Topic sort order. a is Author, r is Replies, t is Post Time, s is Subject, v is Views"
    )
    topic_sortby_dir = models.CharField(max_length=1, db_column="user_topic_sortby_dir",
        # char(1)
        default="d",
        help_text="Topic sort direction. a is ascending, d is descending"
    )
    post_show_days = models.PositiveIntegerField(db_column="user_post_show_days",
        # smallint(4) unsigned
        default=0,
        help_text="Preferences for reading "
    )
    post_sortby_type = models.CharField(max_length=1, db_column="user_post_sortby_type",
        # char(1)
        default="t",
        help_text="Post sort order. a is Author, s is subject, t is Post Time"
    )
    post_sortby_dir = models.CharField(max_length=1, db_column="user_post_sortby_dir",
        # char(1)
        default="a",
        help_text="Post sort direction. a is ascending, d is descending"
    )
    notify = models.PositiveSmallIntegerField(db_column="user_notify",
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating whether the user should be notified upon replies to a topic by default or not."
    )
    notify_pm = models.PositiveSmallIntegerField(db_column="user_notify_pm",
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user should be notified upon the arrival of new private messages."
    )
    notify_type = models.IntegerField(db_column="user_notify_type",
        # tinyint(4)
        default=0,
        help_text="How the user should be notified for the above events: email, IM, or both"
    )
    allow_pm = models.PositiveSmallIntegerField(db_column="user_allow_pm",
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating whether the user wants to receive private messages from other users or not."
    )
    allow_viewonline = models.PositiveSmallIntegerField(db_column="user_allow_viewonline",
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user should be visible or hidden."
    )
    allow_viewemail = models.PositiveSmallIntegerField(db_column="user_allow_viewemail",
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user can be contacted via email through the board's email form."
    )
    allow_massemail = models.PositiveSmallIntegerField(db_column="user_allow_massemail",
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating if the user wishes to receive mass emails."
    )
    options = models.PositiveIntegerField(db_column="user_options",
        # int(11) unsigned
        default=230271,
        help_text="A bitfield containing the options for: showing images in posts, showing flash in posts, showing similies in posts, showing signatures, showing avatars, enable word censoring, attach signature by default, enable bbcodes by default, enable smilies by default, show a popup for new private messages, enable bbcode in signature, enable smilies in signature, automatically parse links in signature"
    )
    avatar = models.CharField(max_length=255, db_column="user_avatar", blank=True,
        # varchar(255)
        help_text="Avatar's file name. URI for remote avatar, file directory and name for gallery avatar, combination of user id and time stamp for uploaded avatar."
    )
    avatar_type = models.IntegerField(db_column="user_avatar_type",
        # tinyint(2)
        default=0,
        help_text="The type of avatar the user has: remote, gallery, or uploaded"
    )
    avatar_width = models.PositiveIntegerField(db_column="user_avatar_width",
        # smallint(4) unsigned
        default=0,
        help_text="Width of the avatar"
    )
    avatar_height = models.PositiveIntegerField(db_column="user_avatar_height",
        # smallint(4) unsigned
        default=0,
        help_text="Height of the avatar"
    )
    sig = models.TextField(db_column="user_sig",
        # mediumtext
        help_text="The user's signature"
    )
    sig_bbcode_uid = models.CharField(max_length=8, db_column="user_sig_bbcode_uid",
        # varchar(5)
        help_text="The bbcode uid used in the user's signature."
    )
    sig_bbcode_bitfield = models.CharField(max_length=255, db_column="user_sig_bbcode_bitfield",
        # varchar(255)
        help_text="The bbcode, smiley, and url settings used when saving the user's signature."
    )
    user_from = models.CharField(max_length=100,
        # varchar(100)
        help_text="User's location field value"
    )
    icq = models.CharField(max_length=15, db_column="user_icq", blank=True,
        # varchar(15)
        help_text="User's ICQ field value"
    )
    aim = models.CharField(max_length=255, db_column="user_aim", blank=True,
        # varchar(255)
        help_text="User's AIM field value"
    )
    yim = models.CharField(max_length=255, db_column="user_yim", blank=True,
        # varchar(255)
        help_text="User's YIM field value"
    )
    msnm = models.CharField(max_length=255, db_column="user_msnm", blank=True,
        # varchar(255)
        help_text="User's MSN field value"
    )
    jabber = models.CharField(max_length=255, db_column="user_jabber", blank=True,
        # varchar(255)
        help_text="User's Jabber field value"
    )
    website = models.CharField(max_length=200, db_column="user_website", blank=True,
        # varchar(200)
        help_text="User's website field value"
    )
    occ = models.TextField(db_column="user_occ", blank=True,
        # text
        help_text="User's occupation field value"
    )
    interests = models.TextField(db_column="user_interests", blank=True,
        # text
        help_text="User's interests field value"
    )
    actkey = models.CharField(max_length=32, db_column="user_actkey", blank=True,
        # varchar(32)
        help_text="The key required to activate the user's account."
    )
    newpasswd = models.CharField(max_length=40, db_column="user_newpasswd", blank=True,
        # varchar(32)
        help_text="A randomly generated password for when the user has forgotten their password."
    )
    form_salt = models.CharField(max_length=32, db_column="user_form_salt")
    new = models.IntegerField(db_column="user_new",)
    reminded = models.IntegerField(db_column="user_reminded",)
    reminded_time = models.IntegerField(db_column="user_reminded_time",)

    def has_content(self):
        """
        Manually check if user has a post or topic
        """
        if Topic.objects.all().filter(poster=self).count():
            return True
        if Post.objects.all().filter(poster=self).count():
            return True
        if Attachment.objects.all().filter(poster=self).count():
            return True
        return False

    def registration_datetime(self):
        return timestamp2datetime(self.regdate, self.timezone)

    def lastvisit_datetime(self):
        return timestamp2datetime(self.lastvisit, self.timezone)

    def get_cleaned_signature(self):
        """
        returns a cleaned version of the self.sig bbcode.
        """
        if self.sig_bbcode_bitfield:
            bbcode_uid = self.sig_bbcode_uid
        else:
            bbcode_uid = None

        text = smart_unicode(self.sig)
        bbcode = clean_bbcode(text, bbcode_uid)
        return bbcode

    def __unicode__(self):
        return smart_unicode(self.username)

    class Meta:
        db_table = u"%susers" % settings.PHPBB_TABLE_PREFIX
        ordering = ['-posts']


class Forum(models.Model):
    """
    Forum (Name, description, rules...)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="forum_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    parent = models.ForeignKey("self", related_name='+', blank=True,
        # mediumint(8) unsigned
        default=0,
        help_text="the forum_id of the parent forum (or category)"
    )
    left = models.ForeignKey("self", related_name='+', blank=True,
        # mediumint(8) unsigned
        default=0,
        help_text="forum_id of the forum left to the current forum in the binary tree (used e. g. to retrieve the list of all parents very fast to create the forum navigation)"
    )
    right = models.ForeignKey("self", related_name='+', blank=True,
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
    forum_style = models.ForeignKey("Style", db_column="forum_style",
        # tinyint(4)
        default=0,
        blank=True,
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
    def last_post_datetime(self):
        # FIXME: UTC or local time from user???
        return timestamp2datetime(self.forum_last_post_time, timezone=None)

    def __unicode__(self):
        return smart_unicode(self.forum_name)

    class Meta:
        db_table = u"%sforums" % settings.PHPBB_TABLE_PREFIX


class Post(models.Model):
    """
    Topic posts
    """
    id = models.AutoField(primary_key=True, db_column="post_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    topic = models.ForeignKey("Topic", blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    forum = models.ForeignKey("Forum", blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    poster = PhpBBForeignKey("User",
        # mediumint(8) unsigned - default=0,
    )
    icon = models.ForeignKey("Icon", blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    poster_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    time = models.PositiveIntegerField(db_column="post_time",
        # int(11) unsigned
        default=0,
    )
    approved = models.PositiveSmallIntegerField(db_column="post_approved",
        # tinyint(1) unsigned
        default=1,
    )
    reported = models.PositiveSmallIntegerField(db_column="post_reported",
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
    username = models.CharField(max_length=255, db_column="post_username",
        # varchar(255)
    )
    subject = models.CharField(max_length=255, db_column="post_subject",
        # varchar(100)
    )
    text = models.TextField(db_column="post_text",
        # mediumtext
    )
    checksum = models.CharField(max_length=32, db_column="post_checksum",
        # varchar(32)
    )
    attachment = models.PositiveSmallIntegerField(db_column="post_attachment",
        # tinyint(1) unsigned
        default=0,
        help_text="1=This post has at least one attachment 0=no attachments in this post"
    )
    bbcode_bitfield = models.CharField(max_length=255,
        # varchar(255)
        help_text="see [[Parsing text]]"
    )
    bbcode_uid = models.CharField(max_length=8,
        # varchar(5)
        help_text="see [[Parsing text]]"
    )
    postcount = models.PositiveSmallIntegerField(db_column="post_postcount",
        # tinyint(1) unsigned
        default=1,
    )
    edit_time = models.PositiveIntegerField(db_column="post_edit_time",
        # int(11) unsigned
        default=0,
    )
    edit_reason = models.CharField(max_length=255, db_column="post_edit_reason",
        # varchar(255)
    )
    edit_user = models.PositiveIntegerField(db_column="post_edit_user",
        # mediumint(8) unsigned
        default=0,
    )
    edit_count = models.PositiveIntegerField(db_column="post_edit_count",
        # smallint(4) unsigned
        default=0,
    )
    edit_locked = models.PositiveSmallIntegerField(db_column="post_edit_locked",
        # tinyint(1) unsigned
        default=0,
    )
    def create_datetime(self):
        # FIXME: UTC or local time from user???
        return timestamp2datetime(self.time, timezone=None)

    def update_datetime(self):
        # FIXME: UTC or local time from user???
        return timestamp2datetime(self.edit_time, timezone=None)

    def teaser(self):
        text = smart_unicode(self.text)
        return u" ".join(text.splitlines())[:50] + u"..."

    def has_attachment(self):
        return bool(self.attachment)
    has_attachment.boolean = True

    def get_cleaned_bbcode(self):
        """
        returns a cleaned version of the self.text bbcode.
        """
        if self.bbcode_bitfield:
            bbcode_uid = self.bbcode_uid
        else:
            bbcode_uid = None

        text = smart_unicode(self.text)
        bbcode = clean_bbcode(text, bbcode_uid)
        return bbcode

    def __unicode__(self):
        return u"Post %i: %s" % (self.id, self.teaser())

    class Meta:
        db_table = u"%sposts" % settings.PHPBB_TABLE_PREFIX



# for Topic.status:
TOPIC_UNLOCKED = 0
TOPIC_LOCKED = 1
TOPIC_MOVED = 2

class Topic(models.Model):
    """
    Topic in forums
    """
    id = models.AutoField(primary_key=True, db_column="topic_id",
        # mediumint(8) unsigned
        help_text="Primary key"
    )
    # forum_id = models.IntegerField()
    forum = PhpBBForeignKey("Forum",
        # mediumint(8) unsigned - default=0,
        help_text="{{fk|forums|forum_id}}"
    )
    # icon_id = models.IntegerField()
    icon = PhpBBForeignKey("Icon",
        # mediumint(8) unsigned - default=0,
        help_text="{{fk|icons|icon_id}}"
    )
    attachment = models.PositiveSmallIntegerField(db_column="topic_attachment",
        # tinyint(1) unsigned
        default=0,
        help_text="1=at least one post in this topic has an attachment&lt;br/>0=no attachments in this topic"
    )
    approved = models.PositiveSmallIntegerField(db_column="topic_approved",
        # tinyint(1) unsigned
        default=1,
        help_text="Flag indicating whether the topic is awaiting approval or not."
    )
    reported = models.PositiveSmallIntegerField(db_column="topic_reported",
        # tinyint(1) unsigned
        default=0,
        help_text="Flag indicating that a post within the topic has been reported."
    )
    title = models.CharField(max_length=255, db_column="topic_title",
        # varchar(100)
        help_text="The title of the topic."
    )
    # topic_poster = models.IntegerField()
    poster = PhpBBForeignKey("User", db_column="topic_poster",
        # mediumint(8) unsigned - default=0,
        help_text="{{fk|users|user_id}}"
    )
    time = models.PositiveIntegerField(db_column="topic_time",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the topic's creation date."
    )
    time_limit = models.PositiveIntegerField(db_column="topic_time_limit",
        # int(11) unsigned
        default=0,
        help_text="The number of seconds that a topic will remain as a sticky."
    )
    views = models.PositiveIntegerField(db_column="topic_views",
        # mediumint(8) unsigned
        default=0,
        help_text="The number of time the topic has been viewed."
    )
    replies = models.PositiveIntegerField(db_column="topic_replies",
        # mediumint(8) unsigned
        default=0,
        help_text="The number of approved replies to this topic."
    )
    replies_real = models.PositiveIntegerField(db_column="topic_replies_real",
        # mediumint(8) unsigned
        default=0,
        help_text="Total number of replies to this topic (including posts waiting for approval)."
    )
    status = models.IntegerField(db_column="topic_status",
        # tinyint(3)
        default=0,
        help_text="0 == UNLOCKED, 1 == LOCKED or 2 == MOVED"
    )
    type = models.IntegerField(db_column="topic_type",
        # tinyint(3)
        default=0,
        help_text="[[Constants|POST_NORMAL]](0), POST_STICKY(1), POST_ANNOUNCE(2) or POST_GLOBAL(3)"
    )
    # topic_first_post_id = models.IntegerField()
    first_post = PhpBBForeignKey("Post", related_name='+', db_column="topic_first_post_id",
        # mediumint(8) unsigned - default=0,
        help_text="{{fk|posts|post_id}}"
    )
    first_poster_name = models.CharField(max_length=255, db_column="topic_first_poster_name",
        # varchar(255)
        help_text="The topic creator's username."
    )
    first_poster_colour = models.CharField(max_length=6, db_column="topic_first_poster_colour",
        # varchar(6)
        help_text="The colour of the topic creator's default user group."
    )
    # topic_last_post_id = models.IntegerField()
    last_post = PhpBBForeignKey("Post", related_name='+', db_column="topic_last_post_id",
        # mediumint(8) unsigned - default=0,
        help_text="{{fk|posts|post_id}}"
    )
    # topic_last_poster_id = models.IntegerField()
    last_poster = PhpBBForeignKey("User", related_name='+', db_column="topic_last_poster_id",
        # mediumint(8) unsigned - default=0,
        help_text="{{fk|users|user_id}}"
    )
    last_poster_name = models.CharField(max_length=255, db_column="topic_last_poster_name",
        # varchar(255)
        help_text="The username of the topic's last poster."
    )
    last_poster_colour = models.CharField(max_length=6, db_column="topic_last_poster_colour",
        # varchar(6)
        help_text="The colour of the last poster's default user group."
    )
    last_post_subject = models.CharField(max_length=255, db_column="topic_last_post_subject",
        # varchar(100)
        help_text="The subject of the topic's last post"
    )
    last_post_time = models.PositiveIntegerField(db_column="topic_last_post_time",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time a post was made in the topic."
    )
    last_view_time = models.PositiveIntegerField(db_column="topic_last_view_time",
        # int(11) unsigned
        default=0,
        help_text="Unix timestamp, the last time the topic was viewed. Used in topic pruning."
    )
    moved_id = models.PositiveIntegerField(db_column="topic_moved_id",
        # mediumint(8) unsigned
        default=0,
        help_text="If topic_status is ITEM_MOVED (a shadow topic), this field contains the topic id of the real topic."
    )
    bumped = models.PositiveSmallIntegerField(db_column="topic_bumped",
        # tinyint(1) unsigned
        default=0,
        help_text="Has this topic been bumped? 1 (yes), 0(no)"
    )
    # topic_bumper = models.IntegerField()
    bumper = PhpBBForeignKey("User", related_name='+', db_column="topic_bumper",
        # mediumint(8) unsigned - default=0,
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

    def clean_title(self):
        title = deentity.replace_all(self.title)
        title = smart_unicode(title)
        return title

    def moved(self):
        return self.status == TOPIC_MOVED
    moved.boolean = True
    def locked(self):
        return self.status == TOPIC_LOCKED
    locked.boolean = True

    def create_datetime(self):
        return timestamp2datetime(self.time)
    def last_post_datetime(self):
        return timestamp2datetime(self.last_post_time)
    def last_view_datetime(self):
        return timestamp2datetime(self.last_view_time)

    def __unicode__(self):
        return smart_unicode(self.title)

    class Meta:
        db_table = u"%stopics" % settings.PHPBB_TABLE_PREFIX
        ordering = ['-time']


class Group(models.Model):
    """
    Usergroups
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="group_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    type = models.IntegerField(db_column="group_type",
        # tinyint(4)
        default=1,
    )
    founder_manage = models.PositiveSmallIntegerField(db_column="group_founder_manage",
        # tinyint(1) unsigned
        default=0,
    )
    skip_auth = models.IntegerField(db_column="group_skip_auth")
    name = models.CharField(max_length=255, db_column="group_name",
        # varchar(255)
    )
    desc = models.TextField(db_column="group_desc",
        # text
    )
    desc_bitfield = models.CharField(max_length=255, db_column="group_desc_bitfield",
        # varchar(255)
    )
    desc_options = models.PositiveIntegerField(db_column="group_desc_options",
        # int(11) unsigned
        default=7,
    )
    desc_uid = models.CharField(max_length=8, db_column="group_desc_uid",
        # varchar(5)
    )
    display = models.PositiveSmallIntegerField(db_column="group_display",
        # tinyint(1) unsigned
        default=0,
    )
    avatar = models.CharField(max_length=255, db_column="group_avatar",
        # varchar(255)
    )
    avatar_type = models.IntegerField(db_column="group_avatar_type",
        # tinyint(4)
        default=0,
    )
    avatar_width = models.IntegerField(db_column="group_avatar_width",
        # tinyint(4)
        default=0,
    )
    avatar_height = models.IntegerField(db_column="group_avatar_height",
        # tinyint(4)
        default=0,
    )
    rank = models.PositiveIntegerField(db_column="group_rank",
        # mediumint(8) unsigned
        default=0,
    )
    colour = models.CharField(max_length=6, db_column="group_colour",
        # varchar(6)
    )
    sig_chars = models.PositiveIntegerField(db_column="group_sig_chars",
        # mediumint(8) unsigned
        default=0,
    )
    receive_pm = models.PositiveSmallIntegerField(db_column="group_receive_pm",
        # tinyint(1) unsigned
        default=0,
    )
    message_limit = models.PositiveIntegerField(db_column="group_message_limit",
        # mediumint(8) unsigned
        default=0,
    )
    max_recipients = models.IntegerField(db_column="group_max_recipients")
    legend = models.PositiveSmallIntegerField(db_column="group_legend",
        # tinyint(1) unsigned
        default=1,
    )
    def __unicode__(self):
        return smart_unicode(self.name)

    class Meta:
        db_table = u"%sgroups" % settings.PHPBB_TABLE_PREFIX


class Attachment(models.Model):
    """
    Information on attachments (Post, physical filename, original filename, MIME type...)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="attach_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    # post_msg_id = models.IntegerField()
    post_msg = models.ForeignKey("Post", blank=True, related_name="+",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|posts|post_id}}"
    )
    # topic_id = models.IntegerField()
    topic = models.ForeignKey("Topic", blank=True, related_name="+",
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
    poster = PhpBBForeignKey("User",
        # mediumint(8) unsigned - default=0,
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
    def file_datetime(self):
        return datetime.datetime.fromtimestamp(self.filetime)

    def __unicode__(self):
        return u"Attachment %i for %s" % (self.id, self.post_msg)

    class Meta:
        db_table = u"%sattachments" % settings.PHPBB_TABLE_PREFIX


#------------------------------------------------------------------------------
# more uninportand models:


class Config(models.Model):
    """
    Configuration information ($config table)
    """
    id = models.CharField(max_length=255, primary_key=True, db_column="config_name",
        # varchar(255)
        help_text="config name, primary key"
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
            return u"%s: %s" % (self.id, self.config_value)
    class Meta:
        db_table = u"%sconfig" % settings.PHPBB_TABLE_PREFIX

#______________________________________________________________________________
# untouched models:

class AclOption(models.Model):
    """
    List of possible permissions
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="auth_option_id",
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
        db_table = u"%sacl_options" % settings.PHPBB_TABLE_PREFIX

class AclRole(models.Model):
    """
    Permission roles (Standard Moderator, Simple Moderator etc.)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="role_id",
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
        db_table = u"%sacl_roles" % settings.PHPBB_TABLE_PREFIX

class AclRoleData(models.Model):
    """
    Permissions each role contains
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="role_id",
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
        db_table = u"%sacl_roles_data" % settings.PHPBB_TABLE_PREFIX


class Banlist(models.Model):
    """
    Banned users/IPs/emails...
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="ban_id",
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
        db_table = u"%sbanlist" % settings.PHPBB_TABLE_PREFIX


class Bbcode(models.Model):
    """
    Custom BBCodes
    """
    id = models.IntegerField(primary_key=True, db_column="bbcode_id",
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
        db_table = u"%sbbcodes" % settings.PHPBB_TABLE_PREFIX

class Bookmark(models.Model):
    """
    Bookmarked topics
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="topic_id",
        # mediumint(8) unsigned
        default=0,
    )
    id = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        default=0,
    )
    class Meta:
        db_table = u"%sbookmarks" % settings.PHPBB_TABLE_PREFIX

class Bot(models.Model):
    """
    Spiders/Robots
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="bot_id",
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
    user = models.ForeignKey("User", related_name='+', blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    bot_agent = models.CharField(max_length=255,
        # varchar(255)
    )
    bot_ip = models.CharField(max_length=255,
        # varchar(255)
    )
    def __unicode__(self):
        return smart_unicode(self.bot_name)

    class Meta:
        db_table = u"%sbots" % settings.PHPBB_TABLE_PREFIX


if settings.PHPBB_CAPTCHA_QUESTIONS_MODEL_EXIST:
    class CaptchaQuestions(models.Model):
        """
        FIXME: This table doesn't exist in every case???
        """
        id = models.IntegerField(primary_key=True, db_column="question_id")
        strict = models.IntegerField()
        lang_id = models.IntegerField()
        lang_iso = models.CharField(max_length=30)
        question_text = models.TextField()
        class Meta:
            db_table = u"%scaptcha_questions" % settings.PHPBB_TABLE_PREFIX


class Confirm(models.Model):
    """
    Contains session information for confirm pages ("are you sure you want to delete foo")
    
    Note: Not really supported mode, because no field is really unique!!!
    """
    id = models.CharField(max_length=96, primary_key=True, db_column="session_id",
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
        db_table = u"%sconfirm" % settings.PHPBB_TABLE_PREFIX

class Disallow(models.Model):
    """
    Disallowed usernames
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="disallow_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    disallow_username = models.CharField(max_length=255,
        # varchar(255)
    )
    def __unicode__(self):
        return smart_unicode(self.disallow_username)
    class Meta:
        db_table = u"%sdisallow" % settings.PHPBB_TABLE_PREFIX

class Draft(models.Model):
    """
    Draft of future posts/private messages
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="draft_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user = models.ForeignKey("User", related_name='+', blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    topic = models.ForeignKey("Topic", blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    forum = models.ForeignKey("Forum", blank=True,
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
        db_table = u"%sdrafts" % settings.PHPBB_TABLE_PREFIX

class ExtensionGroup(models.Model):
    """
    Extension Group (associate extensions with a file type - Images, text...)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="group_id",
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
        db_table = u"%sextension_groups" % settings.PHPBB_TABLE_PREFIX

class Extension(models.Model):
    """
    Extension (.xxx) allowed for attachments
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="extension_id",
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
        db_table = u"%sextensions" % settings.PHPBB_TABLE_PREFIX

class Icon(models.Model):
    """
    Post icons
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="icons_id",
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
    def __unicode__(self):
        return smart_unicode(self.icons_url)
    class Meta:
        db_table = u"%sicons" % settings.PHPBB_TABLE_PREFIX

class Lang(models.Model):
    """
    Installed languages
    """
    id = models.IntegerField(primary_key=True, db_column="lang_id",
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
        db_table = u"%slang" % settings.PHPBB_TABLE_PREFIX

class Log(models.Model):
    """
    Administration/Moderation/Error logs
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="log_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    log_type = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    user = models.ForeignKey("User", related_name='+', blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    forum = models.ForeignKey("Forum", blank=True,
        # mediumint(8) unsigned
        default=0,
    )
    topic = models.ForeignKey("Topic", blank=True,
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
        db_table = u"%slog" % settings.PHPBB_TABLE_PREFIX


class Module(models.Model):
    """
    Configuration of acp, mcp and ucp modules
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="module_id",
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
        db_table = u"%smodules" % settings.PHPBB_TABLE_PREFIX


class Privmsg(models.Model):
    """
    Private messages text
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="msg_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    root_level = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
        help_text="the initial message in this message chain (i.e. if you write messages A -> B (reply to A) -> C (reply to B), then B and C will have root_level=msg_id of A"
    )
    # author_id = models.IntegerField()
    author = models.ForeignKey("User", blank=True,
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    # icon_id = models.IntegerField()
    icon = models.ForeignKey("Icon", blank=True,
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
        db_table = u"%sprivmsgs" % settings.PHPBB_TABLE_PREFIX

class PrivmsgFolder(models.Model):
    """
    Custom privates messages folders (for each user)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="folder_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user = models.ForeignKey("User", related_name='+', blank=True,
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
        db_table = u"%sprivmsgs_folder" % settings.PHPBB_TABLE_PREFIX

class PrivmsgRules(models.Model):
    """
    Messages rules, e.g. "if the username of the sender is ..., move the message to this folder".
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="rule_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user = models.ForeignKey("User", related_name='+', blank=True,
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
    rule_user = models.ForeignKey("User", related_name='+',
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
        db_table = u"%sprivmsgs_rules" % settings.PHPBB_TABLE_PREFIX

class ProfileField(models.Model):
    """
    Custom profile fields (name, min/max number of characters, allowed characters...)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="field_id",
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
        db_table = u"%sprofile_fields" % settings.PHPBB_TABLE_PREFIX

class ProfileFieldData(models.Model):
    """
    Data that users enter in custom profile fields
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    class Meta:
        db_table = u"%sprofile_fields_data" % settings.PHPBB_TABLE_PREFIX

class ProfileFieldLang(models.Model):
    """
    tbd (empty on my forum with some custom profile fields)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="field_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    id = models.PositiveIntegerField(primary_key=True, db_column="lang_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    id = models.PositiveIntegerField(primary_key=True, db_column="option_id",
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
        db_table = u"%sprofile_fields_lang" % settings.PHPBB_TABLE_PREFIX

class ProfileLang(models.Model):
    """
    Localized name and description of custom profile fields (presented to users)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="field_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    id = models.PositiveIntegerField(primary_key=True, db_column="lang_id",
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
        db_table = u"%sprofile_lang" % settings.PHPBB_TABLE_PREFIX

class Rank(models.Model):
    """
    Rank (Name, image, minimal # of posts)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="rank_id",
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
    def __unicode__(self):
        return smart_unicode(self.rank_title)
    class Meta:
        db_table = u"%sranks" % settings.PHPBB_TABLE_PREFIX

class Report(models.Model):
    """
    Reported posts
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="report_id",
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
    user = models.ForeignKey("User", related_name='+', blank=True,
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
        db_table = u"%sreports" % settings.PHPBB_TABLE_PREFIX

class ReportReasons(models.Model):
    """
    Reasons for reported posts and disapprovals
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="reason_id",
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
        db_table = u"%sreports_reasons" % settings.PHPBB_TABLE_PREFIX

class SearchResult(models.Model):
    """
    Last searches
    """
    id = models.CharField(max_length=32, primary_key=True, db_column="search_key",
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
        db_table = u"%ssearch_results" % settings.PHPBB_TABLE_PREFIX

class SearchWordlist(models.Model):
    """
    Indexed words (for search)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="word_id",
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
        db_table = u"%ssearch_wordlist" % settings.PHPBB_TABLE_PREFIX


class Session(models.Model):
    """
    Session (to identify users browsing the forum)
    """
    id = models.CharField(max_length=96, primary_key=True, db_column="session_id",
        # varchar(32)
        help_text="primary key"
    )
    session_user = models.ForeignKey("User", related_name='+', blank=True,
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
        db_table = u"%ssessions" % settings.PHPBB_TABLE_PREFIX

class Sitelist(models.Model):
    """
    Secure Downloads of attachments - list of IPs and hostnames
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="site_id",
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
        db_table = u"%ssitelist" % settings.PHPBB_TABLE_PREFIX

class Smilie(models.Model):
    """
    Smilie (text => image)
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="smiley_id",
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
        db_table = u"%ssmilies" % settings.PHPBB_TABLE_PREFIX

class Style(models.Model):
    """
    Style = template + theme + imageset
    """
    id = models.IntegerField(primary_key=True, db_column="style_id",
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
    def __unicode__(self):
        return smart_unicode(self.style_name)
    class Meta:
        db_table = u"%sstyles" % settings.PHPBB_TABLE_PREFIX

class StyleImageset(models.Model):
    """
    [[Templating_Tutorial#Customizing_the_Imageset|Imagesets]]
    """
    id = models.IntegerField(primary_key=True, db_column="imageset_id",
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
        db_table = u"%sstyles_imageset" % settings.PHPBB_TABLE_PREFIX

class StyleImagesetData(models.Model):
    """
    tbd
    """
    id = models.IntegerField(primary_key=True, db_column="image_id")
    image_name = models.CharField(max_length=200)
    image_filename = models.CharField(max_length=200)
    image_lang = models.CharField(max_length=30)
    image_height = models.IntegerField()
    image_width = models.IntegerField()
    imageset_id = models.IntegerField()
    class Meta:
        db_table = u"%sstyles_imageset_data" % settings.PHPBB_TABLE_PREFIX

class StyleTemplate(models.Model):
    """
    tbd
    """
    id = models.IntegerField(primary_key=True, db_column="template_id",
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
        db_table = u"%sstyles_template" % settings.PHPBB_TABLE_PREFIX

class StyleTemplateData(models.Model):
    """
    FIXME: template_id is a ForeignKey to StyleTemplate?
    """
    template = models.IntegerField(primary_key=True, db_column="template_id",
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
        db_table = u"%sstyles_template_data" % settings.PHPBB_TABLE_PREFIX

class StyleTheme(models.Model):
    """
    theme = css file
    """
    id = models.IntegerField(primary_key=True, db_column="theme_id",
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
        db_table = u"%sstyles_theme" % settings.PHPBB_TABLE_PREFIX

class TopicTrack(models.Model):
    """
    Unread post information is stored here
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    topic = models.ForeignKey("Topic",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    forum = models.ForeignKey("Forum",
        # mediumint(8) unsigned
    )
    mark_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    class Meta:
        db_table = u"%stopics_track" % settings.PHPBB_TABLE_PREFIX


class Warning(models.Model):
    """
    Warning given to users
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="warning_id",
        # mediumint(8) unsigned
        help_text="primary key"
    )
    user = models.ForeignKey("User", related_name='+', blank=True,
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
        db_table = u"%swarnings" % settings.PHPBB_TABLE_PREFIX


class Word(models.Model):
    """
    censored words
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="word_id",
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
        db_table = u"%swords" % settings.PHPBB_TABLE_PREFIX

class Zebra(models.Model):
    """
    Friends and foes
    """
    id = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        default=0,
    )
    id = models.PositiveIntegerField(primary_key=True, db_column="zebra_id",
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
        db_table = u"%szebra" % settings.PHPBB_TABLE_PREFIX


