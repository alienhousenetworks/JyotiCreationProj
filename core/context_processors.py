from .models import SiteConfiguration, TrustMarqueeItem, Category, PartnersSectionSettings


def partners_page_is_visible(site_config=None, partners_sec=None):
    """
    Partners is shown in header/footer only when both:
    - SiteConfiguration.partners_page_active is True (or no config row), and
    - PartnersSectionSettings.is_active is True (or no section row).
    """
    if site_config is None:
        site_config = SiteConfiguration.objects.first()
    if site_config is not None and not site_config.partners_page_active:
        return False
    if partners_sec is None:
        partners_sec = PartnersSectionSettings.objects.first()
    if partners_sec is not None and not partners_sec.is_active:
        return False
    return True


def site_settings(request):
    site_config = SiteConfiguration.objects.first()
    partners_sec = PartnersSectionSettings.objects.first()
    return {
        'site_config': site_config,
        'trust_marquee': TrustMarqueeItem.objects.all(),
        'global_categories': Category.objects.prefetch_related('subcategories').all(),
        'partners_page_visible': partners_page_is_visible(site_config, partners_sec),
    }
