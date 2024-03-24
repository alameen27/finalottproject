from django.contrib import admin
from django.urls import path, include
from .views import MovieKidDetail, MovieListView, Moviedetail, ProfileDetailView, kidmovie_list, kidprofile_details, \
    home_view, kid_profile_registration_view, list_profiles, movie_list, profile_details, profile_registration_view, \
    register_customer, login_view, KidMovieListView, upcoming_movies, delete_profile, update_profile, \
    update_kid_profile, delete_kid_profile

urlpatterns = [
    path('home/', home_view, name='home'),
    path('register/', register_customer, name='register_customer'),
    path('', login_view, name='login'),
    path('list_profiles/<int:customer_id>/', list_profiles, name='list_profiles'),
    path('profile/<int:customer_id>/', profile_registration_view, name='profile_registration'),
    path('profile/detail/<int:customer_id>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('customer/<int:customer_id>/kid-profile-registration/', kid_profile_registration_view, name='kid_profile_registration'),
    path('profile/detail/<int:customer_id>/profile/<int:profile_id>/', profile_details, name='profile_details'),
    path('profile/detail/<int:customer_id>/kidprofile/<int:profile_id>/', kidprofile_details, name='kidprofile_details'),
    path('movies/<int:profile_id>/', MovieListView.as_view(), name='movie_list'),
    path('movie_detail/<int:id>/',Moviedetail.as_view(), name='movie_detail'),
    path('kidmovielist/<int:id>/', KidMovieListView.as_view(), name='kidmovielist'),
    path('moviekiddetail/<int:id>/', MovieKidDetail.as_view(), name='moviekiddetail'),
    path('upcoming_movies/<int:movie_id>/', upcoming_movies, name='upcoming_movies'),
    path('movies/',movie_list,name='movie_list'),
    path('kidmovies/',kidmovie_list,name='kidmovie_list'),
    path('update_profile/<int:customer_id>/<int:profile_id>/', update_profile, name='update_profile'),
    path('delete_profile/<int:customer_id>/<int:profile_id>/', delete_profile, name='delete_profile'),
    path('update_kid_profile/<int:customer_id>/<int:kid_profile_id>/', update_kid_profile, name='update_kid_profile'),
    path('delete_kid_profile/<int:customer_id>/<int:kid_profile_id>/', delete_kid_profile, name='delete_kid_profile'),

  
]
