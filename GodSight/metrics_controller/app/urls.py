from django.urls import path
from .views import MetricsDataView, GetSelectionDataView, CreateMetricView, GeneralModelDataView

urlpatterns = [
    path('metrics/chart_data', MetricsDataView.as_view(), name='metrics_data_view'),
    path('metrics/init/', GetSelectionDataView.as_view(), name='get_selection_data'),
    path('metrics/add_metric/', CreateMetricView.as_view(), name='create_metric'),
    path('metrics/general_features', GeneralModelDataView.as_view(), name='general_model'),
]
