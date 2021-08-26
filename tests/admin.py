from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Question)
admin.site.register(TestPart)
admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(TestResult)
admin.site.register(Category)

