# your_app/models.py

import uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models

import qrcode


class QRCode(models.Model):
    link = models.URLField(
        max_length=200,
        help_text="The URL that the QR code will point to.",
    )
    qr_code = models.ImageField(
        upload_to="qr_codes/",
        blank=True,
        null=True,
        help_text="The generated QR code image.",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp.")

    def __str__(self):
        return f"QR Code for {self.link}"

    def _generate_qr_image_bytes(self):
        """
        Generate a PNG image (bytes) for the current `link`.
        Returns bytes suitable for saving with ContentFile.
        """
        qr_img = qrcode.make(self.link)  # returns a PIL Image
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)
        data = buffer.read()
        buffer.close()
        return data

    def save(self, *args, **kwargs):
        """
        Override save to generate and save a QR image when:
          - there's no qr_code yet, or
          - the link was changed.
        """
        # Determine whether we need to regenerate the image:
        must_generate = False

        if not self.qr_code:
            must_generate = True
        else:
            # If instance exists in DB, compare link to detect change
            if self.pk:
                try:
                    orig = QRCode.objects.get(pk=self.pk)
                except QRCode.DoesNotExist:
                    orig = None
                if orig and orig.link != self.link:
                    # link changed → regenerate
                    # optionally delete the old file to avoid orphaned files:
                    try:
                        orig.qr_code.delete(save=False)
                    except Exception:
                        pass
                    must_generate = True

        # If we need to generate, do it before the final save and attach the file
        if must_generate:
            image_bytes = self._generate_qr_image_bytes()
            filename = f"qr_{uuid.uuid4().hex}.png"
            self.qr_code.save(filename, ContentFile(image_bytes), save=False)

        # Finally save the model (this writes the ImageField if present)
        super().save(*args, **kwargs)













# # your_app/models.py

# from django.db import models
# from django.core.files import File
# from io import BytesIO
# import qrcode

# class QRCode(models.Model):
#     # ... (the rest of your model fields are fine) ...
#     link = models.URLField(max_length=200, help_text="The URL that the QR code will point to.")
#     qr_code = models.ImageField(upload_to='qr_codes/', blank=True, help_text="The generated QR code image.")
#     created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time the QR code was created.")

#     def __str__(self):
#         return f"QR Code for {self.link}"

#     # ❗️ Replace your old save method with this one ❗️
#     def save(self, *args, **kwargs):
#         """
#         Overrides the save method to generate a QR code.
#         """
#         # Only generate a QR code if the qr_code field is empty.
#         if not self.qr_code:
#             # qrcode.make() directly returns a PilImage object.
#             qr_image = qrcode.make(self.link)
            
#             # Use BytesIO to handle the image in memory.
#             buffer = BytesIO()
#             qr_image.save(buffer, format='PNG')
            
            
#             # Save the image from the buffer to the qr_code field.
#             file_name = f'qr_code-{self.pk or "new"}.png'
#             self.qr_code.save(file_name, File(buffer), save=False)

#         super().save(*args, **kwargs)