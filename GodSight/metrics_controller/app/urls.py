from django.urls import path
from .views import MetricsDataView, GetSelectionDataView, CreateMetricView

urlpatterns = [
    path('metrics/chart_data', MetricsDataView.as_view(), name='metrics_data_view'),
    path('metrics/init/', GetSelectionDataView.as_view(), name='get_selection_data'),
    path('metrics/add_metric/', CreateMetricView.as_view(), name='create_metric'),
]
