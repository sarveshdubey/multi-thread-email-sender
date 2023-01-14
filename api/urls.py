from django.urls import path
from .views import Email_View,Subscriber_View

urlpatterns = [
    path('api/', Email_View.as_view(), name="Some name"),
    path('sub/', Subscriber_View, name="Subscribe"),
]