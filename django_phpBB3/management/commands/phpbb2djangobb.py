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
import shutil
import sys
import time
import traceback

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "phpBB2DjangoBB_project.settings"
    from django.core import management
#    print "reset 'djangobb_forum'...",
#    management.call_command("reset", "djangobb_forum", interactive=False)
#    print "OK"
    management.call_command("phpbb2djangobb", flush_djangobb=True, interactive=False)
    management.call_command("phpbb2djangobb", max_entries=10)
    #management.call_command("phpbb2djangobb", cleanup_users=3)
    sys.exit()

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models.signals import post_save
from django.utils.encoding import smart_unicode, smart_str

from haystack import site

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

try:
    from pip.util import get_terminal_size
except ImportError:
    TERMINAL_WIDTH = 79
else:
    TERMINAL_WIDTH = get_terminal_size()[0] - 1


try:
    import pudb as debugger # http://pypi.python.org/pypi/pudb
except ImportError:
    import pdb as debugger


OUT_ENCODING = sys.stdout.encoding or sys.getfilesystemencoding()


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
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--cleanup_users',
            action='store',
            dest='cleanup_users',
            default='2',
            type='choice', choices=['0', '1', '2', '3'],
            help='Which user to migrate: 0:all users, 1:with email, 2:+lastvisit (default), 3:+has post'
        ),
        make_option('--flush_djangobb', action='store_true',
            help='Delete all DjangoBB forum models. (For testing, only)'
        ),
        make_option('--max_entries', type="int",
            help='Migrate only a few users/topics/posts. (For testing, only)'
        ),
    )

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except Exception:
            print "-"*TERMINAL_WIDTH
            traceback.print_exc()
            print "-"*TERMINAL_WIDTH
            debugger.post_mortem()

    def _handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        self.interactive = options.get('interactive')

        flush_djangobb = options.get("flush_djangobb", False)
        if flush_djangobb:
            self._flush_djangobb()
            return

        self.max_entries = options.get("max_entries")
        if self.max_entries:
            self.warn("Migrate with max entries: %i !\n" % self.max_entries)

        self.check_attachment_path()
        self.check_models()

        # disable DjangoBB signals for speedup
        post_save.disconnect(djangobb_signals.post_saved, sender=Post, dispatch_uid='djangobb_post_save')
        post_save.disconnect(djangobb_signals.topic_saved, sender=Topic, dispatch_uid='djangobb_topic_save')

        # Speedup migration by disable haystack search index creation.
        site.unregister(Post)

        #disable_auto_fields(Forum)
        disable_auto_fields(Topic)
        disable_auto_fields(Post)

        cleanup_users = int(options.get("cleanup_users"))
        moderator_groups = phpbb_Group.objects.filter(
            name__in=["ADMINISTRATORS", "GLOBAL_MODERATORS"]
        )
        user_dict, moderators = self.migrate_users(cleanup_users, moderator_groups)

        forum_dict = self.migrate_forums(moderators)

        self.migrate_topic(user_dict, forum_dict)
        self.migrate_posts(user_dict)

        # needed if signals disabled, see above
        self.update_topic_stats()
        self.update_forum_stats()

        self.out(u"\nmigration done.\n")

    def _out_encode(self, msg):
        # see: https://github.com/jedie/django-phpBB3/issues/9#issuecomment-8494830
        msg = smart_str(msg, encoding=OUT_ENCODING, errors="replace")
        msg = msg.replace("\t", "    ") # Helpful in out_update()
        return msg

    def warn(self, msg):
        self.stderr.write(self.style.ERROR(self._out_encode(msg)))
        self.stderr.flush()

    def out(self, msg):
        self.stdout.write(self._out_encode(msg))
        self.stdout.flush()

    def err(self, msg):
        self.stderr.write(self._out_encode(msg))
        self.stdout.flush()

    def _out_justify(self, msg):
        self.stdout.write(msg.ljust(TERMINAL_WIDTH))

    def out_update(self, msg):
        msg = self._out_encode(msg)
        self.stdout.write("\r")
        self._out_justify(msg)
        self.stdout.flush()

    def out_overwrite(self, msg):
        self.out_update(msg)
        self.stdout.write("\n")
        self.stdout.flush()

    def _flush_djangobb(self):
        self.warn("Delete all DjangoBB data.\n")
        if self.interactive:
            confirm = raw_input("Continue? (yes/no): ")
            while 1:
                if confirm.lower().startswith("n"):
                    sys.exit("-1")
                if confirm.lower() != "yes":
                    confirm = raw_input('Please enter either "yes" or "no": ')
                    continue
                break

        for ModelClass in (Attachment, Post, Topic, Forum, Profile, Category):
            count = ModelClass.objects.all().count()
            self.out(" *** Delete %i '%s' model entries..." % (count, ModelClass.__name__))
            ModelClass.objects.all().delete()
            self.out("OK\n")

    def check_attachment_path(self):
        attachment_count = phpbb_Attachment.objects.count()
        self.out(self.style.NOTICE("This phpBB3 Forum has %i Attachment(s).\n" % attachment_count))
        if attachment_count == 0:
            # Don't check paths if no attachments exists.
            return

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
                self.warn("WARNING: file '%s' doesn't exists!\n" % test_path)

        djangobb_path = os.path.join(settings.MEDIA_ROOT, forum_settings.ATTACHMENT_UPLOAD_TO)
        if not os.path.isdir(djangobb_path):
            msg = (
                "DjangoBB attachment path '%s' doesn't exists!"
                " Please check MEDIA_ROOT + ATTACHMENT_UPLOAD_TO in your local_settings.py!"
            ) % djangobb_path
            raise CommandError(msg)

    def check_models(self):
        has_entries = False
        for ModelClass in (Category, Forum, Profile, Post, Topic, Attachment):
            count = ModelClass.objects.all().count()
            if count != 0:
                has_entries = True
                self.err("ERROR: '%s' model has %i entries!\n" % (ModelClass.__name__, count))
        if has_entries:
            self.warn("Maybe you have missed to use '--flush_djangobb' ?\n")
            if self.interactive:
                confirm = raw_input("\nContinue? (yes/no): ")
                while 1:
                    if confirm.lower().startswith("n"):
                        sys.exit("-1")
                    if confirm.lower() != "yes":
                        confirm = raw_input('Please enter either "yes" or "no": ')
                        continue
                    break

    def migrate_users(self, cleanup_users, moderator_groups):
        self.out(u"\n *** Migrate phpbb_forum users...\n")

        lang_codes = [i[0] for i in settings.LANGUAGES]
        default_lang = settings.LANGUAGE_CODE.split("-")[0]

        moderators = []
        user_dict = {}
        phpbb_users = phpbb_User.objects.all()

        total = phpbb_users.count()
        process_info = ProcessInfo(total, use_last_rates=4)
        skip_count = 0
        start_time = time.time()
        next_status = start_time + 0.25
        for count, phpbb_user in enumerate(phpbb_users, 1):
            if self.max_entries and count >= self.max_entries:
                self.warn("Skip rest of users because max_entries used!")
                break

            if time.time() > next_status:
                next_status = time.time() + 1
                rest, eta, rate = process_info.update(count)
                self.out_update(
                    "\t%i/%i users migrated %i skiped... rest: %i - eta: %s (rate: %.1f/sec)" % (
                        count, total, skip_count, rest, eta, rate
                    )
                )

            if not phpbb_user.posts:
                #assert phpbb_user.has_content() == False

                # Only users with has no posts can be skip.
                if cleanup_users >= 1:
                    if not phpbb_user.email:
                        skip_count += 1
                        if self.verbosity >= 2:
                            self.out_overwrite(
                                u"\t * Skip '%s' (no email)" % smart_unicode(phpbb_user.username)
                            )
                        continue
                if cleanup_users >= 2:
                    if not phpbb_user.lastvisit:
                        skip_count += 1
                        if self.verbosity >= 2:
                            self.out_overwrite(
                                u"\t * Skip '%s' (no lastvisit)" % smart_unicode(phpbb_user.username)
                            )
                        continue
                if cleanup_users >= 3:
                    if not phpbb_user.posts:
                        skip_count += 1
                        if self.verbosity >= 2:
                            self.out_overwrite(
                                u"\t * Skip '%s' (no posts)" % smart_unicode(phpbb_user.username)
                            )
                        continue

            last_login = phpbb_user.lastvisit_datetime()
            if not last_login:
                # can't be None in User model:
                last_login = datetime.datetime(year=datetime.MINYEAR, month=1, day=1)

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
                if self.verbosity >= 2:
                    self.out_overwrite(
                        u"\tUser '%s' created." % smart_unicode(django_user.username)
                    )
                django_user.set_unusable_password()
                django_user.save()
            else:
                if self.verbosity >= 2:
                    self.out_overwrite(
                        u"\tUser '%s' exists." % smart_unicode(django_user.username)
                    )

            if phpbb_user.group in moderator_groups:
                if self.verbosity >= 1:
                    self.out_overwrite(
                        u"\t *** Mark user '%s' as global forum moderator" % phpbb_user
                    )
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

            cleaned_signature = phpbb_user.get_cleaned_signature()

            user_profile, created = Profile.objects.get_or_create(
                user=django_user,
                defaults={
                    "site": phpbb_user.website,
                    "signature": cleaned_signature,
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
                if self.verbosity >= 2:
                    self.out_overwrite(
                        u"\t - User profile for '%s' created." % smart_unicode(django_user.username)
                    )
            else:
                if self.verbosity >= 2:
                    self.out_overwrite(
                        u"\t - User profile for '%s' exists." % smart_unicode(django_user.username)
                    )

        duration = time.time() - start_time
        rate = float(count) / duration
        self.out_overwrite(
            u" *** %i users migrated %i skiped in %s (rate: %.1f/sec)" % (
                count, skip_count, human_duration(duration), rate
            )
        )

        return user_dict, moderators

    def get_or_create_category(self, phpbb_forum):
        obj, created = Category.objects.get_or_create(
            name=smart_unicode(phpbb_forum.forum_name)
        )
        if created:
            self.out(u"\tCategory '%s' created.\n" % obj.name)
        else:
            self.out(u"\tCategory '%s' exists.\n" % obj.name)
        return obj

    def migrate_forums(self, moderators):
        self.out(u"\n *** Migrate phpbb_forum entries...\n")

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
                self.out(u"\tForum '%s' created.\n" % smart_unicode(obj.name))
            else:
                self.out(u"\tForum '%s' exists.\n" % smart_unicode(obj.name))

            forum_dict[phpbb_forum.id] = obj

            for moderator in moderators:
                obj.moderators.add(moderator)
            obj.save()
            self.out(u"\t - moderators: %s\n" % obj.moderators.all())

        return forum_dict

    def migrate_topic(self, user_dict, forum_dict):
        self.out(u"\n *** Migrate phpBB topic entries...\n")

        self.out(u"\tget topic watch information...")
        self.stdout.flush()
        topic_watch = get_topic_watch()
        self.out(u"OK\n")
        self.stdout.flush()

        anonymous_user = User.objects.get(username="Anonymous") # Pseudo account from phpBB

        topics = phpbb_Topic.objects.all().order_by("time")
        total = topics.count()
        process_info = ProcessInfo(total, use_last_rates=4)
        start_time = time.time()
        next_status = start_time + 0.25
        for count, topic in enumerate(topics, 1):
            if self.max_entries and count >= self.max_entries:
                self.warn("Skip rest of topics because max_entries used!")
                break

            if time.time() > next_status:
                next_status = time.time() + 1
                rest, eta, rate = process_info.update(count)
                self.out_update(
                    "\t%i/%i topics migrated... rest: %i - eta: %s (rate: %.1f/sec)" % (
                        count, total, rest, eta, rate
                    )
                )

            if topic.moved():
                # skip moved topics -> DjangoBB doesn't support them
                continue

            phpbb_user_id = topic.poster_id #topic.poster.id
            try:
                user = user_dict[phpbb_user_id]
            except KeyError:
                self.out_overwrite(self.style.NOTICE(
                    "topic %i poster: phpBB User with ID %i doesn't exist. Use Anonymous." % (
                        topic.id, phpbb_user_id
                    )
                ))
                user = anonymous_user

            forum = forum_dict[topic.forum_id]

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
                subscribers = []
                phpbb_user_ids = topic_watch[topic.id]
                for phpbb_user_id in phpbb_user_ids:
                    try:
                        user = user_dict[phpbb_user_id]
                    except KeyError:
                        continue # Skip not existing users.
                    subscribers.append(user)

                obj.subscribers = subscribers
                obj.save()

        duration = time.time() - start_time
        rate = float(count) / duration
        self.out_overwrite(
            " *** %i topics migrated in %s (rate: %.1f/sec)" % (
                count, human_duration(duration), rate
            )
        )

    def migrate_posts(self, user_dict):
        self.out(u"\n *** Migrate phpBB posts entries...\n")

        anonymous_user = User.objects.get(username="Anonymous") # Pseudo account from phpBB

        posts = phpbb_Post.objects.all().order_by("time")
        total = posts.count()
        process_info = ProcessInfo(total, use_last_rates=4)
        start_time = time.time()
        next_status = start_time + 0.25
        for count, phpbb_post in enumerate(posts, 1):
            if self.max_entries and count >= self.max_entries:
                self.warn("Skip rest of posts because max_entries used!")
                break

            if time.time() > next_status:
                next_status = time.time() + 1
                rest, eta, rate = process_info.update(count)
                self.out_update(
                    "\t%i/%i posts migrated... rest: %i - eta: %s (rate: %.1f/sec)" % (
                        count, total, rest, eta, rate
                    )
                )

            topic_id = phpbb_post.topic_id
            try:
                topic = Topic.objects.get(id=topic_id)
            except Topic.DoesNotExist:
                self.out_overwrite(self.style.NOTICE(
                    "topic for post %i doesn't exist! Skip post." % phpbb_post.id
                ))
                continue

            phpbb_user_id = phpbb_post.poster_id
            try:
                user = user_dict[phpbb_user_id]
            except KeyError:
                self.out_overwrite(self.style.NOTICE(
                    "phpBB User with ID %i doesn't exist for post %i. Use Anonymous." % (
                        phpbb_user_id, phpbb_post.id
                    )
                ))
                user = anonymous_user


            if phpbb_post.edit_user > 0 and phpbb_post.edit_time > 0:
                updated = phpbb_post.update_datetime()
                try:
                    updated_by = user_dict[phpbb_post.edit_user]
                except KeyError:
                    updated_by = anonymous_user
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
                self.out_overwrite(self.style.NOTICE(msg))
                continue

            if phpbb_post.has_attachment():
                # copy attachment files
                phpbb_attachments = phpbb_Attachment.objects.filter(post_msg=phpbb_post)
                for phpbb_attachment in phpbb_attachments:
                    src_path = os.path.join(settings.PHPBB_ATTACHMENT_PATH, phpbb_attachment.physical_filename)
                    if not os.path.isfile(src_path):
                        self.warn("\r\n +++ ERROR: Attachment not found: '%s'\n" % src_path)
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
                        self.out_overwrite(
                            "\t *** Attachment %s copied in: %s" % (
                                attachment.name, dst_path
                            )
                        )

        duration = time.time() - start_time
        rate = float(count) / duration
        self.out_overwrite(
            " *** %i posts migrated in %s (rate: %.1f/sec)" % (
                count, human_duration(duration), rate
            )
        )

    def update_topic_stats(self):
        self.out(u"\n *** set topic stats...\n")

        topics = Topic.objects.all()
        total = topics.count()
        process_info = ProcessInfo(total, use_last_rates=4)
        start_time = time.time()
        next_status = time.time() + 0.25
        for count, topic in enumerate(topics, 1):
            if time.time() > next_status:
                next_status = time.time() + 1
                rest, eta, rate = process_info.update(count)
                self.out_update(
                    "\t%i/%i topics... rest: %i - eta: %s (rate: %.1f/sec)" % (
                        count, total, rest, eta, rate
                    )
                )

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
        self.out_overwrite(
            " *** %i topic stats set in %s (rate: %.1f/sec)" % (
                count, human_duration(duration), rate
            )
        )

    def update_forum_stats(self):
        self.out(u"\n *** set forum stats...\n")

        for forum in Forum.objects.all():
            self.out(u"\tset stats for %s\n" % forum)
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
