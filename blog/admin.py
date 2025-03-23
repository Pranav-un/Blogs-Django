from django.contrib import admin
from .models import Blogger, BlogPost, Comment, Reaction, Poll, PollChoice

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PollChoiceInline(admin.TabularInline):
    model = PollChoice
    extra = 3

class PollInline(admin.TabularInline):
    model = Poll
    extra = 0

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_count')
    search_fields = ('user__username', 'bio')

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'comment_count', 'reaction_count')
    list_filter = ('created_date', 'author')
    search_fields = ('title', 'content', 'author__user__username')
    date_hierarchy = 'created_date'
    inlines = [CommentInline, PollInline]

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

    def reaction_count(self, obj):
        return obj.reactions.count()
    reaction_count.short_description = 'Reactions'

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'post', 'created_date', 'total_votes')
    inlines = [PollChoiceInline]

    def total_votes(self, obj):
        return sum(choice.votes for choice in obj.choices.all())
    total_votes.short_description = 'Total Votes'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('content', 'author__username', 'post__title')

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'reaction_type', 'created_date')
    list_filter = ('reaction_type', 'created_date')
    search_fields = ('user__username', 'post__title')
