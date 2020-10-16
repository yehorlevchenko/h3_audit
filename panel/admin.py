from django.contrib import admin
from .models import Audit, Check, AuditResults


admin.site.register(Audit)
admin.site.register(Check)
admin.site.register(AuditResults)
