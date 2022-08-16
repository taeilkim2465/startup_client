from django.contrib import admin
from .models import Post, Recruit, Image, Tag, Employee

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    search_fields = ['startup_name']

class ImageAdmin(admin.ModelAdmin):
    search_fields = ['post_id']

class RecruitAdmin(admin.ModelAdmin):
    search_fields = ['post_id']

class TagAdmin(admin.ModelAdmin):
    search_fields = ['post_id']

class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['post_id']

admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Recruit, RecruitAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Employee, EmployeeAdmin)