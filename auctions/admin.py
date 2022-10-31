from django.contrib import admin
from .models import User,auction_listing,category,WatchList,Bid,Comments

from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(User,UserAdmin)
admin.site.register(auction_listing)
admin.site.register(category)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(Comments)
