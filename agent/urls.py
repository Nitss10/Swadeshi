from django.urls import path
from . import agent_views

urlpatterns = [
    # ----- Login/Signup ------
    path('', agent_views.agent_controller),
    path('agent/login/', agent_views.login_agent, name="agent_login"),
    path('agent/signup/', agent_views.signup_agent, name="agent_signup"),
    path('agent/logout/', agent_views.logout_agent, name="agent_logout"),
    path('agent/manufacturer/register', agent_views.register_manufacturer, name="manu_register"),
    # path('manu/', agent_views.manufacturer),
        
]