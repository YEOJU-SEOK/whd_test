#user/urls.py
from django.urls import path, include
from user.views import SignUpView, SignInView, UserView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/info/<int:user_id>', UserView.as_view()),
]