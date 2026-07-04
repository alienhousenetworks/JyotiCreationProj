from .models import SiteConfiguration, TrustMarqueeItem, Category

def site_settings(request):
    return {
        'site_config': SiteConfiguration.objects.first(),
        'trust_marquee': TrustMarqueeItem.objects.all(),
        'global_categories': Category.objects.prefetch_related('subcategories').all(),
    }
