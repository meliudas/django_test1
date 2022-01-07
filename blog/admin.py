from django.contrib import admin
from blog.models import Post, Author, Category, CastomUser, Comments

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)

admin.site.register(CastomUser)
admin.site.register(Comments)
