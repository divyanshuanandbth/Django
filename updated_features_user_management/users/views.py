from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, RegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import UserProfile
from django.contrib import messages
import random
import string
import json
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User


def generate_random_password(length=8):
    """Generates a random password with letters and digits."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to DB yet
            random_password = generate_random_password()  # Generate password
            user.set_password(random_password)  # Set the generated password
            user.save()  # Now save the user to the database

            # Automatically create a UserProfile
            UserProfile.objects.create(user=user)

            # Show success message with username and password
            messages.success(
                request,
                f"Registration successful! Your username is '{user.username}' and your password is '{random_password}'. Please log in."
            )
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        # Collect education details from form
        education_data = []
        boards = request.POST.getlist('board[]')
        degrees = request.POST.getlist('degree[]')
        percentages = request.POST.getlist('percentage[]')
        years = request.POST.getlist('year[]')

        for board, degree, percentage, year in zip(boards, degrees, percentages, years):
            education_data.append({
                'board': board,
                'degree': degree,
                'percentage': percentage,
                'year': year,
            })

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.education = education_data  # Save education as JSON
            profile.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'users/dashboard.html', {
        'user_form': user_form,
        'profile_form': profile_form,
})

'''@login_required
def dashboard_view(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'users/dashboard.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })'''

@login_required
def users_list_view(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

@login_required
def user_detail_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')