from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('guide/', views.guide_view, name='guide'),
    path('downloads/', views.downloads_view, name='downloads'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('ai-chat/', views.ai_chat_view, name='ai_chat'),
    path('api/ai-web-chat/', views.ai_web_chat_api, name='ai_web_chat_api'),
    path('ai-chat/transcribe/', views.transcribe_audio, name='transcribe_audio'),
    path('progress/', views.progress_view, name='progress'),
    path('contact/', views.contact_view, name='contact'),
    path('courses/', views.courses_view, name='courses'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/progress/', views.profile_progress_view, name='profile_progress'),
    path('profile/grants/', views.profile_grants_view, name='profile_grants'),
    path('profile/leaderboard/', views.profile_leaderboard_view, name='profile_leaderboard'),
    path('profile/settings/', views.profile_settings_view, name='profile_settings'),
<<<<<<< HEAD
]
=======
]
>>>>>>> 2fb66b60e5cd0fb4e449e2c10377c89bb53b022d
