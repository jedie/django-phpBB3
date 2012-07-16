# coding: utf-8

from django.contrib import admin

from django_phpBB3.models import AclGroups, AclOptions, AclRoles, AclRolesData, \
    AclUsers, Attachments, Banlist, Bbcodes, Bookmarks, Bots, CaptchaAnswers, \
    CaptchaQuestions, Config, Confirm, Disallow, Drafts, ExtensionGroups, Extensions, \
    Forums, ForumsAccess, ForumsTrack, ForumsWatch, Groups, Icons, Lang, Log, \
    LoginAttempts, ModeratorCache, Modules, PollOptions, PollVotes, Posts, Privmsgs, \
    PrivmsgsFolder, PrivmsgsRules, PrivmsgsTo, ProfileFields, ProfileFieldsData, \
    ProfileFieldsLang, ProfileLang, QaConfirm, Ranks, Reports, ReportsReasons, \
    SearchResults, SearchWordlist, SearchWordmatch, Sessions, SessionsKeys, Sitelist, \
    Smilies, Styles, StylesImageset, StylesImagesetData, StylesTemplate, \
    StylesTemplateData, StylesTheme, Topics, TopicsPosted, TopicsTrack, TopicsWatch, \
    UserGroup, Users, Warnings, Words, Zebra


class AclGroupsAdmin(admin.ModelAdmin):
    pass
admin.site.register(AclGroups, AclGroupsAdmin)

class AclOptionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(AclOptions, AclOptionsAdmin)

class AclRolesAdmin(admin.ModelAdmin):
    pass
admin.site.register(AclRoles, AclRolesAdmin)

class AclRolesDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(AclRolesData, AclRolesDataAdmin)

class AclUsersAdmin(admin.ModelAdmin):
    pass
admin.site.register(AclUsers, AclUsersAdmin)

class AttachmentsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attachments, AttachmentsAdmin)

class BanlistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Banlist, BanlistAdmin)

class BbcodesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bbcodes, BbcodesAdmin)

class BookmarksAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bookmarks, BookmarksAdmin)

class BotsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Bots, BotsAdmin)

class CaptchaAnswersAdmin(admin.ModelAdmin):
    pass
admin.site.register(CaptchaAnswers, CaptchaAnswersAdmin)

class CaptchaQuestionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(CaptchaQuestions, CaptchaQuestionsAdmin)

class ConfigAdmin(admin.ModelAdmin):
    pass
admin.site.register(Config, ConfigAdmin)

class ConfirmAdmin(admin.ModelAdmin):
    pass
admin.site.register(Confirm, ConfirmAdmin)

class DisallowAdmin(admin.ModelAdmin):
    pass
admin.site.register(Disallow, DisallowAdmin)

class DraftsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Drafts, DraftsAdmin)

class ExtensionGroupsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExtensionGroups, ExtensionGroupsAdmin)

class ExtensionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Extensions, ExtensionsAdmin)

class ForumsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Forums, ForumsAdmin)

class ForumsAccessAdmin(admin.ModelAdmin):
    pass
admin.site.register(ForumsAccess, ForumsAccessAdmin)

class ForumsTrackAdmin(admin.ModelAdmin):
    pass
admin.site.register(ForumsTrack, ForumsTrackAdmin)

class ForumsWatchAdmin(admin.ModelAdmin):
    pass
admin.site.register(ForumsWatch, ForumsWatchAdmin)

class GroupsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Groups, GroupsAdmin)

class IconsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Icons, IconsAdmin)

class LangAdmin(admin.ModelAdmin):
    pass
admin.site.register(Lang, LangAdmin)

class LogAdmin(admin.ModelAdmin):
    pass
admin.site.register(Log, LogAdmin)

class LoginAttemptsAdmin(admin.ModelAdmin):
    pass
admin.site.register(LoginAttempts, LoginAttemptsAdmin)

class ModeratorCacheAdmin(admin.ModelAdmin):
    pass
admin.site.register(ModeratorCache, ModeratorCacheAdmin)

class ModulesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Modules, ModulesAdmin)

class PollOptionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PollOptions, PollOptionsAdmin)

class PollVotesAdmin(admin.ModelAdmin):
    pass
admin.site.register(PollVotes, PollVotesAdmin)

class PostsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Posts, PostsAdmin)

class PrivmsgsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Privmsgs, PrivmsgsAdmin)

class PrivmsgsFolderAdmin(admin.ModelAdmin):
    pass
admin.site.register(PrivmsgsFolder, PrivmsgsFolderAdmin)

class PrivmsgsRulesAdmin(admin.ModelAdmin):
    pass
admin.site.register(PrivmsgsRules, PrivmsgsRulesAdmin)

class PrivmsgsToAdmin(admin.ModelAdmin):
    pass
admin.site.register(PrivmsgsTo, PrivmsgsToAdmin)

class ProfileFieldsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProfileFields, ProfileFieldsAdmin)

class ProfileFieldsDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProfileFieldsData, ProfileFieldsDataAdmin)

class ProfileFieldsLangAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProfileFieldsLang, ProfileFieldsLangAdmin)

class ProfileLangAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProfileLang, ProfileLangAdmin)

class QaConfirmAdmin(admin.ModelAdmin):
    pass
admin.site.register(QaConfirm, QaConfirmAdmin)

class RanksAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ranks, RanksAdmin)

class ReportsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Reports, ReportsAdmin)

class ReportsReasonsAdmin(admin.ModelAdmin):
    pass
admin.site.register(ReportsReasons, ReportsReasonsAdmin)

class SearchResultsAdmin(admin.ModelAdmin):
    pass
admin.site.register(SearchResults, SearchResultsAdmin)

class SearchWordlistAdmin(admin.ModelAdmin):
    pass
admin.site.register(SearchWordlist, SearchWordlistAdmin)

class SearchWordmatchAdmin(admin.ModelAdmin):
    pass
admin.site.register(SearchWordmatch, SearchWordmatchAdmin)

class SessionsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sessions, SessionsAdmin)

class SessionsKeysAdmin(admin.ModelAdmin):
    pass
admin.site.register(SessionsKeys, SessionsKeysAdmin)

class SitelistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sitelist, SitelistAdmin)

class SmiliesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Smilies, SmiliesAdmin)

class StylesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Styles, StylesAdmin)

class StylesImagesetAdmin(admin.ModelAdmin):
    pass
admin.site.register(StylesImageset, StylesImagesetAdmin)

class StylesImagesetDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(StylesImagesetData, StylesImagesetDataAdmin)

class StylesTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(StylesTemplate, StylesTemplateAdmin)

class StylesTemplateDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(StylesTemplateData, StylesTemplateDataAdmin)

class StylesThemeAdmin(admin.ModelAdmin):
    pass
admin.site.register(StylesTheme, StylesThemeAdmin)

class TopicsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Topics, TopicsAdmin)

class TopicsPostedAdmin(admin.ModelAdmin):
    pass
admin.site.register(TopicsPosted, TopicsPostedAdmin)

class TopicsTrackAdmin(admin.ModelAdmin):
    pass
admin.site.register(TopicsTrack, TopicsTrackAdmin)

class TopicsWatchAdmin(admin.ModelAdmin):
    pass
admin.site.register(TopicsWatch, TopicsWatchAdmin)

class UserGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserGroup, UserGroupAdmin)

class UsersAdmin(admin.ModelAdmin):
    pass
admin.site.register(Users, UsersAdmin)

class WarningsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Warnings, WarningsAdmin)

class WordsAdmin(admin.ModelAdmin):
    pass
admin.site.register(Words, WordsAdmin)

class ZebraAdmin(admin.ModelAdmin):
    pass
admin.site.register(Zebra, ZebraAdmin)