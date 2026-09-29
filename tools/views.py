import os
import uuid
from io import BytesIO
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

import fitz

from PIL import Image

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render

from PyPDF2 import PdfMerger, PdfReader, PdfWriter


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_storage():
    """
    Return Django's configured file storage.
    """
    return FileSystemStorage()


def unique_filename(prefix, extension):
    """
    Create a unique filename so files do not overwrite each other.
    """
    return f"{prefix}_{uuid.uuid4().hex}{extension}"


def save_pil_image(image, filename, image_format="JPEG", **kwargs):
    """
    Save a PIL image using Django FileSystemStorage.
    Returns the saved filename.
    """

    storage = get_storage()

    buffer = BytesIO()

    image.save(
        buffer,
        format=image_format,
        **kwargs
    )

    buffer.seek(0)

    saved_name = storage.save(
        filename,
        ContentFile(buffer.getvalue())
    )

    return saved_name


def compress_image_to_target(image_path, target_size_kb):
    """
    Compress an image to approximately <= target_size_kb.

    Output format is JPEG.
    """

    storage = get_storage()

    img = Image.open(image_path)

    if img.mode != "RGB":

        if img.mode in ("RGBA", "LA"):

            background = Image.new(
                "RGB",
                img.size,
                "white"
            )

            background.paste(
                img,
                mask=img.getchannel("A")
            )

            img = background

        else:
            img = img.convert("RGB")

    target_bytes = target_size_kb * 1024

    working_img = img.copy()

    quality = 95

    while True:

        buffer = BytesIO()

        working_img.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True
        )

        current_size = len(
            buffer.getvalue()
        )

        if current_size <= target_bytes:
            break

        if quality > 20:

            quality -= 5
            continue

        new_width = int(
            working_img.width * 0.90
        )

        new_height = int(
            working_img.height * 0.90
        )

        if (
            new_width < 50
            or new_height < 50
        ):
            break

        working_img = working_img.resize(
            (
                new_width,
                new_height
            ),
            Image.Resampling.LANCZOS
        )

        quality = 80

    output_name = unique_filename(
        f"compressed_{target_size_kb}kb",
        ".jpg"
    )

    buffer.seek(0)

    saved_name = storage.save(
        output_name,
        ContentFile(buffer.getvalue())
    )

    final_size = (
        storage.size(saved_name) / 1024
    )

    return saved_name, round(final_size, 2)


def save_pdf_from_path(source_doc, output_filename):
    """
    Save a PyMuPDF document inside MEDIA_ROOT.
    """

    storage = get_storage()

    output_path = storage.path(
        output_filename
    )

    source_doc.save(
        output_path,
        garbage=4,
        deflate=True
    )

    return output_filename


# ============================================================
# HOME
# ============================================================

def home(request):

    context = {}

    if request.method == "POST":

        image = request.FILES.get("image")
        target_size = request.POST.get(
            "target_size"
        )

        if image and target_size:

            try:

                target_size_kb = int(
                    target_size
                )

                if target_size_kb <= 0:
                    raise ValueError

                storage = get_storage()

                uploaded_name = storage.save(
                    image.name,
                    image
                )

                uploaded_path = storage.path(
                    uploaded_name
                )

                compressed_name, final_size = (
                    compress_image_to_target(
                        uploaded_path,
                        target_size_kb
                    )
                )

                try:
                    storage.delete(
                        uploaded_name
                    )
                except Exception:
                    pass

                context["compressed_image"] = (
                    compressed_name
                )

                context["final_size"] = (
                    final_size
                )

            except (
                ValueError,
                InvalidOperation
            ):

                context["error"] = (
                    "Please enter a valid target size."
                )

    return render(
        request,
        "home.html",
        context
    )


# ============================================================
# IMAGE TOOLS
# ============================================================

def image_tools(request):

    return render(
        request,
        "image_tools.html"
    )


# ============================================================
# PDF TOOLS
# ============================================================

def pdf_tools(request):

    context = {}

    if request.method == "POST":

        pdf_file = request.FILES.get(
            "pdf"
        )

        if pdf_file:

            storage = get_storage()

            filename = storage.save(
                pdf_file.name,
                pdf_file
            )

            pdf_path = storage.path(
                filename
            )

            compressed_name = unique_filename(
                "compressed_pdf",
                ".pdf"
            )

            compressed_path = storage.path(
                compressed_name
            )

            doc = fitz.open(
                pdf_path
            )

            doc.save(
                compressed_path,
                garbage=4,
                deflate=True
            )

            doc.close()

            final_size = (
                storage.size(compressed_name)
                / 1024
            )

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

            context["compressed_pdf"] = (
                compressed_name
            )

            context["final_size"] = round(
                final_size,
                2
            )

    return render(
        request,
        "pdf_tools.html",
        context
    )


# ============================================================
# RESIZE IMAGE TO 20KB
# ============================================================

def resize_20kb(request):

    context = {}

    if (
        request.method == "POST"
        and request.FILES.get("image")
    ):

        image = request.FILES["image"]

        storage = get_storage()

        filename = storage.save(
            image.name,
            image
        )

        image_path = storage.path(
            filename
        )

        try:

            compressed_name, final_size = (
                compress_image_to_target(
                    image_path,
                    20
                )
            )

            context["compressed_image"] = (
                compressed_name
            )

            context["final_size"] = (
                final_size
            )

        finally:

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

    return render(
        request,
        "resize_image_to_20kb.html",
        context
    )


# ============================================================
# RESIZE IMAGE TO 50KB
# ============================================================

def resize_50kb(request):

    context = {}

    if (
        request.method == "POST"
        and request.FILES.get("image")
    ):

        image = request.FILES["image"]

        storage = get_storage()

        filename = storage.save(
            image.name,
            image
        )

        image_path = storage.path(
            filename
        )

        try:

            compressed_name, final_size = (
                compress_image_to_target(
                    image_path,
                    50
                )
            )

            context["compressed_image"] = (
                compressed_name
            )

            context["final_size"] = (
                final_size
            )

        finally:

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

    return render(
        request,
        "resize_50kb.html",
        context
    )


# ============================================================
# RESIZE IMAGE TO 100KB
# ============================================================

def resize_100kb(request):

    context = {}

    if (
        request.method == "POST"
        and request.FILES.get("image")
    ):

        image = request.FILES["image"]

        storage = get_storage()

        filename = storage.save(
            image.name,
            image
        )

        image_path = storage.path(
            filename
        )

        try:

            compressed_name, final_size = (
                compress_image_to_target(
                    image_path,
                    100
                )
            )

            context["compressed_image"] = (
                compressed_name
            )

            context["final_size"] = (
                final_size
            )

        finally:

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

    return render(
        request,
        "resize_100kb.html",
        context
    )


# ============================================================
# PASSPORT PHOTO
# ============================================================

def passport_photo(request):

    context = {}

    if (
        request.method == "POST"
        and request.FILES.get("image")
    ):

        image = request.FILES["image"]

        storage = get_storage()

        filename = storage.save(
            image.name,
            image
        )

        image_path = storage.path(
            filename
        )

        try:

            img = Image.open(
                image_path
            )

            passport_size = (
                413,
                531
            )

            img = img.resize(
                passport_size,
                Image.Resampling.LANCZOS
            )

            if img.mode != "RGB":
                img = img.convert("RGB")

            passport_name = unique_filename(
                "passport",
                ".jpg"
            )

            saved_name = save_pil_image(
                img,
                passport_name,
                "JPEG",
                quality=95
            )

            context["passport_image"] = (
                saved_name
            )

        finally:

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

    return render(
        request,
        "passport_photo.html",
        context
    )


# ============================================================
# SIGNATURE RESIZE
# ============================================================

def signature_resize(request):

    context = {}

    if (
        request.method == "POST"
        and request.FILES.get("image")
    ):

        image = request.FILES["image"]

        storage = get_storage()

        filename = storage.save(
            image.name,
            image
        )

        image_path = storage.path(
            filename
        )

        try:

            img = Image.open(
                image_path
            )

            signature_size = (
                300,
                100
            )

            img = img.resize(
                signature_size,
                Image.Resampling.LANCZOS
            )

            if img.mode != "RGB":
                img = img.convert("RGB")

            signature_name = unique_filename(
                "signature",
                ".jpg"
            )

            saved_name = save_pil_image(
                img,
                signature_name,
                "JPEG",
                quality=85,
                optimize=True
            )

            final_size = (
                storage.size(saved_name)
                / 1024
            )

            context["signature_image"] = (
                saved_name
            )

            context["final_size"] = round(
                final_size,
                2
            )

        finally:

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

    return render(
        request,
        "signature_resize.html",
        context
    )


# ============================================================
# ROBOTS.TXT
# ============================================================

def robots_txt(request):

    data = """
User-agent: *
Allow: /

Sitemap: https://pytoolshub.in/sitemap.xml
"""

    return HttpResponse(
        data.strip(),
        content_type="text/plain"
    )


# ============================================================
# STATIC PAGES
# ============================================================

def contact(request):

    return render(
        request,
        "contact.html"
    )


def about(request):

    return render(
        request,
        "about.html"
    )


def privacy_policy(request):

    return render(
        request,
        "privacy_policy.html"
    )


def disclaimer(request):

    return render(
        request,
        "disclaimer.html"
    )


def terms_conditions(request):

    return render(
        request,
        "terms_conditions.html"
    )


# ============================================================
# JPG TO PNG
# ============================================================

def jpg_to_png(request):

    converted_image = None

    if (
        request.method == "POST"
        and request.FILES.get("image")
    ):

        image = request.FILES["image"]

        storage = get_storage()

        filename = storage.save(
            image.name,
            image
        )

        image_path = storage.path(
            filename
        )

        try:

            img = Image.open(
                image_path
            )

            if img.mode not in (
                "RGB",
                "RGBA"
            ):
                img = img.convert("RGB")

            png_filename = unique_filename(
                "converted",
                ".png"
            )

            converted_image = save_pil_image(
                img,
                png_filename,
                "PNG",
                optimize=True
            )

        finally:

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

    return render(
        request,
        "jpg_to_png.html",
        {
            "converted_image":
                converted_image
        }
    )


# ============================================================
# PNG TO JPG
# ============================================================

def png_to_jpg(request):

    converted_image = None

    if (
        request.method == "POST"
        and request.FILES.get("image")
    ):

        image = request.FILES["image"]

        storage = get_storage()

        filename = storage.save(
            image.name,
            image
        )

        image_path = storage.path(
            filename
        )

        try:

            img = Image.open(
                image_path
            ).convert("RGB")

            jpg_filename = unique_filename(
                "converted",
                ".jpg"
            )

            converted_image = save_pil_image(
                img,
                jpg_filename,
                "JPEG",
                quality=95,
                optimize=True
            )

        finally:

            try:
                storage.delete(
                    filename
                )
            except Exception:
                pass

    return render(
        request,
        "png_to_jpg.html",
        {
            "converted_image":
                converted_image
        }
    )


# ============================================================
# JPG TO PDF
# ============================================================

def jpg_to_pdf(request):

    pdf_file = None

    if request.method == "POST":

        image = request.FILES.get(
            "image"
        )

        if image:

            storage = get_storage()

            filename = storage.save(
                image.name,
                image
            )

            image_path = storage.path(
                filename
            )

            try:

                img = Image.open(
                    image_path
                ).convert("RGB")

                pdf_filename = unique_filename(
                    "converted",
                    ".pdf"
                )

                pdf_path = storage.path(
                    pdf_filename
                )

                img.save(
                    pdf_path,
                    "PDF",
                    resolution=100.0
                )

                pdf_file = pdf_filename

            finally:

                try:
                    storage.delete(
                        filename
                    )
                except Exception:
                    pass

    return render(
        request,
        "jpg_to_pdf.html",
        {
            "pdf_file": pdf_file
        }
    )


# ============================================================
# PDF TO JPG
# ============================================================

def pdf_to_jpg(request):

    converted_image = None

    if request.method == "POST":

        pdf = request.FILES.get(
            "pdf"
        )

        if pdf:

            storage = get_storage()

            filename = storage.save(
                pdf.name,
                pdf
            )

            pdf_path = storage.path(
                filename
            )

            try:

                doc = fitz.open(
                    pdf_path
                )

                if doc.page_count > 0:

                    page = doc.load_page(0)

                    pix = page.get_pixmap(
                        matrix=fitz.Matrix(
                            2,
                            2
                        ),
                        alpha=False
                    )

                    jpg_filename = unique_filename(
                        "pdf_to_jpg",
                        ".jpg"
                    )

                    jpg_path = storage.path(
                        jpg_filename
                    )

                    pix.save(
                        jpg_path
                    )

                    converted_image = (
                        jpg_filename
                    )

                doc.close()

            finally:

                try:
                    storage.delete(
                        filename
                    )
                except Exception:
                    pass

    return render(
        request,
        "pdf_to_jpg.html",
        {
            "converted_image":
                converted_image
        }
    )


# ============================================================
# MERGE PDF
# ============================================================

def merge_pdf(request):

    merged_pdf = None

    if request.method == "POST":

        pdf1 = request.FILES.get(
            "pdf1"
        )

        pdf2 = request.FILES.get(
            "pdf2"
        )

        if pdf1 and pdf2:

            storage = get_storage()

            file1 = storage.save(
                pdf1.name,
                pdf1
            )

            file2 = storage.save(
                pdf2.name,
                pdf2
            )

            path1 = storage.path(
                file1
            )

            path2 = storage.path(
                file2
            )

            merged_filename = unique_filename(
                "merged",
                ".pdf"
            )

            merged_path = storage.path(
                merged_filename
            )

            merger = PdfMerger()

            try:

                merger.append(path1)
                merger.append(path2)

                with open(
                    merged_path,
                    "wb"
                ) as output_file:

                    merger.write(
                        output_file
                    )

                merged_pdf = (
                    merged_filename
                )

            finally:

                merger.close()

                try:
                    storage.delete(file1)
                    storage.delete(file2)
                except Exception:
                    pass

    return render(
        request,
        "merge_pdf.html",
        {
            "merged_pdf": merged_pdf
        }
    )


# ============================================================
# SPLIT PDF
# ============================================================

def split_pdf(request):

    split_pdf_file = None

    if request.method == "POST":

        pdf = request.FILES.get(
            "pdf"
        )

        if pdf:

            storage = get_storage()

            filename = storage.save(
                pdf.name,
                pdf
            )

            pdf_path = storage.path(
                filename
            )

            try:

                reader = PdfReader(
                    pdf_path
                )

                if len(reader.pages) > 0:

                    writer = PdfWriter()

                    writer.add_page(
                        reader.pages[0]
                    )

                    split_filename = unique_filename(
                        "split_page_1",
                        ".pdf"
                    )

                    split_path = storage.path(
                        split_filename
                    )

                    with open(
                        split_path,
                        "wb"
                    ) as output_pdf:

                        writer.write(
                            output_pdf
                        )

                    split_pdf_file = (
                        split_filename
                    )

            finally:

                try:
                    storage.delete(
                        filename
                    )
                except Exception:
                    pass

    return render(
        request,
        "split_pdf.html",
        {
            "split_pdf_file":
                split_pdf_file
        }
    )


# ============================================================
# CROP IMAGE ONLINE
# ============================================================

def crop_image_online(request):

    cropped_image = None

    if (
        request.method == "POST"
        and request.POST.get("crop_submit") == "1"
    ):

        image = request.FILES.get(
            "image"
        )

        if image:

            try:

                left = int(
                    request.POST.get(
                        "left",
                        0
                    )
                )

                top = int(
                    request.POST.get(
                        "top",
                        0
                    )
                )

                right = int(
                    request.POST.get(
                        "right",
                        200
                    )
                )

                bottom = int(
                    request.POST.get(
                        "bottom",
                        200
                    )
                )

            except ValueError:

                left = 0
                top = 0
                right = 200
                bottom = 200

            storage = get_storage()

            filename = storage.save(
                image.name,
                image
            )

            file_path = storage.path(
                filename
            )

            try:

                img = Image.open(
                    file_path
                )

                left = max(
                    0,
                    min(left, img.width)
                )

                top = max(
                    0,
                    min(top, img.height)
                )

                right = max(
                    left + 1,
                    min(right, img.width)
                )

                bottom = max(
                    top + 1,
                    min(bottom, img.height)
                )

                cropped = img.crop(
                    (
                        left,
                        top,
                        right,
                        bottom
                    )
                )

                if cropped.mode != "RGB":

                    cropped = cropped.convert(
                        "RGB"
                    )

                cropped_name = unique_filename(
                    "cropped",
                    ".jpg"
                )

                cropped_image = save_pil_image(
                    cropped,
                    cropped_name,
                    "JPEG",
                    quality=95,
                    optimize=True
                )

            finally:

                try:
                    storage.delete(
                        filename
                    )
                except Exception:
                    pass

    return render(
        request,
        "crop_image_online.html",
        {
            "cropped_image":
                cropped_image
        }
    )


# ============================================================
# COMPRESS PDF
# ============================================================

def compress_pdf(request):

    if request.method == "POST":

        pdf = request.FILES.get(
            "pdf"
        )

        if pdf:

            reader = PdfReader(
                pdf
            )

            writer = PdfWriter()

            for page in reader.pages:

                try:
                    page.compress_content_streams()
                except Exception:
                    pass

                writer.add_page(
                    page
                )

            response = HttpResponse(
                content_type="application/pdf"
            )

            response[
                "Content-Disposition"
            ] = (
                'attachment; '
                'filename="compressed.pdf"'
            )

            writer.write(
                response
            )

            return response

    return render(
        request,
        "compress_pdf.html"
    )


# ============================================================
# MEDIA FILE PREVIEW
# ============================================================

def media_file(request, filename):

    filename = os.path.basename(
        filename
    )

    storage = get_storage()

    try:
        file_path = storage.path(
            filename
        )
    except Exception:
        raise Http404(
            "File not found."
        )

    if not os.path.isfile(file_path):

        raise Http404(
            "File not found."
        )

    return FileResponse(
        open(
            file_path,
            "rb"
        ),
        as_attachment=False,
        filename=filename
    )


# ============================================================
# FILE DOWNLOAD
# ============================================================

def download_file(request, filename):

    filename = os.path.basename(
        filename
    )

    storage = get_storage()

    try:
        file_path = storage.path(
            filename
        )
    except Exception:
        raise Http404(
            "File not found."
        )

    if not os.path.isfile(file_path):

        raise Http404(
            "File not found."
        )

    response = FileResponse(
        open(
            file_path,
            "rb"
        ),
        as_attachment=True,
        filename=filename
    )

    response["Cache-Control"] = (
        "no-cache, no-store, must-revalidate"
    )

    response["Pragma"] = "no-cache"

    response["Expires"] = "0"

    return response


# ============================================================
# CALCULATOR TOOLS
# ============================================================

def calculator_tools(request):

    return render(
        request,
        "calculator_tools.html"
    )


# ============================================================
# AGE CALCULATOR
# ============================================================

def age_calculator(request):

    age = None

    if request.method == "POST":

        dob = request.POST.get(
            "dob"
        )

        if dob:

            try:

                birth_date = datetime.strptime(
                    dob,
                    "%Y-%m-%d"
                ).date()

                today = date.today()

                age = (
                    today.year
                    - birth_date.year
                )

                if (
                    (today.month, today.day)
                    <
                    (
                        birth_date.month,
                        birth_date.day
                    )
                ):
                    age -= 1

            except ValueError:

                age = None

    return render(
        request,
        "age_calculator.html",
        {
            "age": age
        }
    )


# ============================================================
# PERCENTAGE CALCULATOR
# ============================================================

def percentage_calculator(request):

    result = None

    if request.method == "POST":

        try:

            total = Decimal(
                request.POST.get(
                    "total",
                    "0"
                )
            )

            percent = Decimal(
                request.POST.get(
                    "percent",
                    "0"
                )
            )

            result = (
                total * percent
            ) / Decimal("100")

            result = round(
                result,
                2
            )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            result = None

    return render(
        request,
        "percentage_calculator.html",
        {
            "result": result
        }
    )


# ============================================================
# BMI CALCULATOR
# ============================================================

def bmi_calculator(request):

    bmi = None
    category = None

    if request.method == "POST":

        try:

            weight = Decimal(
                request.POST.get(
                    "weight",
                    "0"
                )
            )

            height = Decimal(
                request.POST.get(
                    "height",
                    "0"
                )
            )

            height_m = (
                height / Decimal("100")
            )

            if (
                weight > 0
                and height_m > 0
            ):

                bmi_decimal = (
                    weight
                    /
                    (
                        height_m
                        * height_m
                    )
                )

                bmi = round(
                    bmi_decimal,
                    2
                )

                if bmi < 18.5:
                    category = "Underweight"

                elif bmi < 25:
                    category = "Normal weight"

                elif bmi < 30:
                    category = "Overweight"

                else:
                    category = "Obesity"

        except (
            InvalidOperation,
            TypeError,
            ValueError,
            ZeroDivisionError
        ):

            bmi = None
            category = None

    return render(
        request,
        "bmi_calculator.html",
        {
            "bmi": bmi,
            "category": category
        }
    )


# ============================================================
# CGPA CALCULATOR
# ============================================================

def cgpa_calculator(request):

    cgpa = None
    percentage = None

    if request.method == "POST":

        try:

            value = Decimal(
                request.POST.get(
                    "cgpa",
                    "0"
                )
            )

            if value >= 0:

                cgpa = round(
                    value,
                    2
                )

                percentage = round(
                    value * Decimal("9.5"),
                    2
                )

        except (
            InvalidOperation,
            TypeError,
            ValueError
        ):

            cgpa = None
            percentage = None

    return render(
        request,
        "cgpa_calculator.html",
        {
            "cgpa": cgpa,
            "percentage": percentage
        }
    )


# ============================================================
# EMI CALCULATOR
# ============================================================

def emi_calculator(request):

    emi = None
    total_payment = None
    total_interest = None

    if request.method == "POST":

        try:

            principal = Decimal(
                request.POST.get(
                    "principal",
                    request.POST.get(
                        "amount",
                        "0"
                    )
                )
            )

            annual_rate = Decimal(
                request.POST.get(
                    "interest",
                    request.POST.get(
                        "rate",
                        "0"
                    )
                )
            )

            tenure_years = Decimal(
                request.POST.get(
                    "tenure",
                    request.POST.get(
                        "years",
                        "0"
                    )
                )
            )

            if (
                principal > 0
                and annual_rate >= 0
                and tenure_years > 0
            ):

                number_of_months = int(
                    tenure_years
                    * Decimal("12")
                )

                if number_of_months <= 0:
                    raise ValueError

                monthly_rate = (
                    annual_rate
                    /
                    Decimal("12")
                    /
                    Decimal("100")
                )

                if monthly_rate == 0:

                    emi_value = (
                        principal
                        /
                        Decimal(
                            number_of_months
                        )
                    )

                else:

                    factor = (
                        Decimal("1")
                        + monthly_rate
                    ) ** number_of_months

                    emi_value = (
                        principal
                        * monthly_rate
                        * factor
                        /
                        (
                            factor
                            - Decimal("1")
                        )
                    )

                total_payment_value = (
                    emi_value
                    * Decimal(
                        number_of_months
                    )
                )

                total_interest_value = (
                    total_payment_value
                    - principal
                )

                emi = round(
                    emi_value,
                    2
                )

                total_payment = round(
                    total_payment_value,
                    2
                )

                total_interest = round(
                    total_interest_value,
                    2
                )

        except (
            InvalidOperation,
            TypeError,
            ValueError,
            ZeroDivisionError
        ):

            emi = None
            total_payment = None
            total_interest = None

    return render(
        request,
        "emi_calculator.html",
        {
            "emi": emi,
            "total_payment": total_payment,
            "total_interest": total_interest
        }
    )