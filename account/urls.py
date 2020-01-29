from django.urls import path
from django.contrib.auth import views as auth_views


from account import views


app_name = "account"

urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('password-request-link/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),


	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('profile-BlogPics/', views.ProfileView.as_view(), name='profile'),
	path('profile/edit/', views.edit_profile, name='edit_profile'),
	path('profile/password/', views.change_password, name='change_password'),
	path('profile/<int:pk>/removeAccount/', views.DeleteAccount.as_view(), name='deleteAccount'),

	path('profile-CodeQ/', views.CodeQProfile.as_view(), name='codeq_profile'),
]
