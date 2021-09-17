from django.urls import path
from . import views

urlpatterns = [
    path("", views.article_CR),
    path("<int:pk>/", views.article_RUD),
    path("<int:pk>/comment/", views.comment_CR),
    path("<int:pk>/comment/<int:comment_pk>/", views.comment_D),
    path("<int:pk>/comment_article/<int:comment_pk>/", views.comment_article_reverse),
]
