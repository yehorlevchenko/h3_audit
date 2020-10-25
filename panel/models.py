from django.db import models
from django.conf import settings


class Audit(models.Model):
    main_url = models.URLField(name="main_url", max_length=255,
                               null=False, blank=False)
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.DO_NOTHING)
    is_done = models.BooleanField(name='is_done', default=False, null=False)

    def __str__(self):
        return f'{self.main_url} => {self.owner_id}'


class Check(models.Model):
    code_error = models.IntegerField(name='code_error')
    name_error = models.CharField(name='name_error', max_length=250)
    description_error = models.CharField(name='description_error', max_length=1500)
    priority = models.IntegerField(name='priority')
    group_name = models.CharField(name='group_name', max_length=100)
    group_description = models.CharField(name='group_description', max_length=1500)

    @classmethod
    def get_group_name(cls):
        group_name_list = []
        for check in cls.objects.all():
            group_name_list.append(check.group_name)
        unique_group_name = list(set(group_name_list))
        unique_group_name.sort()
        return unique_group_name

    def __str__(self):
        return f'{self.name_error} => {self.code_error} => {self.group_name}'


class AuditResults(models.Model):
    url = models.URLField(name='url', max_length=2040, null=False)
    audit_id = models.ForeignKey(Audit, on_delete=models.DO_NOTHING)
    title_error = models.CharField(name='title_errors',
                                   max_length=32, null=True)
    description_error = models.CharField(name='description_errors',
                                         max_length=32, null=True)
    keywords_error = models.CharField(name='keywords_errors',
                                      max_length=32, null=True)
    h1_error = models.CharField(name='h1_errors',
                                max_length=32, null=True)
    h2_error = models.CharField(name='h2_errors',
                                max_length=32, null=True)
    h3_error = models.CharField(name='h3_errors',
                                max_length=32, null=True)
    status_code = models.IntegerField(name='status_code',
                                      default=0, null=False)

    def __str__(self):
        return f'{self.url} => {self.status_code} => {self.audit_id}'