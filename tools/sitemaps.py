from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "home",

            # Image tools
            "image_tools",
            "resize_image_to_20kb",
            "resize_image_to_50kb",
            "resize_image_to_100kb",
            "passport_photo",
            "signature_resize",
            "jpg_to_png",
            "png_to_jpg",
            "crop_image_online",

            # PDF tools
            "pdf_tools",
            "jpg_to_pdf",
            "pdf_to_jpg",
            "merge_pdf",
            "split_pdf",
            "compress_pdf",

            # Calculator tools
            "calculator_tools",
            "age_calculator",
            "percentage_calculator",
            "bmi_calculator",
            "cgpa_calculator",
            "emi_calculator",

            # Website pages
            "about",
            "contact",
            "privacy_policy",
            "disclaimer",
            "terms_conditions",
        ]

    def location(self, item):
        return reverse(item)