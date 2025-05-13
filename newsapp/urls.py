from django.urls import path
from .views import (ListPageView, DetailPageView, HomePageView, ContactPageView,
                    LocalNewsViews, XorijNewsViews, SportNewsViews, TechnolgyNewsViews,
                    UpdateNewsView, DeleteNewsView, CreateNewsView, SearchListView, EditCommentView, DeleteCommentView,
                    NewsLikeView)

app_name = 'newsapp'

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),

    path('search/', SearchListView.as_view(), name='search'),

    path('create/', CreateNewsView.as_view(), name='create_news'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('all-news/', ListPageView.as_view(), name='list_page'),
    path('local-news/', LocalNewsViews.as_view(), name='localnews'),
    path('xorij-news/', XorijNewsViews.as_view(), name='xorijnews'),
    path('sport-news/', SportNewsViews.as_view(), name='sportnews'),
    path('technology-news/', TechnolgyNewsViews.as_view(), name='technologynews'),
    path('<slug:slug>/update/', UpdateNewsView.as_view(), name='update_news'),
    path('<slug:slug>/delete/', DeleteNewsView.as_view(), name='delete_news'),
    path('<slug:slug>/', DetailPageView.as_view(), name='detail_page'),

    path("comment/<int:pk>/edit/", EditCommentView.as_view(), name='edit_comment'),
    path("comment/<int:pk>/delete/", DeleteCommentView.as_view(), name='delete_comment'),

    path("like/<slug:slug>/", NewsLikeView.as_view(), name='like'),
]