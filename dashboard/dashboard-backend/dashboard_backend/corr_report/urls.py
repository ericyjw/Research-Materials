from rest_framework import routers
from .api import CorrReportViewSet

router = routers.DefaultRouter()

router.register('api/corr_reports', CorrReportViewSet, 'corr_reports')
router.register('', CorrReportViewSet, '')

urlpatterns = router.urls
# for url in urlpatterns:
#     print(url, "\n")