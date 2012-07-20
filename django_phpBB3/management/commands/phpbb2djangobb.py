# coding: utf-8

"""
    migrate phpBB3 to DjangoBB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
import datetime
import time
if __name__ == "__main__":
    import os
    import sys
    os.environ["DJANGO_SETTINGS_MODULE"] = "django_phpBB3_project.settings"
    from django.core import management
    management.call_command("phpbb2djangobb",
        clear_tables=True,
        cleanup_users=3
    )
    sys.exit()

from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from postmarkup import render_bbcode
from djangobb_forum.models import Category, Forum, Profile, TZ_CHOICES, Post, Topic

from django_phpBB3.models import Forum as phpbb_Forum
from django_phpBB3.models import Topic as phpbb_Topic
from django_phpBB3.models import Group as phpbb_Group
from django_phpBB3.models import User as phpbb_User
from django_phpBB3.models import Post as phpbb_Post


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
        make_option('--clear_tables',
            action='store_true',
            dest='clear_tables',
            default=False,
            help='Delete all DjangoBB entries before migrate. WARNING: Made a backup of existing data!'
        ),
        make_option('--cleanup_users',
            action='store',
            dest='cleanup_users',
            default='2',
            type='choice', choices=['0', '1', '2', '3'],
            help='Which user to migrate: 0:all users, 1:with email, 2:+lastvisit (default), 3:+has post'
        ),

    )

    def handle(self, *args, **options):
        clear_tables = options.get("clear_tables")
        if clear_tables:
            self.clear_tables()

        #disable_auto_fields(Forum)
        disable_auto_fields(Topic)
        disable_auto_fields(Post)

        cleanup_users = int(options.get("cleanup_users"))
        moderator_groups = phpbb_Group.objects.filter(
            name__in=["ADMINISTRATORS", "GLOBAL_MODERATORS"]
        )
        user_dict, moderators = self.migrate_users(cleanup_users, moderator_groups)

        forum_dict = self.migrate_forums(moderators)

        topic_dict, last_post_dict = self.migrate_topic(user_dict, forum_dict)
        post_id_dict = self.migrate_posts(user_dict, topic_dict, last_post_dict)

        self.set_last_post(post_id_dict, last_post_dict)

        self.stdout.write("\nmigration done.\n")

    def clear_tables(self):
        self.stdout.write("Delete all DjangoBB entries...\n")
        Category.objects.all().delete()
        Forum.objects.all().delete()
        Profile.objects.all().delete()
        #User.objects.all().exclude(username="test").delete()

    def migrate_users(self, cleanup_users, moderator_groups):
        self.stdout.write("Migrate phpbb_forum users...\n")

        moderators = []
        user_dict = {}
        phpbb_users = phpbb_User.objects.all()
        for phpbb_user in phpbb_users:
            if not phpbb_user.posts:
                # Only users with has no posts can be skip.
                if cleanup_users >= 1:
                    if not phpbb_user.email:
                        self.stdout.write("\t * Skip '%s' (no email)\n" % phpbb_user)
                        continue
                if cleanup_users >= 2:
                    if not phpbb_user.lastvisit:
                        self.stdout.write("\t * Skip '%s' (no lastvisit)\n" % phpbb_user)
                        continue
                if cleanup_users >= 3:
                    if not phpbb_user.posts:
                        self.stdout.write("\t * Skip '%s' (no posts)\n" % phpbb_user)
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
                self.stdout.write("\tUser '%s' created.\n" % django_user)
                django_user.set_unusable_password()
                django_user.save()
            else:
                self.stdout.write("\tUser '%s' exists.\n" % django_user)

            if phpbb_user.group in moderator_groups:
                self.stdout.write("\t *** Mark user '%s' as global forum moderator\n" % phpbb_user)
                moderators.append(django_user)

            user_dict[phpbb_user.id] = django_user

            tz = TZ_CHOICES[int(phpbb_user.timezone)][0]
            #print tz

            user_profile, created = Profile.objects.get_or_create(
                user=django_user,
                defaults={
                    "site": phpbb_user.website,
                    "signature": phpbb_user.sig,
                    #"signature_html": phpbb_user.sig,

                    "time_zone": tz,

                    "jabber":phpbb_user.jabber,
                    "icq":phpbb_user.icq,
                    "msn":phpbb_user.msnm,
                    "aim":phpbb_user.aim,

                }
            )
            if created:
                self.stdout.write("\t - User profile for '%s' created.\n" % django_user)
            else:
                self.stdout.write("\t - User profile for '%s' exists.\n" % django_user)

        return user_dict, moderators

    def get_or_create_category(self, phpbb_forum):
        obj, created = Category.objects.get_or_create(
            name=phpbb_forum.forum_name
        )
        if created:
            self.stdout.write("\tCategory '%s' created.\n" % obj)
        else:
            self.stdout.write("\tCategory '%s' exists.\n" % obj)
        return obj

    def migrate_forums(self, moderators):
        self.stdout.write("Migrate phpbb_forum entries...\n")

        phpbb_forums = phpbb_Forum.objects.all()

        # Create Categories
        category_dict = {}
        forum_dict = {}
        for phpbb_forum in phpbb_forums:
            #print phpbb_forum
            try:
                # XXX: We can also use "forum_type"
                phpbb_forum.parent
            except phpbb_Forum.DoesNotExist:
                # has no parent -> is a Category
                # phpbb_forum.parent == 0 and a db item with ID 0 doesn't exist
                category = self.get_or_create_category(phpbb_forum)
                category_dict[phpbb_forum.id] = category
            else:
                # Has parent -> no Categorie
                continue


        # Create Categories
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
            except KeyError as err:
                parent = phpbb_Forum.objects.get(pk=parent.id)
                category = self.get_or_create_category(parent)
                category_dict[parent.id] = category

            obj, created = Forum.objects.get_or_create(
                name=phpbb_forum.forum_name,
                defaults={
                    "category":category,
                    "description":phpbb_forum.forum_desc,
                    #"updated": phpbb_forum.last_post_datetime(),
                    #    position
                    #    post_count
                    #    topic_count
                    #    last_post
                }
            )
            if created:
                self.stdout.write("\tForum '%s' created.\n" % obj)
            else:
                self.stdout.write("\tForum '%s' exists.\n" % obj)

            forum_dict[phpbb_forum.id] = obj

            for moderator in moderators:
                obj.moderators.add(moderator)
            obj.save()
            self.stdout.write("\t - moderators: %s\n" % obj.moderators.all())

        return forum_dict


    def migrate_topic(self, user_dict, forum_dict):
        self.stdout.write("Migrate phpBB topic entries...\n")

        last_post_dict = {}
        topic_dict = {}
        topics = phpbb_Topic.objects.all().order_by("time")
        total = topics.count()
        count = 0
        next_status = time.time() + 0.25
        for topic in topics:
            count += 1
            if time.time() > next_status:
                self.stdout.write("\r\t%i/%i topics migrated...          " % (count, total))
                next_status = time.time() + 1

            if topic.moved():
                # skip moved topics -> DjangoBB doesn't support them
                continue

            user = user_dict[topic.poster.id]
            forum = forum_dict[topic.forum.id]

            if topic.type in (1, 2):
                # POST_NORMAL(0), POST_STICKY(1), POST_ANNOUNCE(2) or POST_GLOBAL(3)
                # POST_GLOBAL not supported by DjangoBB
                sticky = True
            else:
                sticky = False

            obj, created = Topic.objects.get_or_create(
                forum=forum,
                user=user,
                name=topic.title,
                defaults={
                    "created": topic.create_datetime(),
                    "updated": topic.last_post_datetime(),
                    "views": topic.views,
                    "sticky": sticky,
                    "closed": topic.locked(),
                    #"subscribers":, # FIXME: ForumWatch / TopicWatch models are unsupported
                    "post_count": topic.replies_real,
                    "last_post": None, # will be set in migrate_posts()
                }
            )
#            if created:
#                self.stdout.write("\tTopic '%s' created.\n" % obj)
#            else:
#                self.stdout.write("\tTopic '%s' exists.\n" % obj)

            last_post_dict[obj] = topic.last_post.id
            topic_dict[topic.id] = obj

        self.stdout.write("\n *** %i topics migrated.\n" % count)
        return topic_dict, last_post_dict


    def migrate_posts(self, user_dict, topic_dict, last_post_dict):
        self.stdout.write("Migrate phpBB posts entries...\n")

        post_id_dict = {}

        posts = phpbb_Post.objects.all().order_by("time")
        total = posts.count()
        count = 0
        next_status = time.time() + 0.25
        for phpbb_post in posts:
            count += 1
            if time.time() > next_status:
                self.stdout.write("\r\t%i/%i posts migrated...          " % (count, total))
                next_status = time.time() + 1

            if phpbb_post.has_attachment():
                self.stdout.write("\n\t *** TODO: transfer attachment!\n")

            topic = topic_dict[phpbb_post.topic.id]
            user = user_dict[phpbb_post.poster.id]

            if phpbb_post.edit_user > 0 and phpbb_post.edit_time > 0:
                updated = phpbb_post.update_datetime()
                updated_by = user_dict[phpbb_post.edit_user]
            else:
                updated = None
                updated_by = None

            obj, created = Post.objects.get_or_create(
                topic=topic,
                user=user,
                defaults={
                    "created": phpbb_post.create_datetime(),
                    "updated": updated,
                    "updated_by": updated_by,
                    "markup": "bbcode",
                    "body": phpbb_post.text,
                    #"body_html": html, # would be generated in save()
                    "user_ip": phpbb_post.poster_ip,
                }
            )

            post_id_dict[phpbb_post.id] = obj.id

        self.stdout.write("\n *** %i posts migrated.\n" % count)
        return post_id_dict

    def set_last_post(self, post_id_dict, last_post_dict):
        self.stdout.write("\nTODO!\n")
#        self.stdout.write("set last post information...\n")
#
#        for topic, last_post_id in last_post_dict.items():
#            last_post_phpbb_id = post_id_dict[last_post_id]
#            
#            last_post = 
#
#            print "set last post %s to topic %s" % (last_post, topic)
#
#            topic.last_post = last_post
#            topic.save()

