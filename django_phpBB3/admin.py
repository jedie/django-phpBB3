# coding: utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_phpBB3.models import AclOption, AclRole, AclRoleData, \
    AclUser, Attachment, Banlist, Bbcode, Bookmark, Bot, CaptchaAnswers, \
    CaptchaQuestions, Config, Confirm, Disallow, Draft, ExtensionGroup, Extension, \
    Forum, ForumAccess, ForumTrack, ForumWatch, Group, Icon, Lang, Log, \
    LoginAttempt, ModeratorCache, Module, PollOption, PollVote, Post, Privmsg, \
    PrivmsgFolder, PrivmsgRules, PrivmsgTo, ProfileField, ProfileFieldData, \
    ProfileFieldLang, ProfileLang, QaConfirm, Rank, Report, ReportReasons, \
    SearchResult, SearchWordlist, SearchWordmatch, Session, SessionKey, Sitelist, \
    Smilie, Style, StyleImageset, StyleImagesetData, StyleTemplate, \
    StyleTemplateData, StyleTheme, Topic, TopicPosted, TopicTrack, TopicWatch, \
    UserGroup, User, Warning, Word, Zebra


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
    list_display = ('id','username','user_regdate','user_posts','user_email')
    list_display_links = ("username",)
admin.site.register(User, UserAdmin)


class ForumAdmin(admin.ModelAdmin):
    """
    Forum (Name, description, rules...)
    """
    list_display = ('id', "forum_name", "forum_desc", "forum_posts", "forum_topics_real")
    list_display_links = ("forum_name",)
admin.site.register(Forum, ForumAdmin)


class PostAdmin(admin.ModelAdmin):
    """
    Topic posts
    """
    def first_line(self, obj):
        return obj.post_text.strip().splitlines()[0]
    first_line.short_description = _("first line")

    list_display = ('id', "first_line")
    list_filter = ("forum", "poster")
    search_fields = ("post_text",)
admin.site.register(Post, PostAdmin)


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

class AclUserAdmin(admin.ModelAdmin):
    """
    Permission roles and/or individual permissions assigned to users
    """
    pass
admin.site.register(AclUser, AclUserAdmin)

class AttachmentAdmin(admin.ModelAdmin):
    """
    Information on attachments (Post, physical filename, original filename, MIME type...)
    """
    pass
admin.site.register(Attachment, AttachmentAdmin)

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

class CaptchaAnswersAdmin(admin.ModelAdmin):
    pass
admin.site.register(CaptchaAnswers, CaptchaAnswersAdmin)

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

class ForumAccessAdmin(admin.ModelAdmin):
    """
    Stores who is logged in to password protected forums
    """
    pass
admin.site.register(ForumAccess, ForumAccessAdmin)

class ForumTrackAdmin(admin.ModelAdmin):
    """
    Unread post information is stored here
    """
    pass
admin.site.register(ForumTrack, ForumTrackAdmin)

class ForumWatchAdmin(admin.ModelAdmin):
    """
    Subscribed forums
    """
    pass
admin.site.register(ForumWatch, ForumWatchAdmin)

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

class LogAdmin(admin.ModelAdmin):
    """
    Administration/Moderation/Error logs
    """
    pass
admin.site.register(Log, LogAdmin)

class LoginAttemptAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(LoginAttempt, LoginAttemptAdmin)

class ModeratorCacheAdmin(admin.ModelAdmin):
    """
    Who is a moderator in which forum (for display on forum index)
    """
    pass
admin.site.register(ModeratorCache, ModeratorCacheAdmin)

class ModuleAdmin(admin.ModelAdmin):
    """
    Configuration of acp, mcp and ucp modules
    """
    pass
admin.site.register(Module, ModuleAdmin)

class PollOptionAdmin(admin.ModelAdmin):
    """
    Options text of all votes ("Yes", "No", "Maybe"...)
    """
    pass
admin.site.register(PollOption, PollOptionAdmin)

class PollVoteAdmin(admin.ModelAdmin):
    """
    User which have voted on a poll
    """
    pass
admin.site.register(PollVote, PollVoteAdmin)

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

class PrivmsgToAdmin(admin.ModelAdmin):
    """
    Information (sender, new, replied...) on private messages.
    """
    pass
admin.site.register(PrivmsgTo, PrivmsgToAdmin)

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

class QaConfirmAdmin(admin.ModelAdmin):
    pass
admin.site.register(QaConfirm, QaConfirmAdmin)

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

class SearchWordmatchAdmin(admin.ModelAdmin):
    """
    Associate a post with indexed words
    """
    pass
admin.site.register(SearchWordmatch, SearchWordmatchAdmin)

class SessionAdmin(admin.ModelAdmin):
    """
    Session (to identify users browsing the forum)
    """
    pass
admin.site.register(Session, SessionAdmin)

class SessionKeyAdmin(admin.ModelAdmin):
    """
    Autologin feature
    """
    pass
admin.site.register(SessionKey, SessionKeyAdmin)

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

class TopicAdmin(admin.ModelAdmin):
    """
    Topic in forums
    """
    pass
admin.site.register(Topic, TopicAdmin)

class TopicPostedAdmin(admin.ModelAdmin):
    """
    Who posted to which topic (used for the small dots in viewforum)
    """
    pass
admin.site.register(TopicPosted, TopicPostedAdmin)

class TopicTrackAdmin(admin.ModelAdmin):
    """
    Unread post information is stored here
    """
    pass
admin.site.register(TopicTrack, TopicTrackAdmin)

class TopicWatchAdmin(admin.ModelAdmin):
    """
    "notify me upon replies"
    """
    pass
admin.site.register(TopicWatch, TopicWatchAdmin)

class UserGroupAdmin(admin.ModelAdmin):
    """
    User groups
    """
    pass
admin.site.register(UserGroup, UserGroupAdmin)

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
