from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    priority = 0.9
    changefreq = 'daily'

    def items(self):

        return [
            'home',
            'image_tools',
            'pdf_tools',
            'resize_50kb',
            'resize_100kb',
            'passport_photo',
            'signature_resize',
        ]

    def location(self, item):

        return reverse(item)