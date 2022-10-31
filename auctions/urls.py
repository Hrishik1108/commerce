from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listings',views.create,name="create"),
    path('listings/<int:id>',views.listing,name="listing"),
    path('watchlist',views.watchlist,name="watchlist"),
    path('category',views.categories,name="categories"),
    path('category/<int:ids>',views.category_id,name="category_id"),
    path('add/<int:id>',views.add,name="add"),


] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
