from django.contrib import admin
from .models import Post, QA,QAnswer, CustomProfile
from .models import Document, AuthorApply
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import auth







@admin.register(CustomProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','location', 'job','uni','talents','first_name','last_name','avatar','rank','grade','is_active')
    list_filter = ('user','is_active')
    search_fields = ('user', 'is_active')

    fieldsets = ((None,
                  {'fields': ('user','location', 'job','uni','talents','first_name','last_name','avatar','rank','grade','is_active')}),)



@admin.register(QAnswer)
class QAnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'publish','edit_time', 'body','compare_id','unique')
    list_filter = ('publish','compare_id')
    search_fields = ('compare_id', 'body')
    date_hierarchy = 'publish'
    ordering = ['publish']
    fieldsets = ((None,
                  {'fields': ('author', 'publish', 'edit_time', 'body','compare_id','unique')}),)

@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    list_display = ('author','title', 'publish', 'body','fixed','id')
    list_filter = ('publish','fixed')
    search_fields = ('title', 'body')
    date_hierarchy = 'publish'
    ordering = ['publish']
    fieldsets = ((None,
                  {'fields': ('author','title', 'publish', 'body','fixed')}),)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author','title', 'publish', 'allow_comments','slug','category','type')
    list_filter = ('publish','category')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['publish']
    fieldsets = ((None, 
                  {'fields': ('author','title', 'slug', 'body',
                              'allow_comments', 'publish','category')}),)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document', 'category', 'publisher','dataset_title','file_name','publish_date','first_5_row','path','type')
    list_filter = ('publish_date','category')
    search_fields = ('document', 'category')
    date_hierarchy = 'publish_date'
    ordering = ['publish_date']
    fieldsets = ((None,
                  {'fields':
                       ('document', 'category', 'publisher','dataset_title','file_name','publish_date','first_5_row','path')
                   }),)



@admin.register(AuthorApply)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author','name','surname','job','job_talents','apply_date','uni','rustudent','text','approve')
    list_filter = ('apply_date','author')
    search_fields = ('apply_date', 'author')
    date_hierarchy = 'apply_date'
    ordering = ['apply_date']
    fieldsets = ((None,
                  {'fields':
                       ('author', 'name', 'surname', 'job', 'job_talents', 'apply_date', 'uni', 'rustudent', 'text',
                        'approve')
                   }),)