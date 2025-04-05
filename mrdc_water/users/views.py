from rest_framework import generics, views, response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required

User = get_user_model()

# API Views
# user registration view
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserLoginAPIView(views.APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return response.Response({'token': token.key, 'role': user.role, 'username': user.username}) #added user role to response

# User Profile API View
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Web Views
def register_web(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('my-bills')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_web(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['account_id_or_email'], password=form.cleaned_data['password'])
            if user is None:
                user = authenticate(email=form.cleaned_data['account_id_or_email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('my-bills')
            else:
                form.add_error(None, 'Invalid credentials')
        else:
            form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

def logout_web(request):
    logout(request)
    return redirect('login')
