from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Page




class PageInLine(admin.StackedInline):
    model = Page
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author','publish','status','tags']
    list_filter = ['status', 'created','publish','author','tags']
    search_fields = ['slug','title']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status','publish']
    inlines = [PageInLine]




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','active']
    list_filter = ['active','created','updated']
    search_fields = ['name','email','body']
    raw_id_fields = ['post']
