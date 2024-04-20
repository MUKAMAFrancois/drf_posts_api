from django.contrib import admin
from .models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_posted']
    search_fields = ['title', 'content']
    list_filter = ['date_posted']
    readonly_fields = ('id',)

admin.site.register(Post, PostAdmin)
