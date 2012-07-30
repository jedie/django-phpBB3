# coding: utf-8

"""
    unsupported models
    ~~~~~~~~~~~~~~~~~~
    
    The models would need Django to support composite keys.
    
    more info:
        https://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
        
    You can access the tables via raw sql:
        https://docs.djangoproject.com/en/1.4/topics/db/sql/#executing-custom-sql-directly
    
    Implemented functions to get information are:
        * get_topic_watch()

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import collections

from django.db import models, connection
from django.conf import settings


TOPIC_WATCH_DB_TABLE = u"%stopics_watch" % settings.PHPBB_TABLE_PREFIX
class TopicWatch(models.Model):
    """
    "notify me upon replies"
    """
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user = models.ForeignKey("User", related_name='+',
        # mediumint(8) unsigned
        default=0,
    )
    notify_status = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = TOPIC_WATCH_DB_TABLE


def get_topic_watch(topic_id=None):
    """
    returns a dict with the topic watch information
    dict scheme is:
    {
        "topic_id 1": ["user id 1", "user id 2" ... "user id n"],
        "topic_id 2": ["user id 1", "user id 2" ... "user id n"],
        ...
        "topic_id n": ["user id 1", "user id 2" ... "user id n"],
    }
    """
    cursor = connection.cursor()
    if topic_id is None:
        cursor.execute("SELECT topic_id, user_id FROM %s" % TOPIC_WATCH_DB_TABLE)
    else:
        cursor.execute(
            "SELECT topic_id, user_id FROM %s WHERE topic_id = %%s" % TOPIC_WATCH_DB_TABLE,
            [topic_id],
        )

    result = collections.defaultdict(list)
    for topic_id, user_id in cursor.fetchall():
        result[topic_id].append(user_id)

    return result


#------------------------------------------------------------------------------


class AclGroup(models.Model):
    """
    Permission roles and/or individual permissions assigned to groups
    """
    # group_id = models.IntegerField()
    group = models.ForeignKey("Group",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|groups|group_id}}"
    )
    # forum_id = models.IntegerField()
    forum = models.ForeignKey("Forum",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|forums|forum_id}}"
    )
    # auth_option_id = models.IntegerField()
    auth_option = models.ForeignKey("AclOption",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|acl_options|auth_option_id}}"
    )
    # auth_role_id = models.IntegerField()
    auth_role = models.ForeignKey("AclRole",
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|acl_roles|role_id}}"
    )
    auth_setting = models.IntegerField(
        # tinyint(2)
        default=0,
        help_text="ACL_YES, ACL_NO or ACL_NEVER"
    )
    class Meta:
        db_table = u"%sacl_groups" % settings.PHPBB_TABLE_PREFIX


class ForumWatch(models.Model):
    """
    Subscribed forums
    """
    forum = models.ForeignKey("Forum", primary_key=True, related_name='+',
        # mediumint(8) unsigned
        default=0,
    )
    user = models.ForeignKey("User", primary_key=True, related_name='+',
        # mediumint(8) unsigned
        default=0,
    )
    notify_status = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    def __unicode__(self):
        return u"user '%s' watch forum '%s'" % (self.user, self.forum)
    class Meta:
        db_table = u"%sforums_watch" % settings.PHPBB_TABLE_PREFIX


class ModeratorCache(models.Model):
    """
    Who is a moderator in which forum (for display on forum index)
    """
    forum_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user = models.ForeignKey("User", related_name='+',
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
        db_table = u"%smoderator_cache" % settings.PHPBB_TABLE_PREFIX


class SessionKey(models.Model):
    """
    Autologin feature
    """
    id = models.CharField(max_length=96, primary_key=True, db_column="key_id",
        # varchar(32)
        help_text="primary key"
    )
    user = models.PositiveIntegerField(primary_key=True, db_column="user_id",
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
        db_table = u"%ssessions_keys" % settings.PHPBB_TABLE_PREFIX


class PollVote(models.Model):
    """
    User which have voted on a poll
    """
    topic_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    poll_option_id = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    vote_user = models.ForeignKey("User", related_name='+',
        # mediumint(8) unsigned
        default=0,
    )
    vote_user_ip = models.CharField(max_length=40,
        # varchar(40)
    )
    class Meta:
        db_table = u"%spoll_votes" % settings.PHPBB_TABLE_PREFIX


class PrivmsgTo(models.Model):
    """
    Information (sender, new, replied...) on private messages.
    """
    msg_id = models.PositiveIntegerField(
        # mediumint(8) unsigned
        default=0,
    )
    user = models.ForeignKey("User", related_name='+',
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
        db_table = u"%sprivmsgs_to" % settings.PHPBB_TABLE_PREFIX


class UserGroup(models.Model):
    """
    User groups
    """
    # group_id = models.IntegerField()
    group = models.ForeignKey("Group", blank=True,
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|groups|group_id}}"
    )
    # user_id = models.IntegerField()
    user = models.ForeignKey("User", blank=True,
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
        db_table = u"%suser_group" % settings.PHPBB_TABLE_PREFIX


class ForumAccess(models.Model):
    """
    Stores who is logged in to password protected forums
    """
    forum = models.PositiveIntegerField(primary_key=True, db_column="forum_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    user = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    session = models.CharField(max_length=96, primary_key=True, db_column="session_id",
        # char(32) binary
        help_text="primary key"
    )
    class Meta:
        db_table = u"%sforums_access" % settings.PHPBB_TABLE_PREFIX


class AclUser(models.Model):
    """
    Permission roles and/or individual permissions assigned to users
    """
    # user_id = models.IntegerField()
    user = models.ForeignKey("User", blank=True,
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|users|user_id}}"
    )
    # forum_id = models.IntegerField()
    forum = models.ForeignKey("Forum", blank=True,
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|forums|forum_id}}"
    )
    # auth_option_id = models.IntegerField()
    auth_option = models.ForeignKey("AclOption", blank=True,
        # mediumint(8) unsigned
        default=0,
        help_text="{{fk|acl_options|auth_option_id}}"
    )
    # auth_role_id = models.IntegerField()
    auth_role = models.ForeignKey("AclRole", blank=True,
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
        db_table = u"%sacl_users" % settings.PHPBB_TABLE_PREFIX


class CaptchaAnswers(models.Model):
    """
    is like a many-to-one model for CaptchaQuestions, but has no primary key.
    """
    question_id = models.IntegerField()
    answer_text = models.CharField(max_length=255)
    class Meta:
        db_table = u"%scaptcha_answers" % settings.PHPBB_TABLE_PREFIX


class ForumTrack(models.Model):
    """
    Unread post information is stored here
    """
    user = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    forum = models.PositiveIntegerField(primary_key=True, db_column="forum_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    mark_time = models.PositiveIntegerField(
        # int(11) unsigned
        default=0,
    )
    class Meta:
        db_table = u"%sforums_track" % settings.PHPBB_TABLE_PREFIX


class LoginAttempt(models.Model):
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
        db_table = u"%slogin_attempts" % settings.PHPBB_TABLE_PREFIX


class PollOption(models.Model):
    """
    Options text of all votes ("Yes", "No", "Maybe"...)
    """
    poll_option_id = models.IntegerField(
        # tinyint(4)
        default=0,
    )
    topic = models.ForeignKey("Topic", blank=True,
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
        db_table = u"%spoll_options" % settings.PHPBB_TABLE_PREFIX


class QaConfirm(models.Model):
    session_id = models.CharField(max_length=96)
    confirm_id = models.CharField(max_length=96)
    lang_iso = models.CharField(max_length=30)
    question_id = models.IntegerField()
    attempts = models.IntegerField()
    confirm_type = models.IntegerField()
    class Meta:
        db_table = u"%sqa_confirm" % settings.PHPBB_TABLE_PREFIX


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
        db_table = u"%ssearch_wordmatch" % settings.PHPBB_TABLE_PREFIX


class TopicPosted(models.Model):
    """
    Who posted to which topic (used for the small dots in viewforum)
    """
    # FIXME: ForeignKey to User?
    id = models.PositiveIntegerField(primary_key=True, db_column="user_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    # FIXME: ForeignKey to Topic?
    id = models.PositiveIntegerField(primary_key=True, db_column="topic_id",
        # mediumint(8) unsigned
        default=0,
        help_text="primary key"
    )
    topic_posted = models.PositiveSmallIntegerField(
        # tinyint(1) unsigned
        default=0,
    )
    class Meta:
        db_table = u"%stopics_posted" % settings.PHPBB_TABLE_PREFIX
