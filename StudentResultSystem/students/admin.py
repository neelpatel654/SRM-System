from django.contrib import admin
from .models import Student, Subject

# Register your models here.
class SRMAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, SRMAdmin)
admin.site.register(Subject, SRMAdmin)