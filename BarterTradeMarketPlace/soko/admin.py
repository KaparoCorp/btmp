from django.contrib import admin
from .models import Item, Appraisal, Exchange, Escrow, Rating, Category, Message, ActivityLog, Tags

admin.site.register(Item)
admin.site.register(Appraisal)
admin.site.register(Exchange)
admin.site.register(Escrow)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Message)
admin.site.register(ActivityLog)
admin.site.register(Tags)

# class ItemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'user', 'estimated_value', 'created_at')
#     search_fields = ('title',)

# admin.site.register(Item, ItemAdmin)