from django.contrib import admin
from django.urls import path
from . import views

app_name = 'contest'

urlpatterns = [
    path('new/', views.ContestCreateView.as_view(), name='create-contest'),

    path('newtest/', views.ContestCreateViewTest.as_view(), name='create-contest-test'),

    path('edit/', views.ContestUpdateView.as_view(), name='update-contest'),
    path('', views.ContestListView.as_view(), name='contest-list'),
    path('<int:pk>/', views.ContestDetail.as_view(), name='contest-detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('contestant/<int:pk>/new/', views.ContestantCreateView.as_view(), name='new-contestant'),
    path('contestant/<int:pk>/edit/', views.ContestantUpdateView.as_view(), name='edit-contestant'),
    path('contestant/<int:pk>/', views.contestant_detail_view, name='contestant-detail'),
    path('contestant/<int:pk>/test', views.contestant_detail_view, name='contestant-detail-test'),
    path('contestant/<int:pk>/payment', views.paid_vote_view, name='paid_vote_view'),
    path('contestant/<int:pk>/vote', views.contestant_free_vote, name='contestant_vote'),
    path('category/<str:cats>/', views.category_view, name='category'),

    ]
