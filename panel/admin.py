from django.contrib import admin
from .models import Audit, Result


admin.site.register(Audit)
admin.site.register(Result)