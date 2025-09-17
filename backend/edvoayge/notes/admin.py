from django.contrib import admin
from .models import (
    Subject,
    Doctor,
    Video,
    MCQ,
    Question,
    Option,
    ClinicalCase,
    Flashcard,
    FlashcardImage,
    Category
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'doctor', 'duration_in_minutes', 'is_free')
    list_filter = ('subject', 'is_free', 'doctor')
    search_fields = ('title', 'doctor__name')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(MCQ)
class MCQAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'is_free')
    list_filter = ('subject', 'is_free')
    search_fields = ('title', 'subject__name')


# Inline for options inside Question admin
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4   # show 4 option slots by default
    max_num = 4 # restrict to 4 options


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'mcq')
    list_filter = ('mcq',)
    search_fields = ('text', 'mcq__title')
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question__mcq', 'is_correct')
    search_fields = ('text', 'question__text')

@admin.register(ClinicalCase)
class ClinicalCaseAdmin(admin.ModelAdmin):
    """
    Admin view configuration for the ClinicalCase model.
    """
    
    # Fields to display in the main list view
    list_display = ('case_title','subject', 'doctor', 'created_at', 'updated_at')
    
    # Fields that can be used to filter the list
    list_filter = ( 'doctor', 'created_at','subject')
    
    # Fields to search by
    search_fields = ('case_title', 'doctor__name', 'subject')
    
    # How fields are organized in the edit/add form
    fieldsets = (
        ('Case Information', {
            'fields': ('case_title','category', 'doctor', 'subject')
        }),
        ('Examination Sections', {
            'classes': ('collapse',),  # Makes this section collapsible
            'fields': (
                'gather_equipments',
                'introduction',
                'general_inspection',
                'closer_inspection',
                'palpation',
                'final_examination',
                'references',
            ),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    
    # Fields that are read-only in the admin form
    readonly_fields = ('created_at', 'updated_at')
    
    # Helps with performance for ForeignKey relationships
    list_select_related = ('doctor','subject')

# In your app's admin.py file

# In your app's admin.py file

from django.contrib import admin
from .models import Flashcard, FlashcardImage

class FlashcardImageInline(admin.TabularInline):
    model = FlashcardImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.html import mark_safe
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    inlines = [FlashcardImageInline]
    # Updated to show 'subject' instead of 'title'
    list_display = ('subject', 'description', 'created_at')
    # Updated to filter and search by the subject's name
    list_filter = ('subject',)
    search_fields = ('subject__name', 'description')
    list_select_related = ('subject',) # Improves performance
