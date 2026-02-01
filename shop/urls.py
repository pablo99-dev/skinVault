from django.urls import path
from .views import login_view, signup_view, dashboard, weapon_detail_by_name, logout_view, favorites_view, add_favorite

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path("dashboard/", dashboard, name="dashboard"),
    path('weapon/<str:weapon_name>/', weapon_detail_by_name, name='weapon_detail_by_name'),
    path('favorites/', favorites_view, name='favorites'),
    path('logout/', logout_view, name='logout'),
    path('add_favorite/', add_favorite, name='add_favorite'),
    # supprime ou commente la ligne qui utilisait 'home'
    # path('', home, name='home'),
]
