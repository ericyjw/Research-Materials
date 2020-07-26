from rest_framework import routers
from .api import CsvFileViewSet, CommonPeriodViewSet



# urlpatterns = [
#     url(r'^$', schema_view)
# ]

router = routers.DefaultRouter()
# router.register('swagger', schema_view, 'swagger')
router.register('api/csv_files', CsvFileViewSet, 'csv_files')
router.register('', CommonPeriodViewSet, '')
# router.register('generate_reports', CommonPeriodViewSet, '')
# router.register('api/csv_files/get_common_period',
#                 CsvFileViewSet.as_view({"post": "get_common_period"}), 'get_common_period')

# urlpatterns = [
#     # url('^$', schema_view),
#     router.urls
# ]
urlpatterns = router.urls
# for url in urlpatterns:
#     print(url, "\n")