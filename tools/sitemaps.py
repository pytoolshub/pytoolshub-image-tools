from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    priority = 0.8
    changefreq = 'weekly'

    def items(self):

        return [

            'home',

            'image_tools',

            'pdf_tools',

            'resize_50kb',

            'resize_100kb',

            'passport_photo',

            'signature_resize',

            'jpg_to_png',

            'png_to_jpg',

            'jpg_to_pdf',

            'pdf_to_jpg',

            'merge_pdf',

            'split_pdf',

            'contact',

            'about',

            'privacy_policy',

            'disclaimer',

            'terms_conditions',

        ]

    def location(self, item):

        return reverse(item)