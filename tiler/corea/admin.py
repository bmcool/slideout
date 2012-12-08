from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _

class BaseLevelAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "published", "order_link")
    actions = ['published_reverse']
    ordering = ["order"]
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user.member
        obj.save()
    
    def queryset(self, request):
        qs = super(BaseLevelAdmin, self).queryset(request)
        return qs.filter(owner=request.user.member)
    
    def published_reverse(self, request, queryset):
        for level in queryset:
            level.published = not level.published
            level.save()
    published_reverse.short_description = _('Published/Unpublished the selected levels')
