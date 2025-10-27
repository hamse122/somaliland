"""
Enhanced admin functionality for immigration models.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    TravelDocument, TravelDocumentChild,
    DegmadaForm, DegmadaFormMember,
    KafiilkaForm, KafiilkaFormMember
)
from .utils import DocumentValidator, ReportGenerator


class TravelDocumentChildInline(admin.TabularInline):
    """Inline for travel document children."""
    model = TravelDocumentChild
    extra = 0
    fields = ('name', 'birth_date', 'birth_place', 'photo', 'photo_preview')
    readonly_fields = ('photo_preview',)
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.photo.url
            )
        return '-'
    photo_preview.short_description = 'Photo'


@admin.register(TravelDocument)
class TravelDocumentAdmin(admin.ModelAdmin):
    """Admin interface for Travel Documents."""
    
    list_display = (
        'document_number', 'full_name', 'region',
        'district', 'status', 'date', 'created_at',
        'status_color', 'actions'
    )
    list_filter = ('status', 'region', 'district', 'created_at', 'date')
    search_fields = (
        'document_number', 'full_name', 'identification_number',
        'phone_number', 'sponsor_name'
    )
    readonly_fields = (
        'document_number', 'created_at', 'updated_at',
        'created_by', 'photo_preview'
    )
    date_hierarchy = 'created_at'
    inlines = [TravelDocumentChildInline]
    
    fieldsets = (
        ('Document Information', {
            'fields': (
                'document_number', 'region_office', 'date', 'status'
            )
        }),
        ('Personal Information', {
            'fields': (
                'full_name', 'mother_name', 'birth_date', 'birth_place',
                'identification_number', 'photo', 'photo_preview'
            )
        }),
        ('Location Information', {
            'fields': (
                'region', 'district', 'workplace'
            )
        }),
        ('Sponsor Information', {
            'fields': (
                'sponsor_name', 'citizen_card', 'phone_number',
                'contact_number', 'nationality', 'job_type', 'license_number'
            )
        }),
        ('Documents Status', {
            'fields': (
                'has_notayo', 'has_sponsor_id', 'has_damaged_id',
                'has_company_license', 'has_other_documents'
            )
        }),
        ('Immigration Officer', {
            'fields': (
                'filled_date', 'immigration_officer_notes',
                'card_number', 'officer_signature'
            )
        }),
        ('System Information', {
            'fields': (
                'created_at', 'updated_at', 'created_by'
            )
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="200" height="200" style="object-fit: cover;" />',
                obj.photo.url
            )
        return 'No photo'
    photo_preview.short_description = 'Photo Preview'
    
    def status_color(self, obj):
        colors = {
            'filled': '#FFA500',   # Orange
            'approved': '#00FF00',  # Green
            'printed': '#0000FF',   # Blue
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_color.short_description = 'Status'
    
    def actions(self, obj):
        return format_html(
            '<a href="{}" class="button">View</a>&nbsp;'
            '<a href="{}" class="button">Edit</a>',
            reverse('admin:immigration_traveldocument_change', args=[obj.pk]),
            reverse('admin:immigration_traveldocument_change', args=[obj.pk])
        )
    actions.short_description = 'Actions'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class DegmadaFormMemberInline(admin.TabularInline):
    """Inline for degmada form members."""
    model = DegmadaFormMember
    extra = 0
    fields = ('name', 'nationality', 'birth_date', 'phone', 'id_number', 'photo')


@admin.register(DegmadaForm)
class DegmadaFormAdmin(admin.ModelAdmin):
    """Admin interface for Degmada Forms."""
    
    list_display = ('reference', 'company_name', 'sponsor_name', 'gobolka', 'degmada', 'date', 'created_at')
    list_filter = ('gobolka', 'degmada', 'created_at', 'date')
    search_fields = ('reference', 'company_name', 'sponsor_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    inlines = [DegmadaFormMemberInline]
    
    fieldsets = (
        ('Form Information', {
            'fields': ('reference', 'date', 'gobolka', 'degmada')
        }),
        ('Company/Organization', {
            'fields': (
                'company_name', 'company_license', 'establishment_period',
                'working_employees', 'company_region', 'company_district'
            )
        }),
        ('Sponsor Information', {
            'fields': (
                'sponsor_name', 'sponsor_id', 'sponsor_phone',
                'sponsor_contact', 'sponsor_address'
            )
        }),
        ('Approval Information', {
            'fields': (
                'pledge_name', 'pledge_signature',
                'district_leader_name', 'district_leader_signature',
                'filled_date', 'attachment_types', 'special_notes'
            )
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class KafiilkaFormMemberInline(admin.TabularInline):
    """Inline for kafiilka form members."""
    model = KafiilkaFormMember
    extra = 0
    fields = ('name', 'nationality', 'birth_date', 'phone', 'id_number', 'photo')


@admin.register(KafiilkaForm)
class KafiilkaFormAdmin(admin.ModelAdmin):
    """Admin interface for Kafiilka Forms."""
    
    list_display = ('reference', 'company_name', 'sponsor_name', 'sponsor_type', 'gobolka', 'degmada', 'date', 'created_at')
    list_filter = ('sponsor_type', 'gobolka', 'degmada', 'created_at', 'date')
    search_fields = ('reference', 'company_name', 'sponsor_name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    inlines = [KafiilkaFormMemberInline]
    
    fieldsets = (
        ('Form Information', {
            'fields': ('reference', 'date', 'gobolka', 'degmada')
        }),
        ('Company/Organization', {
            'fields': (
                'company_name', 'company_license', 'establishment_period',
                'working_employees', 'company_region', 'company_district'
            )
        }),
        ('Sponsor Information', {
            'fields': (
                'sponsor_type', 'sponsor_name', 'sponsor_id',
                'sponsor_phone', 'sponsor_contact', 'sponsor_address'
            )
        }),
        ('Approval Information', {
            'fields': (
                'pledge_name', 'pledge_signature',
                'district_leader_name', 'district_leader_signature',
                'filled_date', 'attachment_types', 'special_notes'
            )
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# Customize admin site
admin.site.site_header = 'Somaliland Immigration Administration'
admin.site.site_title = 'Immigration Admin'
admin.site.index_title = 'Welcome to Immigration Administration'

