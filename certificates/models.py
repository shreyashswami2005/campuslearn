from django.db import models
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone

class Certificate(models.Model):
    """Certificate issued to a student for completing a course.
    Includes a QR code that encodes a verification URL.
    """
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(default=timezone.now)
    qr_code = models.ImageField(upload_to='certificates/qrcodes/', blank=True, null=True)
    # optional fields for PDF storage
    pdf_file = models.FileField(upload_to='certificates/pdfs/', blank=True, null=True)

    def __str__(self):
        return f"Certificate #{self.pk} – {self.student.username} – {self.course.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.qr_code:
            verification_url = f"https://collegelms.vercel.app/certificates/verify/{self.pk}/"
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(verification_url)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.qr_code.save(f'cert_{self.pk}.png', ContentFile(buffer.getvalue()), save=True)
