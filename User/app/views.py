from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        referral_code = request.POST.get('referral_code', None)

        # Check if the referral code exists
        referred_by = None
        if referral_code:
            try:
                referred_by = UserProfile.objects.get(referral_code=referral_code).user
            except UserProfile.DoesNotExist:
                return JsonResponse({'message': 'Invalid referral code'}, status=400)

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, referral_code=username, referred_by=referred_by)

        # Log in the user
        login(request, user)
        
        return JsonResponse({'message': 'User registered and logged in successfully'}, status=201)

    return render(request, 'registration.html')

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'User logged in successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

    return render(request, 'login.html')
