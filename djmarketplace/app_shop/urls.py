from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import register_view, CustomLoginView, CustomLogoutView, MainView, UserUpdateView, CartView, add_good_to_cart, pay

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('reqister/', register_view, name='register'),
    path('', MainView.as_view(), name='main'),
    path('profile/<int:pk>', UserUpdateView.as_view(), name='profile'),
    path('cart/', CartView.as_view(), name='cart'), #6 (06.02.)
    path('add_good.<int:pk>/', add_good_to_cart, name='add_good'), #6 (06.02.)
    path('cart/pay/<int:pk>/', pay, name='pay'), #7 (08.02.)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)