from django.db import models


class UploadFileModel(models.Model):
    title = models.CharField(max_length=10)
    file = models.FileField(upload_to='./root', null=True)