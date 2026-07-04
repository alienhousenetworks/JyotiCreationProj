from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from rest_framework import viewsets, generics, views, status
from rest_framework.response import Response
from .models import (
    Category, SubCategory, Product, HeroSection, EditorialSection,
    WhyChooseUsCard, HeritageSection, ProcessStep, TechnicalMetric,
    ExportCountry, Testimonial, FaqItem, B2BEnquiry,
    CategorySectionSettings, WhyChooseUsSectionSettings, ProcessSectionSettings,
    MetricsSectionSettings, ExportSectionSettings, TestimonialSectionSettings,
    FaqSectionSettings, PremiumSectionSettings, B2BEnquiryCTA,
    PartnersSectionSettings, Partner
)
from .serializers import (
    CategorySerializer, SubCategorySerializer, ProductSerializer, B2BEnquirySerializer,
    HeroSectionSerializer, EditorialSectionSerializer, WhyChooseUsCardSerializer,
    HeritageSectionSerializer, ProcessStepSerializer, TechnicalMetricSerializer,
    ExportCountrySerializer, TestimonialSerializer, FaqItemSerializer
)

# ==========================================
# FRONTEND TEMPLATE VIEWS
# ==========================================

class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Products & Catalog
        context['categories'] = Category.objects.prefetch_related('subcategories').all()
        context['products'] = Product.objects.filter(is_active=True)
        
        # Premium products grouped by category
        premium_by_cat = []
        for cat in context['categories']:
            prems = cat.products.filter(is_premium=True, is_active=True)
            if prems.exists():
                premium_by_cat.append({
                    'category': cat,
                    'products': prems
                })
        context['premium_by_category'] = premium_by_cat
        
        # Homepage Sections Config (fetch singletons or defaults)
        context['hero'] = HeroSection.objects.first()
        context['heritage'] = HeritageSection.objects.first()
        
        # New singleton config sections
        context['category_sec'] = CategorySectionSettings.objects.first()
        context['why_sec'] = WhyChooseUsSectionSettings.objects.first()
        context['process_sec'] = ProcessSectionSettings.objects.first()
        context['metrics_sec'] = MetricsSectionSettings.objects.first()
        context['export_sec'] = ExportSectionSettings.objects.first()
        context['testimonial_sec'] = TestimonialSectionSettings.objects.first()
        context['faq_sec'] = FaqSectionSettings.objects.first()
        context['premium_sec'] = PremiumSectionSettings.objects.first()
        context['enquiry_cta'] = B2BEnquiryCTA.objects.first()
        
        # List sections
        context['editorials'] = EditorialSection.objects.all()
        context['why_cards'] = WhyChooseUsCard.objects.all()
        context['steps'] = ProcessStep.objects.all()
        context['metrics'] = TechnicalMetric.objects.all()
        context['countries'] = ExportCountry.objects.all()
        context['testimonials'] = Testimonial.objects.all()
        context['faqs'] = FaqItem.objects.all()
        
        return context


class CategoryDetailView(TemplateView):
    template_name = "category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category, slug=slug)
        context['category'] = category
        context['subcategories'] = category.subcategories.all()
        context['products'] = category.products.filter(is_active=True).order_by('-created_at')
        context['categories'] = Category.objects.all()  # For nav dropdowns/links
        return context


class ShowroomView(TemplateView):
    template_name = "showroom.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.prefetch_related('subcategories').all()
        context['products'] = Product.objects.filter(is_active=True)
        return context


class PartnersView(TemplateView):
    template_name = "partners.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partners_sec'] = PartnersSectionSettings.objects.first()
        context['top_partners'] = Partner.objects.filter(is_top_highlight=True).order_by('order')[:10]
        context['all_partners'] = Partner.objects.all().order_by('order')
        return context


# ==========================================
# REST API LAYER (DRF)
# ==========================================

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category', None)
        collection = self.request.query_params.get('collection', None)
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        if collection:
            if collection == 'best_sellers':
                queryset = queryset.filter(is_best_seller=True)
            elif collection == 'new_arrivals':
                queryset = queryset.filter(is_new_arrival=True)
            elif collection == 'handcrafted':
                queryset = queryset.filter(is_handcrafted=True)
            elif collection == 'hand_painted':
                queryset = queryset.filter(is_hand_painted=True)
            elif collection == 'silk':
                queryset = queryset.filter(is_silk_collection=True)
            elif collection == 'cotton':
                queryset = queryset.filter(is_cotton_collection=True)
            elif collection == 'festive':
                queryset = queryset.filter(is_festive_collection=True)
            elif collection == 'sale':
                queryset = queryset.filter(is_sale=True)
                
        return queryset

class B2BEnquiryCreateView(generics.CreateAPIView):
    queryset = B2BEnquiry.objects.all()
    serializer_class = B2BEnquirySerializer

class HomepageConfigAPIView(views.APIView):
    """
    Get all editable section values of the B2B website in a single payload.
    """
    def get(self, request, *args, **kwargs):
        hero = HeroSection.objects.first()
        heritage = HeritageSection.objects.first()
        editorials = EditorialSection.objects.all()
        why_cards = WhyChooseUsCard.objects.all()
        steps = ProcessStep.objects.all()
        metrics = TechnicalMetric.objects.all()
        countries = ExportCountry.objects.all()
        testimonials = Testimonial.objects.all()
        faqs = FaqItem.objects.all()

        return Response({
            'hero': HeroSectionSerializer(hero).data if hero else None,
            'heritage': HeritageSectionSerializer(heritage).data if heritage else None,
            'editorials': EditorialSectionSerializer(editorials, many=True).data,
            'why_choose_us': WhyChooseUsCardSerializer(why_cards, many=True).data,
            'process_steps': ProcessStepSerializer(steps, many=True).data,
            'technical_metrics': TechnicalMetricSerializer(metrics, many=True).data,
            'export_countries': ExportCountrySerializer(countries, many=True).data,
            'testimonials': TestimonialSerializer(testimonials, many=True).data,
            'faqs': FaqItemSerializer(faqs, many=True).data,
        })
