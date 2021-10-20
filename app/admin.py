from django.contrib import admin
from app.models import Post,Comment
# Register your models here.

#registering the post, comment models in the admin
admin.site.register(Post)
admin.site.register(Comment)
