from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('image-tools/', views.image_tools, name='image_tools'),

    path('pdf-tools/', views.pdf_tools, name='pdf_tools'),

    path('resize-image-to-50kb/', views.resize_50kb, name='resize_50kb'),

    path('resize-image-to-100kb/', views.resize_100kb, name='resize_100kb'),

    path('passport-photo-maker/', views.passport_photo, name='passport_photo'),

    path('signature-resize-tool/', views.signature_resize, name='signature_resize'),

    path('robots.txt', views.robots_txt, name='robots_txt'),

    path('contact/', views.contact, name='contact'),

    path('about/', views.about, name='about'),

]