from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('post/<int:pk>/reaction/<str:reaction_type>/', views.add_reaction, name='add-reaction'),
    path('post/<int:post_pk>/poll/create/', views.create_poll, name='create-poll'),
    path('poll/choice/<int:choice_pk>/vote/', views.vote_poll, name='vote-poll'),
    path('bloggers/', views.BloggerListView.as_view(), name='blogger-list'),
    path('blogger/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('profile/', views.profile_view, name='profile'),
]
