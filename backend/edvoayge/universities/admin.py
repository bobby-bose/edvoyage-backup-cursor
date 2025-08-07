"""
Admin configuration for universities app.
Provides Django admin interface for university management.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.utils.safestring import mark_safe
from .models import (
    University, Campus, UniversityRanking, UniversityProgram,
    UniversityFaculty, UniversityResearch, UniversityPartnership, UniversityGallery
)


@admin.register(UniversityGallery)
class UniversityGalleryAdmin(admin.ModelAdmin):
    """Admin for UniversityGallery model."""
    
    list_display = [
        'university_name', 'gallery_preview', 'created_at'
    ]
    list_filter = [
        'created_at'
    ]
    search_fields = [
        'university__name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('University Information', {
            'fields': ('university',)
        }),
        ('Gallery Images', {
            'fields': ('image1', 'image2', 'image3', 'image4', 'image5', 'image6'),
            'description': 'Upload up to 6 images for the university gallery.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def university_name(self, obj):
        """Display university name with link."""
        if obj.university:
            url = reverse('admin:universities_university_change', args=[obj.university.id])
            return format_html('<a href="{}">{}</a>', url, obj.university.name)
        return '-'
    university_name.short_description = 'University'
    university_name.admin_order_field = 'university__name'
    
    def gallery_preview(self, obj):
        """Display gallery preview with all available images."""
        images = []
        for i in range(1, 7):
            image_field = getattr(obj, f'image{i}', None)
            if image_field:
                images.append(f'<img src="{image_field.url}" style="max-height: 50px; max-width: 80px; margin-right: 5px;" />')
        
        if images:
            return mark_safe("".join(images))
        return 'No images'
    gallery_preview.short_description = 'Gallery Preview'
    
    list_per_page = 25
    ordering = ['university__name', '-created_at']
    
    def save_model(self, request, obj, form, change):
        """Save model with debug information."""
        print(f"🔍 DEBUG: Saving UniversityGallery - University: {obj.university.name if obj.university else 'None'}")
        print(f"🔍 DEBUG: Images: {[getattr(obj, f'image{i}', None) for i in range(1, 7)]}")
        super().save_model(request, obj, form, change)
        print(f"🔍 DEBUG: UniversityGallery saved successfully")


class UniversityAdminForm(forms.ModelForm):
    """Custom form for University admin with gallery handling."""
    
    gallery_image1 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        help_text="Upload image 1 for the gallery"
    )
    gallery_image2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        help_text="Upload image 2 for the gallery"
    )
    gallery_image3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        help_text="Upload image 3 for the gallery"
    )
    gallery_image4 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        help_text="Upload image 4 for the gallery"
    )
    gallery_image5 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        help_text="Upload image 5 for the gallery"
    )
    gallery_image6 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        help_text="Upload image 6 for the gallery"
    )
    
    class Meta:
        model = University
        fields = [
            'name', 'short_name', 'slug', 'description', 'mission_statement',
            'vision_statement', 'university_type', 'founded_year', 'accreditation',
            'website', 'email', 'phone', 'country', 'state', 'city', 'address',
            'postal_code', 'logo', 'banner_image', 'total_students',
            'international_students', 'faculty_count', 'is_active', 'is_featured',
            'is_verified'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f"🔍 DEBUG: Initializing UniversityAdminForm")
        if self.instance and self.instance.pk:
            print(f"🔍 DEBUG: Editing existing university: {self.instance.name}")
        else:
            print(f"🔍 DEBUG: Creating new university")
    
    def save(self, commit=True):
        """Save the university with gallery images."""
        print(f"🔍 DEBUG: Saving university with gallery images")
        
        university = super().save(commit=False)
        
        # Save the university first to get the ID
        if commit:
            university.save()
            print(f"🔍 DEBUG: University saved with ID: {university.id}")
        
        # Handle gallery images
        gallery_images = []
        for i in range(1, 7):
            image_field = f'gallery_image{i}'
            if image_field in self.files:
                gallery_images.append((i, self.files[image_field]))
        
        if gallery_images:
            print(f"🔍 DEBUG: Adding {len(gallery_images)} new images to gallery")
            
            # Get or create UniversityGallery
            gallery, created = UniversityGallery.objects.get_or_create(university=university)
            if created:
                print(f"🔍 DEBUG: Created new UniversityGallery for university: {university.id}")
            else:
                print(f"🔍 DEBUG: Using existing UniversityGallery for university: {university.id}")
            
            # Set the images
            for image_num, image_file in gallery_images:
                setattr(gallery, f'image{image_num}', image_file)
                print(f"🔍 DEBUG: Set image{image_num} for gallery")
            
            gallery.save()
            print(f"🔍 DEBUG: Gallery saved successfully")
        
        return university


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    """Admin for University model."""
    
    form = UniversityAdminForm
    
    list_display = [
        'name', 'short_name', 'university_type', 'country', 'city',
        'total_students', 'international_students', 'faculty_count',
        'is_active', 'is_featured', 'is_verified', 'age', 'created_at'
    ]
    list_filter = [
        'university_type', 'country', 'state', 'is_active', 'is_featured',
        'is_verified', 'founded_year', 'created_at'
    ]
    search_fields = [
        'name', 'short_name', 'description', 'country', 'city', 'state'
    ]
    readonly_fields = [
        'age', 'international_student_percentage', 'created_at', 'updated_at',
        'logo_preview', 'banner_preview', 'gallery_preview'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_name', 'slug', 'description')
        }),
        ('Mission & Vision', {
            'fields': ('mission_statement', 'vision_statement'),
            'classes': ('collapse',)
        }),
        ('Type & Classification', {
            'fields': ('university_type', 'founded_year', 'accreditation')
        }),
        ('Contact Information', {
            'fields': ('website', 'email', 'phone'),
            'classes': ('collapse',)
        }),
        ('Location', {
            'fields': ('country', 'state', 'city', 'address', 'postal_code')
        }),
        ('Media', {
            'fields': ('logo', 'logo_preview', 'banner_image', 'banner_preview'),
            'classes': ('collapse',)
        }),
        ('Gallery Images', {
            'fields': ('gallery_image1', 'gallery_image2', 'gallery_image3', 
                      'gallery_image4', 'gallery_image5', 'gallery_image6', 'gallery_preview'),
            'classes': ('collapse',),
            'description': 'Upload up to 6 images for the university gallery.'
        }),
        ('Statistics', {
            'fields': ('total_students', 'international_students', 'faculty_count')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_verified')
        }),
        ('Metadata', {
            'fields': ('age', 'international_student_percentage', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def age(self, obj):
        """Display university age."""
        return obj.age or '-'
    age.short_description = 'Age'
    
    def logo_preview(self, obj):
        """Display logo preview."""
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "-"
    logo_preview.short_description = "Logo Preview"
    
    def banner_preview(self, obj):
        """Display banner preview."""
        if obj.banner_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.banner_image.url)
        return "-"
    banner_preview.short_description = "Banner Preview"
    
    def gallery_preview(self, obj):
        """Display gallery preview."""
        if not obj.pk:
            return "-"
        
        try:
            gallery = obj.gallery
            images = []
            for i in range(1, 7):
                image_field = getattr(gallery, f'image{i}', None)
                if image_field:
                    images.append(f'<img src="{image_field.url}" style="max-height: 60px; margin-right: 5px;" />')
            
            if images:
                return mark_safe("".join(images))
            return "No gallery images"
        except UniversityGallery.DoesNotExist:
            return "No gallery created"
    gallery_preview.short_description = "Gallery Preview"
    
    list_per_page = 25
    ordering = ['name']
    
    actions = ['activate_universities', 'deactivate_universities', 'feature_universities']
    
    def activate_universities(self, request, queryset):
        """Activate selected universities."""
        print(f"🔍 DEBUG: Activating {queryset.count()} universities")
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} universities activated successfully.')
    activate_universities.short_description = "Activate selected universities"
    
    def deactivate_universities(self, request, queryset):
        """Deactivate selected universities."""
        print(f"🔍 DEBUG: Deactivating {queryset.count()} universities")
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} universities deactivated successfully.')
    deactivate_universities.short_description = "Deactivate selected universities"
    
    def feature_universities(self, request, queryset):
        """Feature selected universities."""
        print(f"🔍 DEBUG: Featuring {queryset.count()} universities")
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} universities featured successfully.')
    feature_universities.short_description = "Feature selected universities"


@admin.register(UniversityProgram)
class UniversityProgramAdmin(admin.ModelAdmin):
    """Admin for UniversityProgram model."""
    
    list_display = [
        'name', 'university', 'program_level', 'program_type', 
        'duration_years', 'is_active', 'is_featured', 'created_at'
    ]
    list_filter = [
        'university', 'program_level', 'program_type', 'is_active', 
        'is_featured', 'duration_years', 'created_at'
    ]
    search_fields = [
        'name', 'university__name', 'description', 'objectives'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('university', 'name', 'program_level', 'program_type')
        }),
        ('Description', {
            'fields': ('description', 'objectives', 'outcomes'),
            'classes': ('collapse',)
        }),
        ('Duration & Structure', {
            'fields': ('duration_years', 'total_credits', 'semesters')
        }),
        ('Requirements', {
            'fields': ('entry_requirements', 'language_requirements'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25
    ordering = ['university__name', 'name']
    
    def save_model(self, request, obj, form, change):
        """Save model with debug information."""
        if change:
            print(f"🔍 DEBUG: Updating UniversityProgram: {obj.name} (ID: {obj.id})")
        else:
            print(f"🔍 DEBUG: Creating new UniversityProgram: {obj.name}")
        super().save_model(request, obj, form, change)
        print(f"🔍 DEBUG: UniversityProgram saved successfully")

