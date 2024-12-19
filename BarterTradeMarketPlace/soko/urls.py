from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.list_item, name='list_item'),
    path('item/create/', views.create_item, name='create_item'),
    path('item/<int:item_id>/exchange/', views.propose_exchange, name='propose_exchange'),
    path('user/<int:user_id>/rate/', views.rate_user, name='rate_user'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark_read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('rating/edit/<int:rating_id>/', views.edit_rating_view, name='edit_rating'),
    path('category/create/', views.create_category, name='create_category'),
    path('message/send/<int:recipient_id>/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/mark_read/<int:message_id>/', views.mark_message_read, name='mark_message_read'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activity_log/', views.activity_log, name='activity_log'),
    
]