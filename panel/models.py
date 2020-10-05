from django.db import models
from django.conf import settings


class Audit(models.Model):
    main_url = models.URLField(name="main_url", max_length=255,
                               null=False, blank=False)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.DO_NOTHING)

