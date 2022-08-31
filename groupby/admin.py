from django.contrib import admin
from .models import Position, CareerType, TechStack, Startup, StartupPosition, StartupImage, StartupTag, StartupMember, StartupPt

# Register your models here.
class StartupAdmin(admin.ModelAdmin):
    search_fields = ['name']

class StartupPositionAdmin(admin.ModelAdmin):
    search_fields = ['name']

class StartupImageAdmin(admin.ModelAdmin):
    search_fields = ['startup']

class StartupTagAdmin(admin.ModelAdmin):
    search_fields = ['name']

class StartupMemberAdmin(admin.ModelAdmin):
    search_fields = ['name']

class StartupPtAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PositionAdmin(admin.ModelAdmin):
    search_fields = ['name']

class CareerTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']

class TechStackAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Startup, StartupAdmin)
admin.site.register(StartupPosition, StartupPositionAdmin)
admin.site.register(StartupImage, StartupImageAdmin)
admin.site.register(StartupMember, StartupMemberAdmin)
admin.site.register(StartupTag, StartupTagAdmin)
admin.site.register(StartupPt, StartupPtAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(CareerType, CareerTypeAdmin)
admin.site.register(TechStack, TechStackAdmin)

