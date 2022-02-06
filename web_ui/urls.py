from django.urls import path
from web_ui.views import ElectricGuitarsView, HomePageView


urlpatterns = [
    path('', HomePageView.as_view(), name='homepage')
]
