from django.contrib import admin
from .models import (
    SiteConfiguration, HeroSection, TrustMarqueeItem, CategorySectionSettings,
    Category, SubCategory, Product, ProductImage, EditorialSection, WhyChooseUsSectionSettings,
    WhyChooseUsCard, HeritageSection, ProcessSectionSettings, ProcessStep,
    MetricsSectionSettings, TechnicalMetric, ExportSectionSettings, ExportCountry,
    TestimonialSectionSettings, Testimonial, FaqSectionSettings, FaqItem,
    PremiumSectionSettings, B2BEnquiryCTA, B2BEnquiry, PartnersSectionSettings,
    Partner, CRMVendor, CRMClient, CRMOrder, CRMOrderItem
)

# Singleton pattern helper for Section configurations
class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(SingletonAdmin):
    list_display = ('brand_name', 'brand_suffix', 'email_address', 'phone_number')
    fieldsets = (
        ('Branding', {
            'fields': ('brand_name', 'brand_suffix', 'site_subtitle', 'intro_sub')
        }),
        ('Showroom Page Headers', {
            'fields': ('showroom_eyebrow', 'showroom_title', 'showroom_desc')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'whatsapp_number', 'email_address')
        }),
        ('Desks & Hubs', {
            'fields': ('cluster_office', 'sourcing_hub', 'shipping_desk')
        }),
        ('Legal Page Links Text', {
            'fields': ('legal_terms_text', 'legal_privacy_text', 'legal_gi_text', 'legal_export_text')
        }),
    )

@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    list_display = ('title', 'highlighted_title', 'stats_years', 'stats_retailers', 'stats_countries')

@admin.register(TrustMarqueeItem)
class TrustMarqueeItemAdmin(admin.ModelAdmin):
    list_display = ('text', 'order')
    list_editable = ('order',)

@admin.register(CategorySectionSettings)
class CategorySectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    ordering = ('order',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'moq', 'material', 'is_active', 'is_best_seller', 'is_new_arrival')
    list_filter = ('category', 'subcategory', 'is_active', 'is_best_seller', 'is_new_arrival', 'is_handcrafted', 'is_hand_painted')
    search_fields = ('name', 'description', 'purity_fabric', 'material')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'subcategory', 'description')
        }),
        ('B2B Sourcing Metrics', {
            'fields': ('purity_fabric', 'border_specs', 'structural_weight', 'moq', 'lead_time', 'material')
        }),
        ('Images & Media', {
            'fields': ('image_main', 'image_hover', 'video')
        }),
        ('Collection Filters', {
            'fields': ('is_best_seller', 'is_new_arrival', 'is_handcrafted', 'is_hand_painted', 'is_silk_collection', 'is_cotton_collection', 'is_festive_collection', 'is_sale', 'is_premium')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(EditorialSection)
class EditorialSectionAdmin(admin.ModelAdmin):
    list_display = ('tag', 'title', 'section_id', 'is_reversed')
    list_editable = ('is_reversed',)

@admin.register(WhyChooseUsSectionSettings)
class WhyChooseUsSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title')

@admin.register(WhyChooseUsCard)
class WhyChooseUsCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)

@admin.register(HeritageSection)
class HeritageSectionAdmin(SingletonAdmin):
    list_display = ('title', 'highlighted_title', 'specs_iso', 'specs_gi')

@admin.register(ProcessSectionSettings)
class ProcessSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title', 'suffix_title')

@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'label', 'icon', 'order')
    list_editable = ('order',)

@admin.register(MetricsSectionSettings)
class MetricsSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title', 'suffix_title')

@admin.register(TechnicalMetric)
class TechnicalMetricAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'status_tag', 'order')
    list_editable = ('order',)

@admin.register(ExportSectionSettings)
class ExportSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title', 'suffix_title')

@admin.register(ExportCountry)
class ExportCountryAdmin(admin.ModelAdmin):
    list_display = ('flag', 'name', 'tag', 'order')
    list_editable = ('order',)

@admin.register(TestimonialSectionSettings)
class TestimonialSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'role', 'location', 'order')
    list_editable = ('order',)

@admin.register(FaqSectionSettings)
class FaqSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title')

@admin.register(FaqItem)
class FaqItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)

@admin.register(PremiumSectionSettings)
class PremiumSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title')

@admin.register(B2BEnquiryCTA)
class B2BEnquiryCTAAdmin(SingletonAdmin):
    list_display = ('badge', 'title', 'highlighted_title')

@admin.register(B2BEnquiry)
class B2BEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'custom_branding_requested', 'submitted_at')
    readonly_fields = ('name', 'company', 'email', 'phone', 'message', 'custom_branding_requested', 'submitted_at')
    search_fields = ('name', 'company', 'email', 'message')
    date_hierarchy = 'submitted_at'

@admin.register(PartnersSectionSettings)
class PartnersSectionSettingsAdmin(SingletonAdmin):
    list_display = ('label', 'title', 'highlighted_title')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_top_highlight', 'order')
    list_editable = ('is_top_highlight', 'order')
    list_filter = ('is_top_highlight',)
    search_fields = ('name',)


# ==========================================
# CRM ADMIN REGISTRATION
# ==========================================

@admin.register(CRMVendor)
class CRMVendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'cluster', 'active_capacity')
    search_fields = ('name', 'contact_person', 'phone', 'cluster')
    list_filter = ('cluster',)

@admin.register(CRMClient)
class CRMClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone', 'location')
    search_fields = ('company_name', 'contact_person', 'email', 'phone', 'location')

class CRMOrderItemInline(admin.TabularInline):
    model = CRMOrderItem
    extra = 1

@admin.register(CRMOrder)
class CRMOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'vendor', 'status', 'payment_status', 'total_amount', 'custom_branding_requested', 'order_date')
    list_filter = ('status', 'payment_status', 'custom_branding_requested', 'order_date')
    search_fields = ('client__company_name', 'client__contact_person', 'vendor__name', 'notes')
    inlines = [CRMOrderItemInline]
    date_hierarchy = 'order_date'

