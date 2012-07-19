# coding: utf-8

"""
    migrate phpBB3 to DjangoBB
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    :copyleft: 2012 by the django-phpBB3 team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
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

from djangobb_forum.models import Category, Forum, Profile, TZ_CHOICES

from django_phpBB3.models import Forum as phpbb_Forum
from django_phpBB3.models import User as phpbb_User


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

        self.migrate_forums()

        cleanup_users = int(options.get("cleanup_users"))
        self.migrate_users(cleanup_users)

        self.stdout.write("\nmigration done.\n")

    def clear_tables(self):
        self.stdout.write("Delete all DjangoBB entries...\n")
        Category.objects.all().delete()
        Forum.objects.all().delete()
        Profile.objects.all().delete()
        #User.objects.all().exclude(username="test").delete()

    def migrate_forums(self):
        self.stdout.write("Migrate phpbb_forum entries...\n")

        phpbb_forums = phpbb_Forum.objects.all()

        # Create Categories
        category_dict = {}
        for phpbb_forum in phpbb_forums:
            #print phpbb_forum
            try:
                # XXX: We can also use "forum_type"
                phpbb_forum.parent
            except phpbb_Forum.DoesNotExist:
                # has no parent -> is a Category
                # phpbb_forum.parent == 0 and a db item with ID 0 doesn't exist
                obj, created = Category.objects.get_or_create(
                    name=phpbb_forum.forum_name
                )
                if created:
                    self.stdout.write("\tCategory '%s' created.\n" % obj)
                else:
                    self.stdout.write("\tCategory '%s' exists.\n" % obj)
                category_dict[phpbb_forum.id] = obj
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

            category = category_dict[parent.id]

            obj, created = Forum.objects.get_or_create(
                name=phpbb_forum.forum_name,
                defaults={
                    "category":category,
                    "description":phpbb_forum.forum_desc,
                    #    position             
                    #    moderators
                    #    post_count
                    #    topic_count
                    #    last_post
                }
            )
            if created:
                self.stdout.write("\tForum '%s' created.\n" % obj)
            else:
                self.stdout.write("\tForum '%s' exists.\n" % obj)

    def migrate_users(self, cleanup_users):
        self.stdout.write("Migrate phpbb_forum users...\n")

        phpbb_users = phpbb_User.objects.all()
        for phpbb_user in phpbb_users:
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

            django_user, created = User.objects.get_or_create(
                username=phpbb_user.username,
                defaults={
                    "email":phpbb_user.email,
                    "is_staff": False,
                    "is_active": False,
                    "is_superuser": False,
                    "last_login": phpbb_user.lastvisit_datetime(),
                    "date_joined": phpbb_user.registration_datetime(),
                }
            )
            if created:
                self.stdout.write("\tUser '%s' created.\n" % django_user)
                django_user.set_unusable_password()
                django_user.save()
            else:
                self.stdout.write("\tUser '%s' exists.\n" % django_user)


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
                self.stdout.write("\tUser profile for '%s' created.\n" % django_user)
            else:
                self.stdout.write("\tUser profile for '%s' exists.\n" % django_user)


"""
class Profile(models.Model):
    user = AutoOneToOneField(User, related_name='forum_profile', verbose_name=_('User'))
    status = models.CharField(_('Status'), max_length=30, blank=True)
    site = models.URLField(_('Site'), verify_exists=False, blank=True)
    jabber = models.CharField(_('Jabber'), max_length=80, blank=True)
    icq = models.CharField(_('ICQ'), max_length=12, blank=True)
    msn = models.CharField(_('MSN'), max_length=80, blank=True)
    aim = models.CharField(_('AIM'), max_length=80, blank=True)
    yahoo = models.CharField(_('Yahoo'), max_length=80, blank=True)
    location = models.CharField(_('Location'), max_length=30, blank=True)
    signature = models.TextField(_('Signature'), blank=True, default='', max_length=forum_settings.SIGNATURE_MAX_LENGTH)
    signature_html = models.TextField(_('Signature'), blank=True, default='', max_length=forum_settings.SIGNATURE_MAX_LENGTH)
    time_zone = models.FloatField(_('Time zone'), choices=TZ_CHOICES, default=float(forum_settings.DEFAULT_TIME_ZONE))
    language = models.CharField(_('Language'), max_length=5, default='', choices=settings.LANGUAGES)
    avatar = ExtendedImageField(_('Avatar'), blank=True, default='', upload_to=forum_settings.AVATARS_UPLOAD_TO, width=forum_settings.AVATAR_WIDTH, height=forum_settings.AVATAR_HEIGHT)
    theme = models.CharField(_('Theme'), choices=THEME_CHOICES, max_length=80, default='default')
    show_avatar = models.BooleanField(_('Show avatar'), blank=True, default=True)
    show_signatures = models.BooleanField(_('Show signatures'), blank=True, default=True)
    show_smilies = models.BooleanField(_('Show smilies'), blank=True, default=True)
    privacy_permission = models.IntegerField(_('Privacy permission'), choices=PRIVACY_CHOICES, default=1)
    markup = models.CharField(_('Default markup'), max_length=15, default=forum_settings.DEFAULT_MARKUP, choices=MARKUP_CHOICES)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)

"""
