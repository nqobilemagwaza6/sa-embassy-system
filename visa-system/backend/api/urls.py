from rest_framework.routers import DefaultRouter
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import ApplicationViewSet, DocumentViewSet, NotificationViewSet, RegisterViewSet
from .session_views import custom_login_view, custom_logout_view

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'auth', RegisterViewSet, basename='auth')

urlpatterns = [
    path('auth/login/', obtain_auth_token, name='api-login'),
    # Session-based auth (simple function views)
    path('login/', custom_login_view, name='login'),
    path('logout/', custom_logout_view, name='logout'),
]

urlpatterns += router.urls
