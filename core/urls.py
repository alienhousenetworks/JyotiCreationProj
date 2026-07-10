from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeView, ShowroomView, ProductDetailView, PartnersView, CategoryDetailView, CategoryViewSet, ProductViewSet,
    B2BEnquiryCreateView, HomepageConfigAPIView, CRMDashboardView, CRMClientListView,
    CRMVendorListView, CRMOrderListView, CRMOrderCreateView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Frontend Pages
    path('', HomeView.as_view(), name='home'),
    path('showroom/', ShowroomView.as_view(), name='showroom'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('partners/', PartnersView.as_view(), name='partners'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    
    # CRM Portal
    path('crm/', CRMDashboardView.as_view(), name='crm_dashboard'),
    path('crm/clients/', CRMClientListView.as_view(), name='crm_clients'),
    path('crm/vendors/', CRMVendorListView.as_view(), name='crm_vendors'),
    path('crm/orders/', CRMOrderListView.as_view(), name='crm_orders'),
    path('crm/orders/create/', CRMOrderCreateView.as_view(), name='crm_orders_create'),
    
    # B2B APIs
    path('api/', include(router.urls)),
    path('api/enquiry/', B2BEnquiryCreateView.as_view(), name='enquiry-create'),
    path('api/homepage-config/', HomepageConfigAPIView.as_view(), name='homepage-config'),
]
