from django.urls import path
from . import views


urlpatterns = [
    # simple API, unauthorized, used for testing
    path('', views.test, name='test'),
    path('upload/', views.upload_test_form, name='api_upload'),
    path('delete/', views.delete_upload, name='api_delete'),

    # Query API
    #TODO
    #uncomment the line and adapt it according your User Stories!
    # path('correlations/<int:upload_id>/freq_dist/', views.analysis_freq_dist_view, name='api_freq_dist'),
    # path('correlations/<int:upload_id>/trend/', views.analysis_trend_view, name='api_trend'),
    # path('correlations/<int:upload_id>/spread/', views.analysis_spread_view, name='api_spread'),
    path('correlations/correlation/', views.get_correlation, name='api_correlation'),
    path('correlations/freq_dist/', views.get_corr_freq_dist, name='api_corr_freq_dist'),
]