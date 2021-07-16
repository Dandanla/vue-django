from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [
    path('', views.ArticleViewSet.as_view(), name='list'),
]