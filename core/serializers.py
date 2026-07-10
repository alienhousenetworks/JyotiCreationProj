from rest_framework import serializers
from .models import (
    Category, SubCategory, Product, ProductImage, HeroSection, EditorialSection,
    WhyChooseUsCard, HeritageSection, ProcessStep, TechnicalMetric,
    ExportCountry, Testimonial, FaqItem, B2BEnquiry
)

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'description']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'subcategories']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True, default='')
    additional_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name', 'subcategory', 'subcategory_name',
            'description', 'purity_fabric', 'border_specs', 'structural_weight', 'moq',
            'lead_time', 'material', 'image_main', 'image_hover', 'video', 'additional_images',
            'is_best_seller', 'is_new_arrival', 'is_handcrafted', 'is_hand_painted',
            'is_silk_collection', 'is_cotton_collection', 'is_festive_collection', 'is_sale', 'is_premium',
            'is_active'
        ]

class B2BEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = B2BEnquiry
        fields = ['id', 'name', 'company', 'email', 'phone', 'message', 'custom_branding_requested', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']

# Sections Serializers
class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = '__all__'

class EditorialSectionSerializer(serializers.ModelSerializer):
    bullets = serializers.SerializerMethodField()

    class Meta:
        model = EditorialSection
        fields = ['section_id', 'tag', 'title', 'highlighted_title', 'description', 'bullet_points', 'bullets', 'button_text', 'is_reversed', 'image', 'video']

    def get_bullets(self, obj):
        return obj.get_bullets()

class WhyChooseUsCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUsCard
        fields = '__all__'

class HeritageSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeritageSection
        fields = '__all__'

class ProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessStep
        fields = '__all__'

class TechnicalMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalMetric
        fields = '__all__'

class ExportCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportCountry
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class FaqItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqItem
        fields = '__all__'
