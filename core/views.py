from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets, generics, views, status
from rest_framework.response import Response
from .models import (
    Category, SubCategory, Product, HeroSection, EditorialSection,
    WhyChooseUsCard, HeritageSection, ProcessStep, TechnicalMetric,
    ExportCountry, Testimonial, FaqItem, B2BEnquiry,
    CategorySectionSettings, WhyChooseUsSectionSettings, ProcessSectionSettings,
    MetricsSectionSettings, ExportSectionSettings, TestimonialSectionSettings,
    FaqSectionSettings, PremiumSectionSettings, B2BEnquiryCTA,
    PartnersSectionSettings, Partner, CRMVendor, CRMClient, CRMOrder, CRMOrderItem
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


class ProductDetailView(TemplateView):
    template_name = "product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        context['product'] = product
        # Fetch up to 4 related products in the same category, excluding current product
        context['related_products'] = Product.objects.filter(
            category=product.category, 
            is_active=True
        ).exclude(id=product.id)[:4]
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


# ==========================================
# CRM VIEWS SYSTEM
# ==========================================

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/admin/login/'
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class CRMDashboardView(StaffRequiredMixin, TemplateView):
    template_name = "crm_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Core KPIs
        orders = CRMOrder.objects.all()
        context['total_revenue'] = orders.filter(status__in=['Shipped', 'Delivered']).aggregate(total=Sum('total_amount'))['total'] or 0.00
        context['total_orders_count'] = orders.count()
        context['pending_orders_count'] = orders.filter(status='Pending').count()
        context['production_orders_count'] = orders.filter(status='Production').count()
        context['total_vendors_count'] = CRMVendor.objects.count()
        context['total_clients_count'] = CRMClient.objects.count()
        
        # Recent Orders
        context['recent_orders'] = orders.order_by('-order_date', '-id')[:5]
        
        # Vendor Performance (order assignment distribution)
        vendors = CRMVendor.objects.annotate(
            orders_assigned=Count('orders'),
            total_revenue=Sum('orders__total_amount')
        ).order_by('-orders_assigned')
        context['vendors'] = vendors
        
        return context


class CRMClientListView(StaffRequiredMixin, View):
    template_name = "crm_list.html"

    def get(self, request, *args, **kwargs):
        clients = CRMClient.objects.all().order_by('-id')
        return render(request, self.template_name, {
            'view_type': 'clients',
            'items': clients,
            'title': 'CRM Clients Directory'
        })

    def post(self, request, *args, **kwargs):
        company_name = request.POST.get('company_name')
        contact_person = request.POST.get('contact_person')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')

        if company_name and contact_person and phone:
            CRMClient.objects.create(
                company_name=company_name,
                contact_person=contact_person,
                email=email,
                phone=phone,
                location=location
            )
        return redirect('crm_clients')


class CRMVendorListView(StaffRequiredMixin, View):
    template_name = "crm_list.html"

    def get(self, request, *args, **kwargs):
        vendors = CRMVendor.objects.all().order_by('-id')
        return render(request, self.template_name, {
            'view_type': 'vendors',
            'items': vendors,
            'title': 'CRM Weaver & Vendor Clusters'
        })

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        contact_person = request.POST.get('contact_person')
        phone = request.POST.get('phone')
        cluster = request.POST.get('cluster')
        active_capacity = request.POST.get('active_capacity')

        if name and cluster:
            CRMVendor.objects.create(
                name=name,
                contact_person=contact_person,
                phone=phone,
                cluster=cluster,
                active_capacity=active_capacity or "50 units/month"
            )
        return redirect('crm_vendors')


class CRMOrderListView(StaffRequiredMixin, View):
    template_name = "crm_list.html"

    def get(self, request, *args, **kwargs):
        orders = CRMOrder.objects.all().order_by('-order_date', '-id')
        return render(request, self.template_name, {
            'view_type': 'orders',
            'items': orders,
            'title': 'CRM Sourcing Orders Ledger'
        })


class CRMOrderCreateView(StaffRequiredMixin, View):
    template_name = "crm_order_form.html"

    def get(self, request, *args, **kwargs):
        clients = CRMClient.objects.all()
        vendors = CRMVendor.objects.all()
        products = Product.objects.filter(is_active=True)
        return render(request, self.template_name, {
            'clients': clients,
            'vendors': vendors,
            'products': products
        })

    def post(self, request, *args, **kwargs):
        client_id = request.POST.get('client')
        vendor_id = request.POST.get('vendor')
        status = request.POST.get('status', 'Pending')
        payment_status = request.POST.get('payment_status', 'Pending')
        total_amount = request.POST.get('total_amount', 0.00)
        custom_branding = request.POST.get('custom_branding') == 'on'
        notes = request.POST.get('notes')

        # Form product items (we can parse fields like product_1, qty_1, price_1, etc.)
        client = get_object_or_404(CRMClient, id=client_id)
        vendor = None
        if vendor_id:
            vendor = get_object_or_404(CRMVendor, id=vendor_id)

        order = CRMOrder.objects.create(
            client=client,
            vendor=vendor,
            status=status,
            payment_status=payment_status,
            total_amount=total_amount,
            custom_branding_requested=custom_branding,
            notes=notes
        )

        # Process order items
        product_ids = request.POST.getlist('products[]')
        quantities = request.POST.getlist('quantities[]')
        prices = request.POST.getlist('prices[]')

        for prod_id, qty, prc in zip(product_ids, quantities, prices):
            if prod_id and qty:
                prod = get_object_or_404(Product, id=prod_id)
                CRMOrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=int(qty),
                    price=float(prc or 0.00)
                )

        return redirect('crm_orders')

