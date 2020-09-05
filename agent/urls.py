from django.urls import path
from . import views

urlpatterns = [
    # ----- Login/Signup ------
    path('', views.AgentListView.as_view()),
        
]