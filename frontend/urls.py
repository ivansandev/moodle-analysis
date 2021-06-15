from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('analysis/', views.analysis_list_view, name='analysis'),
    path('analysis/<int:upload_id>/', views.analysis_main_view, name='analysis_item'),
    path('analysis/<int:upload_id>/freq_dist/', views.analysis_freq_dist_view, name='freq_dist'),
    path('analysis/<int:upload_id>/trend/', views.analysis_trend_view, name='trend'),
    path('analysis/<int:upload_id>/spread/', views.analysis_spread_view, name='spread'),
    path('analysis/<int:upload_id>/correlations/', views.analysis_correlations_view, name='correlations'),
]