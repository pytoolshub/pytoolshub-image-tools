"""config URL Configuration"""

from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from tools.sitemaps import StaticViewSitemap


# ============================================================
# SITEMAP
# ============================================================

sitemaps = {
    'static': StaticViewSitemap,
}


# ============================================================
# ADS.TXT
# ============================================================

def ads_txt(request):

    return HttpResponse(
        "google.com, pub-1066940079053600, DIRECT, f08c47fec0942fa0",
        content_type="text/plain",
    )


# ============================================================
# BING VERIFICATION
# ============================================================

def bing_verify(request):

    return HttpResponse(
        """<?xml version="1.0"?>
<users>
  <user>D72CE51F64CEF829388A7157602BA283</user>
</users>""",
        content_type="application/xml",
    )


# ============================================================
# URL PATTERNS
# ============================================================

urlpatterns = [

    # Django Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Main application
    path(
        '',
        include('tools.urls')
    ),

    # Sitemap
    path(
        'sitemap.xml',
        sitemap,
        {
            'sitemaps': sitemaps
        },
        name='django.contrib.sitemaps.views.sitemap'
    ),

    # AdSense ads.txt
    path(
        'ads.txt',
        ads_txt
    ),

    # Bing verification
    path(
        'BingSiteAuth.xml',
        bing_verify
    ),

]


# ============================================================
# DEVELOPMENT MEDIA SERVING
# ============================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )