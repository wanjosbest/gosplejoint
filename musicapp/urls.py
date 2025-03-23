from django.urls import path
from. import views

urlpatterns = [
    path("", views.index, name ="index"),
    path('play/<int:song_id>/', views.play_song, name='play_song'),
    path('download/<int:song_id>/', views.download_song, name='download_song'),
    path("songstat", views.user_song_stats, name="song_stats"),
    path("all-songs/", views.allposts, name="all_songs"),
    path("posts/<slug>/",views.postdetails, name="post_details"),
    path("search/", views.search, name="search"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("upload-song/", views.musicianuploadsong, name="musicianuploadsong"),
    path("profile/", views.artistprofile, name="profile"),
    path("songs/<str:username>/", views.songs, name="songs"),
    
   
   
]
