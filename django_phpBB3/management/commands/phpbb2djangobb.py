# coding: utf-8

"""
    migrate phpBB3 to DjangoBB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~


    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from optparse import make_option
import datetime
import os
import sys
import time
import shutil
import pprint
from django.utils.encoding import smart_unicode

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "phpBB2DjangoBB_project.settings"
    from django.core import management
    print "reset 'djangobb_forum'...",
    management.call_command("reset", "djangobb_forum", interactive=False)
    print "OK"
    management.call_command("phpbb2djangobb",
        cleanup_users=3
    )
    sys.exit()

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models.signals import post_save

from djangobb_forum import settings as forum_settings
from djangobb_forum.models import Category, Forum, Profile, TZ_CHOICES, Post, Topic, \
    Attachment
from djangobb_forum import signals as djangobb_signals

from django_phpBB3.models import Attachment as phpbb_Attachment
from django_phpBB3.models import Forum as phpbb_Forum
from django_phpBB3.models import Group as phpbb_Group
from django_phpBB3.models import Post as phpbb_Post
from django_phpBB3.models import Topic as phpbb_Topic
from django_phpBB3.models import User as phpbb_User
from django_phpBB3.unsupported_models import get_topic_watch
from django_phpBB3.utils import ProcessInfo, human_duration



def disable_auto_fields(model_class):
    """
    Hack: It's needed to disable "auto_now_add" to set a old datetime

    see also: http://stackoverflow.com/questions/7499767/temporarily-disable-auto-now-auto-now-add
    """
    ATTR_NAMES = ("auto_now", "auto_now_add")
    for field in model_class._meta.local_fields:
        for attr_name in ATTR_NAMES:
            if getattr(field, attr_name, False) == True:
                print "Disable '%s' on field %s.%s" % (attr_name, model_class.__name__, field.name)
                setattr(field, attr_name, False)


class Command(BaseCommand):
    help = 'migrate a phpBB3 installation to DjangoBB'
    option_list = BaseCommand.option_list + (
        make_option('--cleanup_users',
            action='store',
            dest='cleanup_users',
            default='2',
            type='choice', choices=['0', '1', '2', '3'],
            help='Which user to migrate: 0:all users, 1:with email, 2:+lastvisit (default), 3:+has post'
        ),

    )

    def handle(self, *args, **options):

        self.check_attachment_path()

        # disable DjangoBB signals for speedup
        post_save.disconnect(djangobb_signals.post_saved, sender=Post, dispatch_uid='djangobb_post_save')
        post_save.disconnect(djangobb_signals.topic_saved, sender=Topic, dispatch_uid='djangobb_topic_save')

        #disable_auto_fields(Forum)
        disable_auto_fields(Topic)
        disable_auto_fields(Post)

        cleanup_users = int(options.get("cleanup_users"))
        moderator_groups = phpbb_Group.objects.filter(
            name__in=["ADMINISTRATORS", "GLOBAL_MODERATORS"]
        )
        user_dict, moderators = self.migrate_users(cleanup_users, moderator_groups)

        forum_dict = self.migrate_forums(moderators)

        topic_dict = self.migrate_topic(user_dict, forum_dict)
        self.migrate_posts(user_dict, topic_dict)

        # needed if signals disabled, see above
        self.update_topic_stats()
        self.update_forum_stats()

        self.stdout.write(u"\nmigration done.\n")

    def _warn(self, msg):
        self.stderr.write(self.style.ERROR(msg))
        self.stderr.flush()

    def check_attachment_path(self):
        path = getattr(settings, "PHPBB_ATTACHMENT_PATH", None)
        if path is None:
            raise CommandError(
                "settings.PHPBB_ATTACHMENT_PATH was not set!"
                " Please add it into your local_settings.py!"
            )
        if not os.path.isdir(path):
            msg = (
                "PHPBB_ATTACHMENT_PATH '%s' doesn't exists!"
                " Please add it into your local_settings.py!"
            ) % path
            raise CommandError(msg)

        for filename in (".htaccess", "index.htm"):
            test_path = os.path.join(path, filename)
            if not os.path.isfile(test_path):
                self._warn("WARNING: file '%s' doesn't exists!\n" % test_path)

        djangobb_path = os.path.join(settings.MEDIA_ROOT, forum_settings.ATTACHMENT_UPLOAD_TO)
        if not os.path.isdir(djangobb_path):
            msg = (
                "DjangoBB attachment path '%s' doesn't exists!"
                " Please check MEDIA_ROOT + ATTACHMENT_UPLOAD_TO in your local_settings.py!"
            ) % djangobb_path
            raise CommandError(msg)


    def migrate_users(self, cleanup_users, moderator_groups):
        self.stdout.write(u"\n *** Migrate phpbb_forum users...\n")

        lang_codes = [i[0] for i in settings.LANGUAGES]
        default_lang = settings.LANGUAGE_CODE.split("-")[0]

        moderators = []
        user_dict = {}
        phpbb_users = phpbb_User.objects.all()
        for phpbb_user in phpbb_users:
            if not phpbb_user.posts:
                # Only users with has no posts can be skip.
                if cleanup_users >= 1:
                    if not phpbb_user.email:
                        self.stdout.write(u"\t * Skip '%s' (no email)\n" % smart_unicode(phpbb_user.username))
                        continue
                if cleanup_users >= 2:
                    if not phpbb_user.lastvisit:
                        self.stdout.write(u"\t * Skip '%s' (no lastvisit)\n" % smart_unicode(phpbb_user.username))
                        continue
                if cleanup_users >= 3:
                    if not phpbb_user.posts:
                        self.stdout.write(u"\t * Skip '%s' (no posts)\n" % smart_unicode(phpbb_user.username))
                        continue

            last_login = phpbb_user.lastvisit_datetime()
            if not last_login:
                # can't be None in User model:
                last_login = datetime.datetime(year=datetime.MINYEAR, month=1, day=1)

            # FIXME:
            #     * Clean username (remove non-ascii)
            #     * check doublicates via email compare 

            django_user, created = User.objects.get_or_create(
                username=phpbb_user.username,
                defaults={
                    "email":phpbb_user.email,
                    "is_staff": False,
                    "is_active": False,
                    "is_superuser": False,
                    "last_login": last_login,
                    "date_joined": phpbb_user.registration_datetime(),
                }
            )
            if created:
                self.stdout.write(u"\tUser '%s' created.\n" % smart_unicode(django_user.username))
                django_user.set_unusable_password()
                django_user.save()
            else:
                self.stdout.write(u"\tUser '%s' exists.\n" % smart_unicode(django_user.username))

            if phpbb_user.group in moderator_groups:
                self.stdout.write(u"\t *** Mark user '%s' as global forum moderator\n" % phpbb_user)
                moderators.append(django_user)

            user_dict[phpbb_user.id] = django_user

            tz = TZ_CHOICES[int(phpbb_user.timezone)][0]
            #print tz

            # TODO: migrate avatar, too!
            # see:
            # https://github.com/jedie/django-phpBB3/issues/6

            if phpbb_user.lang in lang_codes:
                language = phpbb_user.lang
            else:
                language = default_lang

            user_profile, created = Profile.objects.get_or_create(
                user=django_user,
                defaults={
                    "site": phpbb_user.website,
                    "signature": phpbb_user.sig,
                    #"signature_html": phpbb_user.sig,
                    "post_count": phpbb_user.posts,
                    "yahoo": phpbb_user.yim,

                    "time_zone": tz,
                    "language":language,

                    "jabber":phpbb_user.jabber,
                    "icq":phpbb_user.icq,
                    "msn":phpbb_user.msnm,
                    "aim":phpbb_user.aim,
                }
            )
            if created:
                self.stdout.write(u"\t - User profile for '%s' created.\n" % smart_unicode(django_user.username))
            else:
                self.stdout.write(u"\t - User profile for '%s' exists.\n" % smart_unicode(django_user.username))

        return user_dict, moderators

    def get_or_create_category(self, phpbb_forum):
        obj, created = Category.objects.get_or_create(
            name=smart_unicode(phpbb_forum.forum_name)
        )
        if created:
            self.stdout.write(u"\tCategory '%s' created.\n" % obj.name)
        else:
            self.stdout.write(u"\tCategory '%s' exists.\n" % obj.name)
        return obj

    def migrate_forums(self, moderators):
        self.stdout.write(u"\n *** Migrate phpbb_forum entries...\n")

        phpbb_forums = phpbb_Forum.objects.all()

        # Create categories
        category_dict = {}
        forum_dict = {}
        for phpbb_forum in phpbb_forums:
            #print phpbb_forum
            try:
                phpbb_forum.parent
            except phpbb_Forum.DoesNotExist:
                # has no parent -> is a Category
                # phpbb_forum.parent == 0 and a db item with ID 0 doesn't exist
                category = self.get_or_create_category(phpbb_forum)
                category_dict[phpbb_forum.id] = category
            else:
                # Has parent -> no Category
                continue

        # Create forums and categories for a sub forum
        for phpbb_forum in phpbb_forums:
            #print phpbb_forum
            try:
                # XXX: We can also use "forum_type"
                parent = phpbb_forum.parent
            except phpbb_Forum.DoesNotExist:
                # has no parent -> is a Category
                # skip, was created above
                continue

            try:
                category = category_dict[parent.id]
            except KeyError:
                # Create a new category for sub-forum
                parent = phpbb_Forum.objects.get(pk=parent.id)
                category = self.get_or_create_category(parent)
                category_dict[parent.id] = category

            obj, created = Forum.objects.get_or_create(
                name=smart_unicode(phpbb_forum.forum_name),
                defaults={
                    "category":category,
                    "description":phpbb_forum.forum_desc,

                    # TODO: set 'position' by flattern the btree

                    # These attributes would be set later in update_forum_stats():
                    # post_count, last_post, topic_count
                }
            )
            if created:
                self.stdout.write(u"\tForum '%s' created.\n" % smart_unicode(obj.name))
            else:
                self.stdout.write(u"\tForum '%s' exists.\n" % smart_unicode(obj.name))

            forum_dict[phpbb_forum.id] = obj

            for moderator in moderators:
                obj.moderators.add(moderator)
            obj.save()
            self.stdout.write(u"\t - moderators: %s\n" % obj.moderators.all())

        return forum_dict


    def migrate_topic(self, user_dict, forum_dict):
        self.stdout.write(u"\n *** Migrate phpBB topic entries...\n")

        self.stdout.write(u"\tget topic watch information...")
        self.stdout.flush()
        topic_watch = get_topic_watch()
        self.stdout.write(u"OK\n")
        self.stdout.flush()

        topic_dict = {}
        topics = phpbb_Topic.objects.all().order_by("time")
        total = topics.count()
        process_info = ProcessInfo(total, use_last_rates=4)
        count = 0
        start_time = time.time()
        next_status = start_time + 0.25
        for topic in topics:
            count += 1
            if time.time() > next_status:
                next_status = time.time() + 1
                rest, eta, rate = process_info.update(count)
                msg = (
                    "\r\t%i/%i topics migrated... rest: %i - eta: %s (rate: %.1f/sec)         "
                ) % (count, total, rest, eta, rate)
                self.stdout.write(msg)
                self.stdout.flush()

            if topic.moved():
                # skip moved topics -> DjangoBB doesn't support them
                continue

            user = user_dict[topic.poster.id]
            forum = forum_dict[topic.forum.id]

            if topic.type in (1, 2, 3):
                # convert sticky, announce and global post to sticky
                # 0 == NORMAL, 1 == STICKY, 2 == ANNOUNCE, 3 == GLOBAL
                sticky = True
            else:
                sticky = False

            obj = Topic.objects.create(
                id=topic.id,
                forum=forum,
                user=user,
                name=topic.clean_title(),
                created=topic.create_datetime(),
                views=topic.views,
                sticky=sticky,
                closed=topic.locked(),

                # These attributes would be set later in update_topic_stats():
                # updated, post_count, last_post
            )
            if topic.id in topic_watch:
                subscribers = [user_dict[user_id] for user_id in topic_watch[topic.id]]
                obj.subscribers = subscribers
                obj.save()

            topic_dict[topic.id] = obj

        duration = time.time() - start_time
        rate = float(count) / duration
        self.stdout.write(
            "\r *** %i topics migrated in %s (rate: %.1f/sec)\n" % (
                count, human_duration(duration), rate
            )
        )
        return topic_dict


    def migrate_posts(self, user_dict, topic_dict):
        self.stdout.write(u"\n *** Migrate phpBB posts entries...\n")

        posts = phpbb_Post.objects.all().order_by("time")
        total = posts.count()
        process_info = ProcessInfo(total, use_last_rates=4)
        count = 0
        start_time = time.time()
        next_status = start_time + 0.25
        for phpbb_post in posts:
            count += 1
            if time.time() > next_status:
                next_status = time.time() + 1
                rest, eta, rate = process_info.update(count)
                msg = (
                    "\r\t%i/%i posts migrated... rest: %i - eta: %s (rate: %.1f/sec)         "
                ) % (count, total, rest, eta, rate)
                self.stdout.write(msg)
                self.stdout.flush()

            topic = topic_dict[phpbb_post.topic.id]
            user = user_dict[phpbb_post.poster.id]

            if phpbb_post.edit_user > 0 and phpbb_post.edit_time > 0:
                updated = phpbb_post.update_datetime()
                updated_by = user_dict[phpbb_post.edit_user]
            else:
                updated = None
                updated_by = None

            try:
                post = Post.objects.create(
                    id=phpbb_post.id,
                    topic=topic,
                    user=user,
                    created=phpbb_post.create_datetime(),
                    updated=updated,
                    updated_by=updated_by,
                    markup="bbcode",
                    body=phpbb_post.get_cleaned_bbcode(),
                    #body_html=html, # would be generated in save()
                    user_ip=phpbb_post.poster_ip,
                )
            except Exception, err:
                raise
                msg = (
                    "\n +++ ERROR: creating Post entry for phpBB3 post (ID: %s):\n"
                    "%s\n"
                ) % (phpbb_post.id, err)
                self._warn(msg)
                continue

            if phpbb_post.has_attachment():
                # copy attachment files
                phpbb_attachments = phpbb_Attachment.objects.filter(post_msg=phpbb_post)
                for phpbb_attachment in phpbb_attachments:
                    src_path = os.path.join(settings.PHPBB_ATTACHMENT_PATH, phpbb_attachment.physical_filename)
                    if not os.path.isfile(src_path):
                        self._warn("\n +++ ERROR: Attachment not found: '%s'\n" % src_path)
                    else:
                        attachment = Attachment(
                            size=phpbb_attachment.filesize,
                            content_type=phpbb_attachment.mimetype,
                            name=phpbb_attachment.real_filename,
                            post=post
                        )
                        filename = "%d.0" % post.id
                        dst_path = os.path.join(
                            settings.MEDIA_ROOT, forum_settings.ATTACHMENT_UPLOAD_TO,
                            filename
                        )
                        shutil.copy(src_path, dst_path)
                        attachment.path = filename
                        attachment.save()
                        self.stdout.write(
                            "\n\t *** Attachment %s copied in: %s\n" % (
                                attachment.name, dst_path
                            )
                        )
                        self.stdout.flush()

        duration = time.time() - start_time
        rate = float(count) / duration
        self.stdout.write(
            "\r *** %i posts migrated in %s (rate: %.1f/sec)\n" % (
                count, human_duration(duration), rate
            )
        )

    def update_topic_stats(self):
        self.stdout.write(u"\n *** set topic stats...\n")

        topics = Topic.objects.all()
        total = topics.count()
        process_info = ProcessInfo(total, use_last_rates=4)
        start_time = time.time()
        next_status = time.time() + 0.25
        for count, topic in enumerate(topics):
            if time.time() > next_status:
                next_status = time.time() + 1
                rest, eta, rate = process_info.update(count)
                msg = (
                    "\r\t%i/%i topics... rest: %i - eta: %s (rate: %.1f/sec)         "
                ) % (count, total, rest, eta, rate)
                self.stdout.write(msg)
                self.stdout.flush()

            queryset = Post.objects.only("created", "updated").filter(topic=topic)
            topic.post_count = queryset.count()
            try:
                last_post = queryset.latest("updated")
            except Post.DoesNotExist:
                # there is no post in this forum
                pass
            else:
                topic.last_post = last_post
                if last_post.updated:
                    topic.updated = last_post.updated
                else:
                    topic.updated = last_post.created
            topic.save()

        duration = time.time() - start_time
        rate = float(count) / duration
        self.stdout.write(
            "\r *** %i topic stats set in %s (rate: %.1f/sec)\n" % (
                count, human_duration(duration), rate
            )
        )

    def update_forum_stats(self):
        self.stdout.write(u"\n *** set forum stats...\n")

        for forum in Forum.objects.all():
            self.stdout.write(u"\tset stats for %s\n" % forum)
            queryset = Post.objects.all().filter(topic__forum=forum)
            forum.post_count = queryset.count()
            try:
                forum.last_post = queryset.latest("created")
            except Post.DoesNotExist:
                # there is no post in this forum
                pass

            queryset = Topic.objects.all().filter(forum=forum)
            forum.topic_count = queryset.count()

            forum.save()
