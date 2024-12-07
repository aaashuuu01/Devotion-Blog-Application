from django.urls import path
from .views import (
    login_view, home, create_post, post_detail,
    blog_page, blog, edit_post, delete_post,
    contact, about, register, logout_view, index, send_email_to_users
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('create/', create_post, name='create_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),  # URL for logout
    path('edit/<int:pk>/', edit_post, name='edit_post'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),
    path('', index, name='index'),  # Default page (index)
     path('send-email/', send_email_to_users, name='send_email'),
]

