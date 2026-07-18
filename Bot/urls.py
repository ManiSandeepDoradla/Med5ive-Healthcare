from django.urls import path
from .views import chatbot_api
 
 
urlpatterns = [
    path("api/chat/" , chatbot_api , name="chatbot_api")
]