from django.urls import path
from .views import Index,URL
urlpatterns = [
    path('', Index.as_view(),name="index"),
    path('<slug:slug>', URL.as_view(),name="URL"),
    
]
