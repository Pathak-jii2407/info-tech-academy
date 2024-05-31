from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(StudentStatus)
admin.site.register(StudentInfo)
admin.site.register(TeacherAccount)
admin.site.register(Edit)

