
from django.urls import path
from . import views

urlpatterns = [
    path('scrape', views.scrape, name='scrape'),
    path('news', views.news, name='news'),
    path('news_single/<int:id>', views.single_news, name='news_single'),
    path('facebook-details', views.facebook_details, name='facebook_details'),
    ]