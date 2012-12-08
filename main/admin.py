from django.contrib import admin
from main.models import *

class LevelAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "published", "order_link")

admin.site.register(Level, LevelAdmin)
# admin.site.register(Sprite)
# admin.site.register(Player)
# admin.site.register(MemberSprite)
# admin.site.register(MemberPlayer)
