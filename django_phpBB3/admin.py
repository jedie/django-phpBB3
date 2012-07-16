# coding: utf-8

from django.contrib import admin

from django_phpBB3.models import AclOptions, AclRoles, AclRolesData, \
    AclUsers, Attachments, Banlist, Bbcodes, Bookmarks, Bots, CaptchaAnswers, \
    CaptchaQuestions, Config, Confirm, Disallow, Drafts, ExtensionGroups, Extensions, \
    Forums, ForumsAccess, ForumsTrack, ForumsWatch, Group, Icons, Lang, Log, \
    LoginAttempts, ModeratorCache, Modules, PollOptions, PollVotes, Posts, Privmsgs, \
    PrivmsgsFolder, PrivmsgsRules, PrivmsgsTo, ProfileFields, ProfileFieldsData, \
    ProfileFieldsLang, ProfileLang, QaConfirm, Ranks, Reports, ReportsReasons, \
    SearchResults, SearchWordlist, SearchWordmatch, Sessions, SessionsKeys, Sitelist, \
    Smilies, Styles, StylesImageset, StylesImagesetData, StylesTemplate, \
    StylesTemplateData, StylesTheme, Topics, TopicsPosted, TopicsTrack, TopicsWatch, \
    UserGroup, User, Warnings, Words, Zebra


#
#These classes would need Django to support composite keys:
#
#class AclGroupsAdmin(admin.ModelAdmin):
#    """
#    Permission roles and/or individual permissions assigned to groups
#    """
#    pass
#admin.site.register(AclGroups, AclGroupsAdmin)
#


class UserAdmin(admin.ModelAdmin):
    """
    Registered users
    """
    list_display = ('username','user_id','user_regdate','user_posts','user_email')
admin.site.register(User, UserAdmin)

class GroupAdmin(admin.ModelAdmin):
    """
    Usergroups
    """
    pass
admin.site.register(Group, GroupAdmin)

#_______________________________________________________________________________
# default Admin classes:

class AclOptionsAdmin(admin.ModelAdmin):
    """
    List of possible permissions
    """
    pass
admin.site.register(AclOptions, AclOptionsAdmin)

class AclRolesAdmin(admin.ModelAdmin):
    """
    Permission roles (Standard Moderator, Simple Moderator etc.)
    """
    pass
admin.site.register(AclRoles, AclRolesAdmin)

class AclRolesDataAdmin(admin.ModelAdmin):
    """
    Permissions each role contains
    """
    pass
admin.site.register(AclRolesData, AclRolesDataAdmin)

class AclUsersAdmin(admin.ModelAdmin):
    """
    Permission roles and/or individual permissions assigned to users
    """
    pass
admin.site.register(AclUsers, AclUsersAdmin)

class AttachmentsAdmin(admin.ModelAdmin):
    """
    Information on attachments (Post, physical filename, original filename, MIME type...)
    """
    pass
admin.site.register(Attachments, AttachmentsAdmin)

class BanlistAdmin(admin.ModelAdmin):
    """
    Banned users/IPs/emails...
    """
    pass
admin.site.register(Banlist, BanlistAdmin)

class BbcodesAdmin(admin.ModelAdmin):
    """
    Custom BBCodes
    """
    pass
admin.site.register(Bbcodes, BbcodesAdmin)

class BookmarksAdmin(admin.ModelAdmin):
    """
    Bookmarked topics
    """
    pass
admin.site.register(Bookmarks, BookmarksAdmin)

class BotsAdmin(admin.ModelAdmin):
    """
    Spiders/Robots
    """
    pass
admin.site.register(Bots, BotsAdmin)

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

class DraftsAdmin(admin.ModelAdmin):
    """
    Drafts of future posts/private messages
    """
    pass
admin.site.register(Drafts, DraftsAdmin)

class ExtensionGroupsAdmin(admin.ModelAdmin):
    """
    Extensions Groups (associate extensions with a file type - Images, text...)
    """
    pass
admin.site.register(ExtensionGroups, ExtensionGroupsAdmin)

class ExtensionsAdmin(admin.ModelAdmin):
    """
    Extensions (.xxx) allowed for attachments
    """
    pass
admin.site.register(Extensions, ExtensionsAdmin)

class ForumsAdmin(admin.ModelAdmin):
    """
    Forums (Name, description, rules...)
    """
    pass
admin.site.register(Forums, ForumsAdmin)

class ForumsAccessAdmin(admin.ModelAdmin):
    """
    Stores who is logged in to password protected forums
    """
    pass
admin.site.register(ForumsAccess, ForumsAccessAdmin)

class ForumsTrackAdmin(admin.ModelAdmin):
    """
    Unread post information is stored here
    """
    pass
admin.site.register(ForumsTrack, ForumsTrackAdmin)

class ForumsWatchAdmin(admin.ModelAdmin):
    """
    Subscribed forums
    """
    pass
admin.site.register(ForumsWatch, ForumsWatchAdmin)

class IconsAdmin(admin.ModelAdmin):
    """
    Post icons
    """
    pass
admin.site.register(Icons, IconsAdmin)

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

class LoginAttemptsAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(LoginAttempts, LoginAttemptsAdmin)

class ModeratorCacheAdmin(admin.ModelAdmin):
    """
    Who is a moderator in which forum (for display on forum index)
    """
    pass
admin.site.register(ModeratorCache, ModeratorCacheAdmin)

class ModulesAdmin(admin.ModelAdmin):
    """
    Configuration of acp, mcp and ucp modules
    """
    pass
admin.site.register(Modules, ModulesAdmin)

class PollOptionsAdmin(admin.ModelAdmin):
    """
    Options text of all votes ("Yes", "No", "Maybe"...)
    """
    pass
admin.site.register(PollOptions, PollOptionsAdmin)

class PollVotesAdmin(admin.ModelAdmin):
    """
    Users which have voted on a poll
    """
    pass
admin.site.register(PollVotes, PollVotesAdmin)

class PostsAdmin(admin.ModelAdmin):
    """
    Topics posts
    """
    pass
admin.site.register(Posts, PostsAdmin)

class PrivmsgsAdmin(admin.ModelAdmin):
    """
    Private messages text
    """
    pass
admin.site.register(Privmsgs, PrivmsgsAdmin)

class PrivmsgsFolderAdmin(admin.ModelAdmin):
    """
    Custom privates messages folders (for each user)
    """
    pass
admin.site.register(PrivmsgsFolder, PrivmsgsFolderAdmin)

class PrivmsgsRulesAdmin(admin.ModelAdmin):
    """
    Messages rules, e.g. "if the username of the sender is ..., move the message to this folder".
    """
    pass
admin.site.register(PrivmsgsRules, PrivmsgsRulesAdmin)

class PrivmsgsToAdmin(admin.ModelAdmin):
    """
    Information (sender, new, replied...) on private messages.
    """
    pass
admin.site.register(PrivmsgsTo, PrivmsgsToAdmin)

class ProfileFieldsAdmin(admin.ModelAdmin):
    """
    Custom profile fields (name, min/max number of characters, allowed characters...)
    """
    pass
admin.site.register(ProfileFields, ProfileFieldsAdmin)

class ProfileFieldsDataAdmin(admin.ModelAdmin):
    """
    Data that users enter in custom profile fields
    """
    pass
admin.site.register(ProfileFieldsData, ProfileFieldsDataAdmin)

class ProfileFieldsLangAdmin(admin.ModelAdmin):
    """
    tbd (empty on my forum with some custom profile fields)
    """
    pass
admin.site.register(ProfileFieldsLang, ProfileFieldsLangAdmin)

class ProfileLangAdmin(admin.ModelAdmin):
    """
    Localized name and description of custom profile fields (presented to users)
    """
    pass
admin.site.register(ProfileLang, ProfileLangAdmin)

class QaConfirmAdmin(admin.ModelAdmin):
    pass
admin.site.register(QaConfirm, QaConfirmAdmin)

class RanksAdmin(admin.ModelAdmin):
    """
    Ranks (Name, image, minimal # of posts)
    """
    pass
admin.site.register(Ranks, RanksAdmin)

class ReportsAdmin(admin.ModelAdmin):
    """
    Reported posts
    """
    pass
admin.site.register(Reports, ReportsAdmin)

class ReportsReasonsAdmin(admin.ModelAdmin):
    """
    Reasons for reported posts and disapprovals
    """
    pass
admin.site.register(ReportsReasons, ReportsReasonsAdmin)

class SearchResultsAdmin(admin.ModelAdmin):
    """
    Last searches
    """
    pass
admin.site.register(SearchResults, SearchResultsAdmin)

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

class SessionsAdmin(admin.ModelAdmin):
    """
    Sessions (to identify users browsing the forum)
    """
    pass
admin.site.register(Sessions, SessionsAdmin)

class SessionsKeysAdmin(admin.ModelAdmin):
    """
    Autologin feature
    """
    pass
admin.site.register(SessionsKeys, SessionsKeysAdmin)

class SitelistAdmin(admin.ModelAdmin):
    """
    Secure Downloads of attachments - list of IPs and hostnames
    """
    pass
admin.site.register(Sitelist, SitelistAdmin)

class SmiliesAdmin(admin.ModelAdmin):
    """
    Smilies (text => image)
    """
    pass
admin.site.register(Smilies, SmiliesAdmin)

class StylesAdmin(admin.ModelAdmin):
    """
    Style = template + theme + imageset
    """
    pass
admin.site.register(Styles, StylesAdmin)

class StylesImagesetAdmin(admin.ModelAdmin):
    """
    [[Templating_Tutorial#Customizing_the_Imageset|Imagesets]]
    """
    pass
admin.site.register(StylesImageset, StylesImagesetAdmin)

class StylesImagesetDataAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(StylesImagesetData, StylesImagesetDataAdmin)

class StylesTemplateAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(StylesTemplate, StylesTemplateAdmin)

class StylesTemplateDataAdmin(admin.ModelAdmin):
    """
    tbd
    """
    pass
admin.site.register(StylesTemplateData, StylesTemplateDataAdmin)

class StylesThemeAdmin(admin.ModelAdmin):
    """
    theme = css file
    """
    pass
admin.site.register(StylesTheme, StylesThemeAdmin)

class TopicsAdmin(admin.ModelAdmin):
    """
    Topics in forums
    """
    pass
admin.site.register(Topics, TopicsAdmin)

class TopicsPostedAdmin(admin.ModelAdmin):
    """
    Who posted to which topic (used for the small dots in viewforum)
    """
    pass
admin.site.register(TopicsPosted, TopicsPostedAdmin)

class TopicsTrackAdmin(admin.ModelAdmin):
    """
    Unread post information is stored here
    """
    pass
admin.site.register(TopicsTrack, TopicsTrackAdmin)

class TopicsWatchAdmin(admin.ModelAdmin):
    """
    "notify me upon replies"
    """
    pass
admin.site.register(TopicsWatch, TopicsWatchAdmin)

class UserGroupAdmin(admin.ModelAdmin):
    """
    Users groups
    """
    pass
admin.site.register(UserGroup, UserGroupAdmin)

class WarningsAdmin(admin.ModelAdmin):
    """
    Warnings given to users
    """
    pass
admin.site.register(Warnings, WarningsAdmin)

class WordsAdmin(admin.ModelAdmin):
    """
    censored words
    """
    pass
admin.site.register(Words, WordsAdmin)

class ZebraAdmin(admin.ModelAdmin):
    """
    Friends and foes
    """
    pass
admin.site.register(Zebra, ZebraAdmin)