from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import agent
import agent.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', agent.views.landing_page, name="landing"),
    path('contact/', agent.views.contact_page, name="landing_contact"),
    path('shop/', include('agent.urls')),
    path('agent/', include('agent.agent_urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
