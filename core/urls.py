from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeView, ShowroomView, PartnersView, CategoryDetailView, CategoryViewSet, ProductViewSet, B2BEnquiryCreateView, HomepageConfigAPIView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Frontend Pages
    path('', HomeView.as_view(), name='home'),
    path('showroom/', ShowroomView.as_view(), name='showroom'),
    path('partners/', PartnersView.as_view(), name='partners'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    
    # B2B APIs
    path('api/', include(router.urls)),
    path('api/enquiry/', B2BEnquiryCreateView.as_view(), name='enquiry-create'),
    path('api/homepage-config/', HomepageConfigAPIView.as_view(), name='homepage-config'),
]
