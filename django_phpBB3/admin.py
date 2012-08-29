# coding: utf-8

from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_phpBB3.models import AclOption, AclRole, AclRoleData, \
    Attachment, Banlist, Bbcode, Bookmark, Bot, \
    Config, Confirm, Disallow, Draft, ExtensionGroup, Extension, \
    Forum, Group, Icon, Lang, Log, Module, Post, Privmsg, \
    PrivmsgFolder, PrivmsgRules, ProfileField, ProfileFieldData, \
    ProfileFieldLang, ProfileLang, Rank, Report, ReportReasons, \
    SearchResult, SearchWordlist, Session, Sitelist, \
    Smilie, Style, StyleImageset, StyleImagesetData, StyleTemplate, \
    StyleTemplateData, StyleTheme, Topic, TopicTrack, \
    User, Warning, Word, Zebra

if settings.PHPBB_CAPTCHA_QUESTIONS_MODEL_EXIST:
    from django_phpBB3.models import CaptchaQuestions

#
#These classes would need Django to support composite keys:
#
#class AclGroupAdmin(admin.ModelAdmin):
#    """
#    Permission roles and/or individual permissions assigned to groups
#    """
#    pass
#admin.site.register(AclGroup, AclGroupAdmin)
#


class UserAdmin(admin.ModelAdmin):
    """
    Registered users
    """
    list_display = (
        'id', 'username', 'registration_datetime', 'posts',
        'lastvisit_datetime', 'email'
    )
    list_display_links = ("username",)
    list_filter = ("group",)
admin.site.register(User, UserAdmin)


class ForumAdmin(admin.ModelAdmin):
    """
    Forum (Name, description, rules...)
    """
    list_display = ('id', "forum_name", "forum_desc", "forum_posts", "forum_topics_real")
    list_display_links = ("forum_name",)
admin.site.register(Forum, ForumAdmin)


class TopicAdmin(admin.ModelAdmin):
    """
    Topic in forums
    """
    def username(self, obj):
        return obj.poster.username

    list_display = ('id', "clean_title",
        #"title",
        "username", "moved", "locked", "type",
        "create_datetime", "last_post_datetime", "last_view_datetime",
    )
    list_display_links = ("clean_title",)
    list_filter = ("status", "type", "forum", "poster")
    search_fields = ("title",)
admin.site.register(Topic, TopicAdmin)


class PostAdmin(admin.ModelAdmin):
    """
    Topic posts
    """
    def poster_username(self, obj):
        return obj.poster.username
    poster_username.short_description = "username"

    list_display = ('id', "poster_username", "has_attachment", "create_datetime", "update_datetime", "teaser")
    list_filter = ("forum", "poster")
    search_fields = ("text",)
admin.site.register(Post, PostAdmin)


class AttachmentAdmin(admin.ModelAdmin):
    """
    Information on attachments (Post, physical filename, original filename, MIME type...)
    """
    def teaser(self, obj):
        return obj.post_msg.teaser()
    def username(self, obj):
        return obj.poster.username
    list_display = ('id', "real_filename", "filesize", "download_count", "username", "file_datetime", "teaser")
    list_display_links = ("real_filename",)
    list_filter = ("poster",)
admin.site.register(Attachment, AttachmentAdmin)


class LogAdmin(admin.ModelAdmin):
    """
    Administration/Moderation/Error logs
    """
    def username(self, obj):
        return obj.user.username
    def forum_name(self, obj):
        return obj.forum.forum_name
    def topic_title(self, obj):
        return obj.topic.topic_title

    list_display = ('id', "username", "log_operation", "log_time", "forum_name", "topic_title")
    list_display_links = ('id', "username", "log_operation", "log_time")
    list_filter = ("forum", "log_operation")
admin.site.register(Log, LogAdmin)

class GroupAdmin(admin.ModelAdmin):
    """
    Usergroups
    """
    pass
admin.site.register(Group, GroupAdmin)

#_______________________________________________________________________________
# default Admin classes:

class AclOptionAdmin(admin.ModelAdmin):
    """
    List of possible permissions
    """
    pass
admin.site.register(AclOption, AclOptionAdmin)

class AclRoleAdmin(admin.ModelAdmin):
    """
    Permission roles (Standard Moderator, Simple Moderator etc.)
    """
    pass
admin.site.register(AclRole, AclRoleAdmin)

class AclRoleDataAdmin(admin.ModelAdmin):
    """
    Permissions each role contains
    """
    pass
admin.site.register(AclRoleData, AclRoleDataAdmin)

class BanlistAdmin(admin.ModelAdmin):
    """
    Banned users/IPs/emails...
    """
    pass
admin.site.register(Banlist, BanlistAdmin)

class BbcodeAdmin(admin.ModelAdmin):
    """
    Custom BBCodes
    """
    pass
admin.site.register(Bbcode, BbcodeAdmin)

class BookmarkAdmin(admin.ModelAdmin):
    """
    Bookmarked topics
    """
    pass
admin.site.register(Bookmark, BookmarkAdmin)

class BotAdmin(admin.ModelAdmin):
    """
    Spiders/Robots
    """
    pass
admin.site.register(Bot, BotAdmin)


if settings.PHPBB_CAPTCHA_QUESTIONS_MODEL_EXIST:
    class CaptchaQuestionsAdmin(admin.ModelAdmin):
        pass
    admin.site.register(CaptchaQuestions, CaptchaQuestionsAdmin)


class ConfigAdmin(admin.ModelAdmin):
    """
    Configuration information ($config table)
    """
    pass
admin.site.register(Config, ConfigAdmin)

class ConfirmAdmin(admin.ModelAdmin):
    """
    Contains session information for confirm pages ("are you sure you want to delete foo")
    """
    pass
admin.site.register(Confirm, ConfirmAdmin)

class DisallowAdmin(admin.ModelAdmin):
    """
    Disallowed usernames
    """
    pass
admin.site.register(Disallow, DisallowAdmin)

class DraftAdmin(admin.ModelAdmin):
    """
    Draft of future posts/private messages
    """
    pass
admin.site.register(Draft, DraftAdmin)

class ExtensionGroupAdmin(admin.ModelAdmin):
    """
    Extension Group (associate extensions with a file type - Images, text...)
    """
    pass
admin.site.register(ExtensionGroup, ExtensionGroupAdmin)

class ExtensionAdmin(admin.ModelAdmin):
    """
    Extension (.xxx) allowed for attachments
    """
    pass
admin.site.register(Extension, ExtensionAdmin)

class IconAdmin(admin.ModelAdmin):
    """
    Post icons
    """
    pass
admin.site.register(Icon, IconAdmin)

class LangAdmin(admin.ModelAdmin):
    """
    Installed languages
    """
    pass
admin.site.register(Lang, LangAdmin)

class ModuleAdmin(admin.ModelAdmin):
    """
    Configuration of acp, mcp and ucp modules
    """
    pass
admin.site.register(Module, ModuleAdmin)

class PrivmsgAdmin(admin.ModelAdmin):
    """
    Private messages text
    """
    pass
admin.site.register(Privmsg, PrivmsgAdmin)

class PrivmsgFolderAdmin(admin.ModelAdmin):
    """
    Custom privates messages folders (for each user)
    """
    pass
admin.site.register(PrivmsgFolder, PrivmsgFolderAdmin)

class PrivmsgRulesAdmin(admin.ModelAdmin):
    """
    Messages rules, e.g. "if the username of the sender is ..., move the message to this folder".
    """
    pass
admin.site.register(PrivmsgRules, PrivmsgRulesAdmin)

class ProfileFieldAdmin(admin.ModelAdmin):
    """
    Custom profile fields (name, min/max number of characters, allowed characters...)
    """
    pass
admin.site.register(ProfileField, ProfileFieldAdmin)

class ProfileFieldDataAdmin(admin.ModelAdmin):
    """
    Data that users enter in custom profile fields
    """
    pass
admin.site.register(ProfileFieldData, ProfileFieldDataAdmin)

class ProfileFieldLangAdmin(admin.ModelAdmin):
    """
    tbd (empty on my forum with some custom profile fields)
    """
    pass
admin.site.register(ProfileFieldLang, ProfileFieldLangAdmin)

class ProfileLangAdmin(admin.ModelAdmin):
    """
    Localized name and description of custom profile fields (presented to users)
    """
    pass
admin.site.register(ProfileLang, ProfileLangAdmin)

class RankAdmin(admin.ModelAdmin):
    """
    Rank (Name, image, minimal # of posts)
    """
    pass
admin.site.register(Rank, RankAdmin)

class ReportAdmin(admin.ModelAdmin):
    """
    Reported posts
    """
    pass
admin.site.register(Report, ReportAdmin)

class ReportReasonsAdmin(admin.ModelAdmin):
    """
    Reasons for reported posts and disapprovals
    """
    pass
admin.site.register(ReportReasons, ReportReasonsAdmin)

class SearchResultAdmin(admin.ModelAdmin):
    """
    Last searches
    """
    pass
admin.site.register(SearchResult, SearchResultAdmin)

class SearchWordlistAdmin(admin.ModelAdmin):
    """
    Indexed words (for search)
    """
    pass
admin.site.register(SearchWordlist, SearchWordlistAdmin)

class SessionAdmin(admin.ModelAdmin):
    """
    Session (to identify users browsing the forum)
    """
    pass
admin.site.register(Session, SessionAdmin)

class SitelistAdmin(admin.ModelAdmin):
    """
    Secure Downloads of attachments - list of IPs and hostnames
    """
    pass
admin.site.register(Sitelist, SitelistAdmin)

class SmilieAdmin(admin.ModelAdmin):
    """
    Smilie (text => image)
    """
    pass
admin.site.register(Smilie, SmilieAdmin)

class StyleAdmin(admin.ModelAdmin):
    """
    Style = template + theme + imageset
    """
    pass
admin.site.register(Style, StyleAdmin)

class StyleImagesetAdmin(admin.ModelAdmin):
    """
    [[Templating_Tutorial#Customizing_the_Imageset|Imagesets]]
    """
    pass
admin.site.register(StyleImageset, StyleImagesetAdmin)

class StyleImagesetDataAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(StyleImagesetData, StyleImagesetDataAdmin)

class StyleTemplateAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(StyleTemplate, StyleTemplateAdmin)

class StyleTemplateDataAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(StyleTemplateData, StyleTemplateDataAdmin)

class StyleThemeAdmin(admin.ModelAdmin):
    """
    theme = css file
    """
    pass
admin.site.register(StyleTheme, StyleThemeAdmin)

class TopicTrackAdmin(admin.ModelAdmin):
    """
    Unread post information is stored here
    """
    pass
admin.site.register(TopicTrack, TopicTrackAdmin)

class WarningAdmin(admin.ModelAdmin):
    """
    Warning given to users
    """
    pass
admin.site.register(Warning, WarningAdmin)

class WordAdmin(admin.ModelAdmin):
    """
    censored words
    """
    pass
admin.site.register(Word, WordAdmin)

class ZebraAdmin(admin.ModelAdmin):
    """
    Friends and foes
    """
    pass
admin.site.register(Zebra, ZebraAdmin)
