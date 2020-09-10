from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import agent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('agent.urls')),
    path('agent/', include('agent.agent_urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
