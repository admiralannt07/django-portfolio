from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import RangeDateFilter, RangeNumericFilter, ChoicesDropdownFilter
from unfold.contrib.forms.widgets import WysiwygWidget
from taggit.models import Tag
from taggit.admin import TaggedItemInline as TaggitTaggedItemInline
from taggit.admin import TagAdmin as TaggitTagAdmin
from .models import (
    Profile, Skill, Project, Certificate, 
    BlogCategory, BlogPost, ContactMessage
)

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['name', 'title', 'email', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'title', 'bio', 'about_desc', 'profile_image']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone', 'location']
        }),
        ('Social Links', {
            'fields': ['github_url', 'linkedin_url', 'twitter_url', 'instagram_url']
        }),
        ('Documents', {
            'fields': ['resume']
        }),
        ('SEO', {
            'fields': ['meta_description', 'meta_keywords'],
            'classes': ['collapse']
        })
    ]
    
    def has_add_permission(self, request):
        # Only allow one profile instance
        return not Profile.objects.exists()

@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    list_display = ['name', 'skill_type', 'proficiency_bar', 'is_featured', 'order']
    list_filter = [
        ('skill_type', ChoicesDropdownFilter),
        'is_featured',
        ('proficiency', RangeNumericFilter),
    ]
    list_editable = ['is_featured', 'order']
    search_fields = ['name']
    ordering = ['order', 'name']
    
    def proficiency_bar(self, obj):
        color = obj.color if obj.color else '#3b82f6'
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">'
            '<div style="width: {}%; background-color: {}; height: 20px; border-radius: 3px; text-align: center; color: white; font-size: 12px; line-height: 20px;">'
            '{}%</div></div>',
            obj.proficiency, color, obj.proficiency
        )
    proficiency_bar.short_description = 'Proficiency'

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['title', 'status', 'is_featured', 'tech_tags', 'created_at']
    list_filter = [
        ('status', ChoicesDropdownFilter),
        'is_featured',
        ('created_at', RangeDateFilter),
        'technologies',
    ]
    list_editable = ['status', 'is_featured']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-is_featured', 'order', '-created_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'slug', 'description', 'image']
        }),
        ('Detailed Content', {
            'fields': ['detailed_description']
        }),
        ('Links', {
            'fields': ['demo_url', 'github_url']
        }),
        ('Metadata', {
            'fields': ['technologies', 'status', 'is_featured', 'order']
        })
    ]
    
    def tech_tags(self, obj):
        return ', '.join([tag.name for tag in obj.technologies.all()[:3]])
    tech_tags.short_description = 'Technologies'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['detailed_description'].widget = WysiwygWidget()
        return form

@admin.register(Certificate)
class CertificateAdmin(ModelAdmin):
    list_display = ['title', 'issuer', 'issue_date', 'is_expired_status', 'is_featured']
    list_filter = [
        'issuer',
        'is_featured',
        ('issue_date', RangeDateFilter),
        'skills',
    ]
    list_editable = ['is_featured']
    search_fields = ['title', 'issuer', 'description']
    date_hierarchy = 'issue_date'
    ordering = ['-is_featured', 'order', '-issue_date']
    
    fieldsets = [
        ('Certificate Information', {
            'fields': ['title', 'issuer', 'description', 'image']
        }),
        ('Dates', {
            'fields': ['issue_date', 'expiry_date']
        }),
        ('Credentials', {
            'fields': ['credential_id', 'credential_url']
        }),
        ('Metadata', {
            'fields': ['skills', 'is_featured', 'order']
        })
    ]
    
    def is_expired_status(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red;">Expired</span>')
        elif obj.expiry_date:
            return format_html('<span style="color: green;">Valid</span>')
        return format_html('<span style="color: blue;">No Expiry</span>')
    is_expired_status.short_description = 'Status'

@admin.register(BlogCategory)
class BlogCategoryAdmin(ModelAdmin):
    list_display = ['name', 'color_preview', 'post_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def post_count(self, obj):
        return obj.blogpost_set.count()
    post_count.short_description = 'Posts'

@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'views', 'published_at']
    list_filter = [
        ('status', ChoicesDropdownFilter),
        'is_featured',
        'category',
        ('published_at', RangeDateFilter),
        'tags',
    ]
    list_editable = ['status', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-is_featured', '-published_at', '-created_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'slug', 'excerpt', 'featured_image']
        }),
        ('Content', {
            'fields': ['content']
        }),
        ('Categorization', {
            'fields': ['category', 'tags']
        }),
        ('Publishing', {
            'fields': ['status', 'is_featured', 'read_time']
        }),
        ('Statistics', {
            'fields': ['views'],
            'classes': ['collapse']
        })
    ]
    
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['content'].widget = WysiwygWidget()
        return form
    
    actions = ['make_published', 'make_draft', 'make_featured']
    
    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        queryset.update(status='draft')
    make_draft.short_description = "Mark selected posts as draft"
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Mark selected posts as featured"

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = [
        'is_read',
        ('created_at', RangeDateFilter),
    ]
    list_editable = ['is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"


class TaggedItemInline(TaggitTaggedItemInline, TabularInline):
    pass


class TagAdmin(TaggitTagAdmin, ModelAdmin):
    inlines = [TaggedItemInline]


admin.site.unregister(Tag)
admin.site.register(Tag, TagAdmin)

# Customize admin site
admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"
