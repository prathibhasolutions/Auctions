from django.contrib import admin
from.models import User,Listing,category,Comment,Bid
# Register your models here.

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(category)
admin.site.register(Comment)







