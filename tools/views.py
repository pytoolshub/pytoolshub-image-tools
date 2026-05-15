from django.http import HttpResponse
import fitz
from django.shortcuts import render

from PIL import Image
from django.core.files.storage import FileSystemStorage


import os


def home(request):

    context = {}

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']

        target_size_kb = int(request.POST.get('target_size'))

        fs = FileSystemStorage()

        filename = fs.save(image.name, image)

        image_path = fs.path(filename)

        img = Image.open(image_path)

        compressed_name = 'compressed_' + filename

        compressed_path = os.path.join('media', compressed_name)

        quality = 95

        while quality > 10:

            img.save(compressed_path, optimize=True, quality=quality)

            current_size_kb = os.path.getsize(compressed_path) / 1024

            if current_size_kb <= target_size_kb:
                break

            quality -= 5

        context['compressed_image'] = compressed_name
        context['final_size'] = round(current_size_kb, 2)

    return render(request, 'home.html', context)


def image_tools(request):

    return render(request, 'image_tools.html')


def pdf_tools(request):

    context = {}

    if request.method == 'POST' and request.FILES.get('pdf'):

        pdf_file = request.FILES['pdf']

        fs = FileSystemStorage()

        filename = fs.save(pdf_file.name, pdf_file)

        pdf_path = fs.path(filename)

        compressed_name = 'compressed_' + filename

        compressed_path = os.path.join('media', compressed_name)

        doc = fitz.open(pdf_path)

        doc.save(compressed_path, garbage=4, deflate=True)

        doc.close()

        final_size = os.path.getsize(compressed_path) / 1024

        context['compressed_pdf'] = compressed_name
        context['final_size'] = round(final_size, 2)

    return render(request, 'pdf_tools.html', context)

def resize_50kb(request):

    context = {}

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']

        target_size_kb = 50

        fs = FileSystemStorage()

        filename = fs.save(image.name, image)

        image_path = fs.path(filename)

        img = Image.open(image_path)

        compressed_name = '50kb_' + filename

        compressed_path = os.path.join('media', compressed_name)

        quality = 95

        while quality > 10:

            img.save(compressed_path, optimize=True, quality=quality)

            current_size_kb = os.path.getsize(compressed_path) / 1024

            if current_size_kb <= target_size_kb:
                break

            quality -= 5

        context['compressed_image'] = compressed_name
        context['final_size'] = round(current_size_kb, 2)

    return render(request, 'resize_50kb.html', context)

def resize_100kb(request):

    context = {}

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']

        target_size_kb = 100

        fs = FileSystemStorage()

        filename = fs.save(image.name, image)

        image_path = fs.path(filename)

        img = Image.open(image_path)

        compressed_name = '100kb_' + filename

        compressed_path = os.path.join('media', compressed_name)

        quality = 95

        while quality > 10:

            img.save(compressed_path, optimize=True, quality=quality)

            current_size_kb = os.path.getsize(compressed_path) / 1024

            if current_size_kb <= target_size_kb:
                break

            quality -= 5

        context['compressed_image'] = compressed_name
        context['final_size'] = round(current_size_kb, 2)

    return render(request, 'resize_100kb.html', context)

def passport_photo(request):

    context = {}

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']

        fs = FileSystemStorage()

        filename = fs.save(image.name, image)

        image_path = fs.path(filename)

        img = Image.open(image_path)

        passport_size = (413, 531)

        img = img.resize(passport_size)

        passport_name = 'passport_' + filename

        passport_path = os.path.join('media', passport_name)

        img.save(passport_path)

        context['passport_image'] = passport_name

    return render(request, 'passport_photo.html', context)

def signature_resize(request):

    context = {}

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']

        fs = FileSystemStorage()

        filename = fs.save(image.name, image)

        image_path = fs.path(filename)

        img = Image.open(image_path)

        signature_size = (300, 100)

        img = img.resize(signature_size)

        signature_name = 'signature_' + filename

        signature_path = os.path.join('media', signature_name)

        quality = 85

        img.save(signature_path, optimize=True, quality=quality)

        final_size = os.path.getsize(signature_path) / 1024

        context['signature_image'] = signature_name
        context['final_size'] = round(final_size, 2)

    return render(request, 'signature_resize.html', context)

def robots_txt(request):

    data = """
User-agent: *
Allow: /

Sitemap: http://127.0.0.1:8000/sitemap.xml
"""

    return HttpResponse(data, content_type="text/plain")

def contact(request):

    return render(request, 'contact.html')

def about(request):

    return render(request, 'about.html')

def privacy_policy(request):

    return render(request, 'privacy_policy.html')

def disclaimer(request):

    return render(request, 'disclaimer.html')

def terms_conditions(request):

    return render(request, 'terms_conditions.html')
