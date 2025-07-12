from django.contrib import admin
from django.urls import path
from myapp import views  # 👈 import your app's views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),  # 👈 add this line for root URL
]

