from django.db import models
from django.utils.text import slugify

# ==========================================
# 00. GLOBAL CONFIGURATION & BRANDING
# ==========================================

class SiteConfiguration(models.Model):
    brand_name = models.CharField(max_length=100, default="Jyoti", help_text="e.g. Jyoti")
    brand_suffix = models.CharField(max_length=100, default="creations", help_text="e.g. creations")
    site_subtitle = models.CharField(max_length=200, default="Premium B2B Manufacturer")
    intro_sub = models.CharField(max_length=200, default="Bengal Handloom Heritage Ledger", help_text="Subtext shown during the entrance animation")
    
    # Showroom Headers Configuration
    showroom_eyebrow = models.CharField(max_length=200, default="Enterprise Allocation Desk")
    showroom_title = models.CharField(max_length=200, default="B2B Showroom Catalog")
    showroom_desc = models.TextField(default="Explore our active handloom allocations and product listings. Click on any card to view manufacturing technical specifications and initialize bulk procurement inquiries.")
    
    # Contact Details
    phone_number = models.CharField(max_length=50, default="+91 99999 99999", help_text="Public contact number")
    whatsapp_number = models.CharField(max_length=50, default="919999999999", help_text="WhatsApp format without + or spaces (e.g. 919999999999)")
    email_address = models.EmailField(default="b2b@jyoticreations.com")
    
    # Cluster addresses & desks
    cluster_office = models.CharField(max_length=200, default="Bishnupur Cluster Office")
    sourcing_hub = models.CharField(max_length=200, default="Murshidabad Sourcing Hub")
    shipping_desk = models.CharField(max_length=200, default="International Shipping Desk")
    
    # Legal links text
    legal_terms_text = models.CharField(max_length=100, default="B2B Terms")
    legal_privacy_text = models.CharField(max_length=100, default="Privacy Policy")
    legal_gi_text = models.CharField(max_length=100, default="GI Certification")
    legal_export_text = models.CharField(max_length=100, default="Export Compliance")

    class Meta:
        verbose_name = "00. Global Settings & Contact Info"
        verbose_name_plural = "00. Global Settings & Contact Info"

    def __str__(self):
        return "Global Site Settings"


# ==========================================
# 01. HERO BANER
# ==========================================

class HeroSection(models.Model):
    eyebrow = models.CharField(max_length=200, default="Direct Manufacturer · Export House · OEM · Private Label")
    title = models.CharField(max_length=200, default="Bengal's Finest")
    highlighted_title = models.CharField(max_length=200, default="Handloom Sarees")
    description = models.TextField(default="Premium B2B Manufacturer & Global Export Partner for Luxury Boutiques, Fashion Houses & International Retail Chains. Garad · Korial · Baluchari · Jamdani.")
    primary_cta_text = models.CharField(max_length=100, default="Explore Collection")
    secondary_cta_text = models.CharField(max_length=100, default="Become Wholesale Partner")
    
    # Stats
    stats_years = models.CharField(max_length=50, default="52+")
    stats_retailers = models.CharField(max_length=50, default="500+")
    stats_countries = models.CharField(max_length=50, default="42")
    stats_variants = models.CharField(max_length=50, default="12K+")

    class Meta:
        verbose_name = "01. Hero Banner Section"
        verbose_name_plural = "01. Hero Banner Section"

    def __str__(self):
        return "Hero Banner Settings"


# ==========================================
# 02. TRUST RIBBON MARQUEE
# ==========================================

class TrustMarqueeItem(models.Model):
    text = models.CharField(max_length=150, help_text="e.g. ISO 9001:2015 Certified")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "02. Trust Ribbon Marquee Item"
        verbose_name_plural = "02. Trust Ribbon Marquee Items"

    def __str__(self):
        return self.text


# ==========================================
# 03. CATEGORIES & PORTFOLIOS
# ==========================================

class CategorySectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Heritage Portfolios")
    title = models.CharField(max_length=200, default="Explore Saree")
    highlighted_title = models.CharField(max_length=200, default="Categories")
    description = models.TextField(default="Select a category to view active loom allocations, technical specifications, and custom procurement options.")

    class Meta:
        verbose_name = "03a. Categories Section Header"
        verbose_name_plural = "03a. Categories Section Header"

    def __str__(self):
        return "Categories Section Headers"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = "03b. Category"
        verbose_name_plural = "03b. Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "03c. Sub-Category"
        verbose_name_plural = "03c. Sub-Categories"
        unique_together = ('category', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} -> {self.name}"


# ==========================================
# 04. PRODUCTS & CATALOG
# ==========================================

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    # B2B premium attributes
    purity_fabric = models.CharField(max_length=200, default="Grade AAAA Raw Silk", help_text="e.g. Grade AAAA Mulberry Raw Silk — Non-Bleached")
    border_specs = models.CharField(max_length=200, default="Traditional Border", help_text="e.g. Intricate 24K Gold Thread Borders")
    structural_weight = models.CharField(max_length=100, default="400 Grams", help_text="e.g. 390 Grams Linear Weight Profile")
    moq = models.CharField(max_length=100, default="10 Units", help_text="e.g. 25 Units Minimum")
    lead_time = models.CharField(max_length=100, default="14-21 Days")
    material = models.CharField(max_length=150, default="Pure Silk")
    
    image_main = models.ImageField(upload_to='products/', blank=True, null=True)
    image_hover = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Collection & Tagging filters
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_handcrafted = models.BooleanField(default=False)
    is_hand_painted = models.BooleanField(default=False)
    is_silk_collection = models.BooleanField(default=False)
    is_cotton_collection = models.BooleanField(default=False)
    is_festive_collection = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False, help_text="Show in the Premium section on home page")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "04. Product & Catalog Sourcing Entry"
        verbose_name_plural = "04. Products & Catalog Sourcing Entries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==========================================
# 05. EDITORIAL PANELS
# ==========================================

class EditorialSection(models.Model):
    section_id = models.CharField(max_length=50, unique=True, help_text="e.g. editorial_1, editorial_2")
    tag = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    highlighted_title = models.CharField(max_length=200)
    description = models.TextField()
    bullet_points = models.TextField(help_text="One bullet point per line")
    button_text = models.CharField(max_length=100, default="View Full Collection")
    is_reversed = models.BooleanField(default=False, help_text="Toggle layout alignment (left/right)")
    image = models.ImageField(upload_to='editorials/', blank=True, null=True, help_text="Optional luxury cover image for the editorial split screen")
    video = models.FileField(upload_to='editorial_videos/', blank=True, null=True, help_text="Optional luxury video loop for the editorial split screen")

    class Meta:
        verbose_name = "05. Editorial Split-Screen Panel"
        verbose_name_plural = "05. Editorial Split-Screen Panels"

    def get_bullets(self):
        return [b.strip() for b in self.bullet_points.split('\n') if b.strip()]

    def __str__(self):
        return f"Editorial - {self.tag}"


# ==========================================
# 06. WHY CHOOSE US
# ==========================================

class WhyChooseUsSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Our Advantage")
    title = models.CharField(max_length=200, default="Why Global Buyers Choose")
    highlighted_title = models.CharField(max_length=200, default="Jyoticreations")
    description = models.TextField(default="From direct loom access to private label programs — we are the complete B2B manufacturing partner for luxury saree commerce worldwide.")
    
    # The two mini stats on the left
    stat1_number = models.CharField(max_length=50, default="100%")
    stat1_label = models.CharField(max_length=100, default="Sourcing Transparency")
    stat2_number = models.CharField(max_length=50, default="ISO")
    stat2_label = models.CharField(max_length=100, default="9001:2015 Audited")

    class Meta:
        verbose_name = "06a. Why Choose Us Section Header"
        verbose_name_plural = "06a. Why Choose Us Section Header"

    def __str__(self):
        return "Why Choose Us Section Headers"

class WhyChooseUsCard(models.Model):
    title = models.CharField(max_length=150)
    icon = models.CharField(max_length=50, help_text="Emoji or icon identifier")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "06b. Why Choose Us Advantage Card"
        verbose_name_plural = "06b. Why Choose Us Advantage Cards"

    def __str__(self):
        return self.title


# ==========================================
# 07. HERITAGE & HISTORY
# ==========================================

class HeritageSection(models.Model):
    label = models.CharField(max_length=100, default="Our Heritage")
    title = models.CharField(max_length=200, default="Five Centuries of")
    highlighted_title = models.CharField(max_length=200, default="Bengali Silk Mastery")
    body_p1 = models.TextField(default="Rooted in the handloom heartlands of Bishnupur, Murshidabad, and Shantipur...")
    body_p2 = models.TextField(default="We operate exclusively as a B2B platform — no retail, no compromise...")
    
    # Specs
    specs_iso = models.CharField(max_length=100, default="9001:2015")
    specs_gi = models.CharField(max_length=100, default="Registered")
    specs_established = models.CharField(max_length=100, default="Est. 2008")
    specs_license = models.CharField(max_length=100, default="Active · 42 Nations")
    button_text = models.CharField(max_length=100, default="Begin B2B Partnership")

    class Meta:
        verbose_name = "07. Heritage & History Section"
        verbose_name_plural = "07. Heritage & History Section"

    def __str__(self):
        return "Heritage Section Settings"


# ==========================================
# 08. MANUFACTURING PROCESS
# ==========================================

class ProcessSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Our Craft")
    title = models.CharField(max_length=200, default="The")
    highlighted_title = models.CharField(max_length=200, default="Manufacturing")
    suffix_title = models.CharField(max_length=100, default="Journey")
    description = models.TextField(default="From raw silk selection to export-ready packaging — every stage is controlled in-house under ISO-certified quality protocols.")

    class Meta:
        verbose_name = "08a. Manufacturing Process Header"
        verbose_name_plural = "08a. Manufacturing Process Header"

    def __str__(self):
        return "Process Section Headers"

class ProcessStep(models.Model):
    step_number = models.CharField(max_length=10, default="01")
    icon = models.CharField(max_length=50, help_text="Emoji e.g. 🌿")
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "08b. Manufacturing Process Step"
        verbose_name_plural = "08b. Manufacturing Process Steps"

    def __str__(self):
        return f"{self.step_number} - {self.label}"


# ==========================================
# 09. TECHNICAL LOOM METRICS
# ==========================================

class MetricsSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Quality Framework")
    title = models.CharField(max_length=200, default="Technical")
    highlighted_title = models.CharField(max_length=200, default="Loom")
    suffix_title = models.CharField(max_length=100, default="Metrics")
    description = models.TextField(default="Rigorous laboratory-grade standards maintained across all production runs for international B2B compliance and customs clearance.")

    class Meta:
        verbose_name = "09a. Loom Metrics Section Header"
        verbose_name_plural = "09a. Loom Metrics Section Header"

    def __str__(self):
        return "Metrics Section Headers"

class TechnicalMetric(models.Model):
    label = models.CharField(max_length=150)
    value = models.CharField(max_length=250)
    status_tag = models.CharField(max_length=50, default="Certified", help_text="e.g. Certified, Tested, Verified, Premium, ISO Active")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "09b. Loom Metrics Specification"
        verbose_name_plural = "09b. Loom Metrics Specifications"

    def __str__(self):
        return self.label


# ==========================================
# 10. GLOBAL EXPORT MAP
# ==========================================

class ExportSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Global Reach")
    title = models.CharField(max_length=200, default="Export to")
    highlighted_title = models.CharField(max_length=200, default="42")
    suffix_title = models.CharField(max_length=100, default="Countries")
    description = models.TextField(default="Established shipping infrastructure with full customs documentation for seamless international delivery across luxury markets worldwide.")
    map_label_title = models.CharField(max_length=150, default="42 Countries")
    map_label_sub = models.CharField(max_length=200, default="Active Export Destinations")

    class Meta:
        verbose_name = "10a. Global Export Section Header"
        verbose_name_plural = "10a. Global Export Section Header"

    def __str__(self):
        return "Export Section Headers"

class ExportCountry(models.Model):
    flag = models.CharField(max_length=10, help_text="Emoji flag e.g. 🇺🇸")
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, default="Active Export")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "10b. Global Export Country"
        verbose_name_plural = "10b. Global Export Countries"

    def __str__(self):
        return self.name


# ==========================================
# 11. CLIENT TESTIMONIALS
# ==========================================

class TestimonialSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Enterprise Confidence")
    title = models.CharField(max_length=200, default="B2B")
    highlighted_title = models.CharField(max_length=200, default="Client")
    suffix_title = models.CharField(max_length=100, default="Voices")
    description = models.TextField(default="Trusted by luxury boutiques, fashion houses, and international retail chains across four continents.")
    partner_strip_label = models.CharField(max_length=200, default="Trusted by enterprises across")
    partner_strip_pills = models.TextField(default="USA · New York\nUK · London\nUAE · Dubai\nFrance · Paris\nSingapore", help_text="One partner location/pill per line")

    class Meta:
        verbose_name = "11a. Testimonials Section Header"
        verbose_name_plural = "11a. Testimonials Section Header"

    def __str__(self):
        return "Testimonial Section Headers"

    def get_partner_pills(self):
        return [p.strip() for p in self.partner_strip_pills.split('\n') if p.strip()]

class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "11b. Testimonials Customer Review"
        verbose_name_plural = "11b. Testimonials Customer Reviews"

    def __str__(self):
        return f"{self.author} ({self.location})"


# ==========================================
# 12. FAQ
# ==========================================

class FaqSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Support Ledger")
    title = models.CharField(max_length=200, default="Frequently Asked")
    highlighted_title = models.CharField(max_length=200, default="Questions")
    description = models.TextField(default="Essential information regarding production capacity, lead times, export documentation, and custom orders.")

    class Meta:
        verbose_name = "12a. FAQ Section Header"
        verbose_name_plural = "12a. FAQ Section Header"

    def __str__(self):
        return "FAQ Section Headers"

class FaqItem(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "12b. FAQ Item"
        verbose_name_plural = "12b. FAQ Items"

    def __str__(self):
        return self.question


# ==========================================
# 13. PREMIUM PRODUCTS & CTA
# ==========================================

class PremiumSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Exclusive Selections")
    title = models.CharField(max_length=200, default="Premium B2B")
    highlighted_title = models.CharField(max_length=200, default="Creations")
    description = models.TextField(default="Explore our most exclusive handloom creations selected for priority showroom allocation. Filtered by category.")

    class Meta:
        verbose_name = "13a. Premium Products Section Header"
        verbose_name_plural = "13a. Premium Products Section Header"

    def __str__(self):
        return "Premium Section Headers"

class B2BEnquiryCTA(models.Model):
    badge = models.CharField(max_length=200, default="B2B Access Portal · Now Accepting Partners")
    title = models.CharField(max_length=200, default="Begin Your Premium")
    highlighted_title = models.CharField(max_length=200, default="Wholesale Partnership")
    description = models.TextField(default="Join 500+ boutiques and luxury retailers sourcing directly from our Bengali silk clusters. Allocations are capacity-limited — contact our procurement team to secure priority access.")
    whatsapp_button_text = models.CharField(max_length=150, default="✆ Contact Procurement Desk")
    email_button_text = models.CharField(max_length=150, default="✉ Send Formal Enquiry")
    guarantees = models.TextField(default="Response within 4 hours\nMOQ from 10 units\nFree sample packs\nGlobal shipping included", help_text="One guarantee per line")

    class Meta:
        verbose_name = "13b. Wholesale Partnership CTA Section"
        verbose_name_plural = "13b. Wholesale Partnership CTA Section"

    def get_guarantees(self):
        return [g.strip() for g in self.guarantees.split('\n') if g.strip()]

    def __str__(self):
        return "B2B Wholesale CTA Settings"


# ==========================================
# 14. ENQUIRIES (READ ONLY)
# ==========================================

class B2BEnquiry(models.Model):
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "14. B2B Trade Enquiry Received"
        verbose_name_plural = "14. B2B Trade Enquiries Received"

    def __str__(self):
        return f"Enquiry from {self.name} ({self.company or 'No Company'})"


# ==========================================
# 15. PARTNERS LIST
# ==========================================

class PartnersSectionSettings(models.Model):
    label = models.CharField(max_length=100, default="Enterprise Network")
    title = models.CharField(max_length=200, default="Our Global")
    highlighted_title = models.CharField(max_length=200, default="B2B Partners")
    description = models.TextField(default="We collaborate with premier fashion boutiques, luxury retail networks, and international sourcing agencies.")

    class Meta:
        verbose_name = "15a. Partners Section Header"
        verbose_name_plural = "15a. Partners Section Header"

    def __str__(self):
        return "Partners Section Headers"


class Partner(models.Model):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, help_text="Partner logo or emblem image")
    is_top_highlight = models.BooleanField(default=False, help_text="Highlight this partner at the top of the list (Max 10)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "15b. Global Partner"
        verbose_name_plural = "15b. Global Partners"

    def __str__(self):
        return self.name
