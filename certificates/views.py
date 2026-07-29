from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings
from .models import Certificate
from courses.models import Course
from django.contrib.auth import get_user_model
import os

@login_required
def generate_certificate(request, course_slug, student_id):
    """Teacher generates a certificate for a student in a course.
    Only staff users are allowed.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to generate certificates.")
    course = get_object_or_404(Course, slug=course_slug)
    student = get_object_or_404(get_user_model(), pk=student_id)
    # Create certificate instance (QR generated in save)
    cert = Certificate.objects.create(student=student, course=course)
    # Render HTML for PDF
    html_string = render_to_string('certificates/certificate.html', {'certificate': cert})
    # Generate PDF with WeasyPrint
    from weasyprint import HTML
    pdf_bytes = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    # Save PDF to FileField
    pdf_name = f'certificate_{cert.pk}.pdf'
    cert.pdf_file.save(pdf_name, content=pdf_bytes, save=True)
    return redirect('certificates:download', cert_id=cert.pk)

@login_required
def download_certificate(request, cert_id):
    cert = get_object_or_404(Certificate, pk=cert_id)
    if not cert.pdf_file:
        return HttpResponse('PDF not generated yet.', status=404)
    return FileResponse(cert.pdf_file.open('rb'), as_attachment=True, filename=os.path.basename(cert.pdf_file.name))

def verify_certificate(request, cert_id):
    cert = get_object_or_404(Certificate, pk=cert_id)
    return render(request, 'certificates/verify.html', {'certificate': cert})
