from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = router.urls
