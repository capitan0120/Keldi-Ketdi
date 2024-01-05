from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import Xodimlar, KeldiKetdi

admin.site.unregister(Group)
admin.site.unregister(User)


admin.site.register(Xodimlar)
admin.site.register(KeldiKetdi)