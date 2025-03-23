from django.contrib import admin
from .models import (User,Post,trendingsongs,promotedsongs,Comment,replycomment)

admin.site.register(User)
admin.site.register(Post)
admin.site.register(trendingsongs)
admin.site.register(promotedsongs)
admin.site.register(Comment)
admin.site.register(replycomment)


# Register your models here.
