from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}  # Ensure 'slug' field is linked to 'title'

admin.site.register(Post, PostAdmin)
