from django.contrib import admin
from .models import Forms
from .models import Child
admin.site.site_title = "Jimmy's website"#my site title
admin.site.site_header = "Jimmy The Great"#Admin site header
admin.site.index_title = "Control room"#Index title

# Register your models here.
admin.site.register(Forms)
admin.site.register(Child)


