"""
URL configuration for cedar_shield project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt
from datetime import datetime, timedelta

# Change admin site title, header and index title
admin.site.site_header = "Phigitals Admin"  # Header on login page and admin
admin.site.site_title = "Phigitals Admin Portal"  # Browser tab title
admin.site.index_title = "Welcome to Phigitals Admin"  # Title on admin index page

@csrf_exempt
def terminal_auth(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    if not request.user.is_superuser:
        return JsonResponse({"error": "Not authorized"}, status=403)
    
    # Generate a JWT token for the WebSocket connection
    payload = {
        'user_id': request.user.id,
        'username': request.user.username,
        'is_superuser': request.user.is_superuser,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    return JsonResponse({
        "token": token,
        "websocket_url": "ws://localhost:8001/terminal"
    })

def user_status(request):
    return JsonResponse({
        "is_authenticated": request.user.is_authenticated,
        "is_superuser": getattr(request.user, 'is_superuser', False),
        "username": request.user.username if request.user.is_authenticated else None
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('terminal-auth/', terminal_auth, name='terminal_auth'),
    path('api/user-status/', user_status, name='user_status'),
    #path('api/', include('assets.urls')),  # Include your app's URL patterns under `/api/`
]

# Add this at the end of the file
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
