from django.contrib import admin

# Register your models here.
from .models import Posts
# admin.site.register(Posts)
@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    """admin interface for managing posts"""
    list_display = ('id', 'img', 'title', 'description', 'externalUrl')  # Fields to display in the list view
    search_fields = ('title', 'description')  # Enable search for title and description
    list_filter = ('title',)  # Filter by external_url



    list_editable = ('title', 'description', 'externalUrl','img')

    