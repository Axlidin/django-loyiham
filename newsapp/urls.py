from django.urls import path
from .views import ListPageView, DetailPageView, HomePageView, ContactPageView

app_name = 'newsapp'

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('all-news/', ListPageView.as_view(), name='list_page'),
    path('<int:id>/', DetailPageView, name='detail_page')
]