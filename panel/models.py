from django.db import models
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list


class Audit(models.Model):
    main_url = models.URLField(name="main_url", max_length=255,
                               null=False, blank=False)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.DO_NOTHING)


class Result(models.Model):
    audit_id = models.ForeignKey(Audit, on_delete=models.DO_NOTHING)
    page_url = models.URLField(name="page_url", max_length=255,
                               null=False, blank=False)
    error_list = models.CharField(name="error_list", max_length=255, default=None,
                                  validators=[validate_comma_separated_integer_list])
