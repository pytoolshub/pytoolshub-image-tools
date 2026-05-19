
from django.http import HttpResponse
import fitz
from django.shortcuts import render

from pdf2image import convert_from_path
from PyPDF2 import PdfMerger

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

Sitemap: https://pytoolshub.onrender.com/sitemap.xml
"""

    return HttpResponse(data, content_type="text/plain")

def contact(request):

    return render(request, 'contact.html')

def about(request):

    return render(request, 'about.html')

def privacy_policy(request):

    return render(request, 'privacy_policy.html')

def jpg_to_png(request):

    converted_image = None

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']

        fs = FileSystemStorage()

        filename = fs.save(image.name, image)

        image_path = fs.path(filename)

        img = Image.open(image_path)

        png_filename = filename.rsplit('.', 1)[0] + '.png'

        png_path = os.path.join('media', png_filename)

        img.save(png_path, 'PNG')

        converted_image = png_filename

    return render(
        request,
        'jpg_to_png.html',
        {
            'converted_image': converted_image
        }
    )

def disclaimer(request):

    return render(request, 'disclaimer.html')

def terms_conditions(request):

    return render(request, 'terms_conditions.html')

def png_to_jpg(request):

    converted_image = None

    if request.method == 'POST' and request.FILES.get('image'):

        image = request.FILES['image']

        fs = FileSystemStorage()

        filename = fs.save(image.name, image)

        image_path = fs.path(filename)

        img = Image.open(image_path).convert('RGB')

        jpg_filename = filename.rsplit('.', 1)[0] + '.jpg'

        jpg_path = os.path.join('media', jpg_filename)

        img.save(jpg_path, 'JPEG')

        converted_image = jpg_filename

    return render(
        request,
        'png_to_jpg.html',
        {
            'converted_image': converted_image
        }
    )

def jpg_to_pdf(request):

    pdf_file = None

    if request.method == 'POST':

        image = request.FILES.get('image')

        if image:

            fs = FileSystemStorage()

            filename = fs.save(image.name, image)

            image_path = fs.path(filename)

            pdf_filename = filename.rsplit('.', 1)[0] + '.pdf'

            pdf_path = os.path.join('media', pdf_filename)

            image_open = Image.open(image_path)

            rgb_image = image_open.convert('RGB')

            rgb_image.save(pdf_path)

            pdf_file = pdf_filename

    return render(
        request,
        'jpg_to_pdf.html',
        {
            'pdf_file': pdf_file
        }
    )

def pdf_to_jpg(request):

    converted_image = None

    if request.method == 'POST':

        pdf = request.FILES.get('pdf')

        if pdf:

            fs = FileSystemStorage()

            filename = fs.save(pdf.name, pdf)

            pdf_path = fs.path(filename)

            images = convert_from_path(pdf_path)

            jpg_filename = filename.rsplit('.', 1)[0] + '.jpg'

            jpg_path = os.path.join('media', jpg_filename)

            images[0].save(jpg_path, 'JPEG')

            converted_image = jpg_filename

    return render(
        request,
        'pdf_to_jpg.html',
        {
            'converted_image': converted_image
        }
    )

def merge_pdf(request):

    merged_pdf = None

    if request.method == 'POST':

        pdf1 = request.FILES.get('pdf1')
        pdf2 = request.FILES.get('pdf2')

        if pdf1 and pdf2:

            fs = FileSystemStorage()

            file1 = fs.save(pdf1.name, pdf1)
            file2 = fs.save(pdf2.name, pdf2)

            path1 = fs.path(file1)
            path2 = fs.path(file2)

            merger = PdfMerger()

            merger.append(path1)
            merger.append(path2)

            merged_filename = 'merged.pdf'

            merged_path = os.path.join('media', merged_filename)

            merger.write(merged_path)

            merger.close()

            merged_pdf = merged_filename

    return render(
        request,
        'merge_pdf.html',
        {
            'merged_pdf': merged_pdf
        }
    )

def split_pdf(request):

    split_pdf_file = None

    if request.method == 'POST':

        pdf = request.FILES.get('pdf')

        if pdf:

            fs = FileSystemStorage()

            filename = fs.save(pdf.name, pdf)

            pdf_path = fs.path(filename)

            from PyPDF2 import PdfReader, PdfWriter

            reader = PdfReader(pdf_path)

            writer = PdfWriter()

            writer.add_page(reader.pages[0])

            split_filename = 'split_page_1.pdf'

            split_path = os.path.join('media', split_filename)

            with open(split_path, 'wb') as output_pdf:

                writer.write(output_pdf)

            split_pdf_file = split_filename

    return render(
        request,
        'split_pdf.html',
        {
            'split_pdf_file': split_pdf_file
        }
    )