from rest_framework.routers import DefaultRouter
from django.urls import path
from parser.views import HomePageView
from parser import htmx_views


app_name = 'parser'

htmx_urlpatterns = [
    path('instagram-accounts/', htmx_views.HtmxInstagramAccounts.as_view(), name='instagram-accounts'),
    path('instagram-accounts/detail/<int:pk>', htmx_views.HtmxInstagramAccountsDetail.as_view(), name='instagram-accounts-detail'),
    path('instagram-accounts/add-account/', htmx_views.HtmxInstagramAccountsCreate.as_view(), name='instagram-accounts-create'),
    path('timeline/', htmx_views.TimelineView.as_view(), name='timeline'),
]


router = DefaultRouter()
router.register(r'stats', htmx_views.AccountStatisticViewSet, basename='stats')
api_urlpatterns = router.urls


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
] + htmx_urlpatterns + api_urlpatterns
